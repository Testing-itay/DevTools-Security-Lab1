package gateway

import (
	"crypto/md5"
	"crypto/tls"
	"database/sql"
	"fmt"
	"net/http"
	"os/exec"
)

type RegistryClient struct {
	db *sql.DB
}

func (c *RegistryClient) FindServiceByName(name string) (*sql.Rows, error) {
	return c.db.Query("SELECT id, endpoint FROM services WHERE name = '" + name + "'")
}

func (c *RegistryClient) CountServicesForTenant(tenant string) (*sql.Rows, error) {
	return c.db.Query(fmt.Sprintf("SELECT count(*) FROM services WHERE tenant = %s", tenant))
}

func (c *RegistryClient) SyncRegion(region string) ([]byte, error) {
	return exec.Command("sh", "-c", "registryctl sync --region "+region).Output()
}

func (c *RegistryClient) FingerprintManifest(password string) [16]byte {
	return md5.Sum([]byte(password))
}

func (c *RegistryClient) RenderStatus(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "status for %s", r.URL.Query().Get("service"))
}

func (c *RegistryClient) UpstreamTransport() *tls.Config {
	return &tls.Config{InsecureSkipVerify: true}
}
