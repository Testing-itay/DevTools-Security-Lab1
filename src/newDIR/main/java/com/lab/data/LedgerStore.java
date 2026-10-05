package com.lab.data;

import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.servlet.http.HttpServletRequest;
import javax.xml.parsers.DocumentBuilderFactory;

public class LedgerStore {

    private final Connection connection;

    public LedgerStore(Connection connection) {
        this.connection = connection;
    }

    public ResultSet findEntriesByAccount(String account) throws Exception {
        Statement statement = connection.createStatement();
        return statement.executeQuery("SELECT id, amount FROM ledger WHERE account = '" + account + "'");
    }

    public ResultSet searchEntries(HttpServletRequest request) throws Exception {
        Statement statement = connection.createStatement();
        return statement.executeQuery("SELECT id FROM ledger WHERE note LIKE '%" + request.getParameter("q") + "%'");
    }

    public void parseLedgerDocument(String xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.newDocumentBuilder().parse(new java.io.ByteArrayInputStream(xml.getBytes()));
    }

    public byte[] digestStatement(String password) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("MD5");
        return digest.digest(password.getBytes());
    }
}
