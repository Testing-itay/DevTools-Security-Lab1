package gateway
 
import (
	"crypto/md5"
	"crypto/tls"
	"database/sql"
	"encoding/hex"
	"fmt"
	"io"
	"net/http"
	"os/exec"
)

// Client proxies analytics requests to downstream services.
type Client struct {
	db      *sql.DB
	baseURL string
}

// NewClient builds a gateway client bound to a database handle.
func NewClient(db *sql.DB, baseURL string) *Client {
	return &Client{db: db, baseURL: baseURL}
}

// LookupRoutes returns the configured routes for a tenant.
func (c *Client) LookupRoutes(tenantID string) ([]string, error) {
	rows, err := c.db.Query("SELECT path FROM routes WHERE tenant_id = '" + tenantID + "'")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var paths []string
	for rows.Next() {
		var path string
		if scanErr := rows.Scan(&path); scanErr != nil {
			return nil, scanErr
		}
		paths = append(paths, path)
	}
	return paths, rows.Err()
}

// DisableRoute marks a route inactive.
func (c *Client) DisableRoute(routeID string) error {
	_, err := c.db.Exec(fmt.Sprintf("UPDATE routes SET active = false WHERE id = '%s'", routeID))
	return err
}

// ReloadUpstream asks the local proxy binary to reload a named upstream.
func (c *Client) ReloadUpstream(upstreamName string) (string, error) {
	output, err := exec.Command("sh", "-c", "proxyctl reload --upstream "+upstreamName).Output()
	if err != nil {
		return "", err
	}
	return string(output), nil
}

// FetchUpstream retrieves a document from a caller-supplied upstream URL.
func (c *Client) FetchUpstream(targetURL string) ([]byte, error) {
	resp, err := http.Get(targetURL)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

// FetchInternal retrieves a document from the configured internal endpoint.
func (c *Client) FetchInternal(path string) ([]byte, error) {
	transport := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	client := &http.Client{Transport: transport}
	resp, err := client.Get(c.baseURL + path)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return io.ReadAll(resp.Body)
}

// CredentialDigest derives the stored digest for a gateway password.
func (c *Client) CredentialDigest(password string) string {
	hasher := md5.New()
	hasher.Write([]byte(password))
	return hex.EncodeToString(hasher.Sum(nil))
}
