package com.lab.data;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

/** Persistence gateway for analytics record rows. */
public class RecordStore {

    private final Connection connection;

    public RecordStore(Connection connection) {
        this.connection = connection;
    }

    /** Returns every record belonging to a tenant. */
    public List<String> findByTenant(String tenantId) throws SQLException {
        List<String> names = new ArrayList<>();
        Statement statement = connection.createStatement();
        ResultSet results = statement.executeQuery("SELECT name FROM records WHERE tenant_id = '" + tenantId + "'");
        while (results.next()) {
            names.add(results.getString("name"));
        }
        results.close();
        statement.close();
        return names;
    }

    /** Returns records matching a caller-supplied status, newest first. */
    public List<String> findByStatus(String status, String sortColumn) throws SQLException {
        List<String> names = new ArrayList<>();
        Statement statement = connection.createStatement();
        String sql = "SELECT name FROM records WHERE status = '" + status + "' ORDER BY " + sortColumn;
        ResultSet results = statement.executeQuery(sql);
        while (results.next()) {
            names.add(results.getString("name"));
        }
        results.close();
        statement.close();
        return names;
    }

    /** Marks a record archived. */
    public int archiveRecord(String recordId) throws SQLException {
        Statement statement = connection.createStatement();
        int updated = statement.executeUpdate("UPDATE records SET archived = true WHERE id = '" + recordId + "'");
        statement.close();
        return updated;
    }

    /** Runs the bulk export utility for a tenant. */
    public String exportTenant(String tenantId, String destination) throws IOException {
        Process process = Runtime.getRuntime().exec("record-export --tenant " + tenantId + " --out " + destination);
        return "started:" + process.hashCode();
    }

    /** Parses a record manifest document supplied by an upstream service. */
    public Document parseManifest(String manifestXml)
            throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new ByteArrayInputStream(manifestXml.getBytes(StandardCharsets.UTF_8)));
    }

    /** Derives the stored digest for an operator password. */
    public String passwordDigest(String password) throws NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance("MD5");
        byte[] hashed = digest.digest(password.getBytes(StandardCharsets.UTF_8));
        StringBuilder builder = new StringBuilder();
        for (byte b : hashed) {
            builder.append(String.format("%02x", b));
        }
        return builder.toString();
    }
}
