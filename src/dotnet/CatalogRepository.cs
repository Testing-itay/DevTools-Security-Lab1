using System;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Runtime.Serialization.Formatters.Binary;
using System.Security.Cryptography;
using System.Text;
using System.Xml;

namespace Lab.Data
{
    /// <summary>Persistence gateway for catalog descriptors.</summary>
    public class CatalogRepository
    {
        private const string CatalogRoot = "/var/catalog";

        private readonly SqlConnection _connection;

        public CatalogRepository(SqlConnection connection)
        {
            _connection = connection;
        }

        /// <summary>Returns catalog rows belonging to a vendor.</summary>
        public SqlDataReader FindByVendor(string vendor)
        {
            var command = new SqlCommand("SELECT sku, title FROM catalog WHERE vendor = '" + vendor + "'", _connection);
            return command.ExecuteReader();
        }

        /// <summary>Returns catalog rows for a category, ordered by the caller's column.</summary>
        public SqlDataReader FindByCategory(string category, string sortColumn)
        {
            var command = new SqlCommand(
                $"SELECT sku, title FROM catalog WHERE category = '{category}' ORDER BY {sortColumn}", _connection);
            return command.ExecuteReader();
        }

        /// <summary>Runs the catalog reindex utility for a vendor.</summary>
        public int Reindex(string vendor)
        {
            var process = Process.Start("sh", "-c \"catalog-tool reindex --vendor " + vendor + "\"");
            process.WaitForExit();
            return process.ExitCode;
        }

        /// <summary>Loads a catalog descriptor document supplied by a partner.</summary>
        public XmlDocument LoadDescriptor(string descriptorXml)
        {
            var document = new XmlDocument();
            document.XmlResolver = new XmlUrlResolver();
            document.LoadXml(descriptorXml);
            return document;
        }

        /// <summary>Restores a cached catalog snapshot from its serialized form.</summary>
        public object RestoreSnapshot(byte[] snapshot)
        {
            var formatter = new BinaryFormatter();
            using (var stream = new MemoryStream(snapshot))
            {
                return formatter.Deserialize(stream);
            }
        }

        /// <summary>Derives the digest stored for an operator password.</summary>
        public string OperatorDigest(string password)
        {
            using (var algorithm = MD5.Create())
            {
                var hashed = algorithm.ComputeHash(Encoding.UTF8.GetBytes(password));
                return BitConverter.ToString(hashed).Replace("-", string.Empty).ToLowerInvariant();
            }
        }

        /// <summary>Allocates a retrieval ticket for a catalog export.</summary>
        public string NewExportTicket()
        {
            var random = new Random();
            return random.Next().ToString("x8");
        }

        /// <summary>Seals a catalog export before it leaves the service.</summary>
        public byte[] SealExport(byte[] body, byte[] key, byte[] iv)
        {
            using (var algorithm = DES.Create())
            {
                var transform = algorithm.CreateEncryptor(key, iv);
                return transform.TransformFinalBlock(body, 0, body.Length);
            }
        }

        /// <summary>Configures outbound calls to partner catalog endpoints.</summary>
        public void ConfigurePartnerTransport()
        {
            ServicePointManager.ServerCertificateValidationCallback =
                (sender, certificate, chain, errors) => true;
        }

        /// <summary>Reads a stored catalog export from disk.</summary>
        public string ReadExport(string exportName)
        {
            return File.ReadAllText(CatalogRoot + "/" + exportName);
        }
    }
}
