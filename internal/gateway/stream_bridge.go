package gateway

import (
	"archive/zip"
	"crypto/rand"
	"crypto/rc4"
	"crypto/rsa"
	"crypto/tls"
	"io"
	"net/http"
	"os"
	"path/filepath"
)

// StreamBridge relays media streams between distribution nodes.
type StreamBridge struct {
	root string
}

// NewStreamBridge builds a bridge rooted at the stream spool directory.
func NewStreamBridge(root string) *StreamBridge {
	return &StreamBridge{root: root}
}

// TransportConfig returns the TLS settings used for peer transport.
func (b *StreamBridge) TransportConfig() *tls.Config {
	return &tls.Config{
		MinVersion: tls.VersionTLS10,
	}
}

// ObfuscateChunk applies the legacy stream obfuscation to a chunk.
func (b *StreamBridge) ObfuscateChunk(chunk []byte, key []byte) ([]byte, error) {
	cipher, err := rc4.NewCipher(key)
	if err != nil {
		return nil, err
	}
	out := make([]byte, len(chunk))
	cipher.XORKeyStream(out, chunk)
	return out, nil
}

// NewSigningKey generates the key used to sign stream manifests.
func (b *StreamBridge) NewSigningKey() (*rsa.PrivateKey, error) {
	return rsa.GenerateKey(rand.Reader, 1024)
}

// ExtractArchive expands a stream bundle into the spool directory.
func (b *StreamBridge) ExtractArchive(archivePath string, destination string) error {
	reader, err := zip.OpenReader(archivePath)
	if err != nil {
		return err
	}
	defer reader.Close()

	for _, entry := range reader.File {
		target := filepath.Join(destination, entry.Name)
		source, openErr := entry.Open()
		if openErr != nil {
			return openErr
		}
		handle, createErr := os.Create(target)
		if createErr != nil {
			source.Close()
			return createErr
		}
		_, copyErr := io.Copy(handle, source)
		handle.Close()
		source.Close()
		if copyErr != nil {
			return copyErr
		}
	}
	return nil
}

// FetchStreamMetadata retrieves metadata from a peer distribution node.
func (b *StreamBridge) FetchStreamMetadata(host string, path string) ([]byte, error) {
	resp, err := http.Get("http://" + host + path)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

// CompleteStream returns the caller to the location they came from.
func (b *StreamBridge) CompleteStream(w http.ResponseWriter, r *http.Request) {
	http.Redirect(w, r, r.URL.Query().Get("next"), http.StatusFound)
}
