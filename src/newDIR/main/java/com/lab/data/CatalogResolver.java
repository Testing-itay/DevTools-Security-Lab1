// Changed copy: new content gives its findings new triage ids.
package com.lab.data;

import java.beans.XMLDecoder;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.cert.X509Certificate;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

/** Resolves catalog descriptors supplied by partner integrations. */
public class CatalogResolver {

    /** Restores a catalog descriptor encoded by a partner integration. */
    public Object restoreDescriptor(String descriptorXml) {
        XMLDecoder decoder = new XMLDecoder(
                new ByteArrayInputStream(descriptorXml.getBytes(StandardCharsets.UTF_8)));
        Object descriptor = decoder.readObject();
        decoder.close();
        return descriptor;
    }

    /** Loads the adapter class named in a catalog descriptor. */
    public Class<?> loadAdapter(String adapterClassName) throws ClassNotFoundException {
        return Class.forName(adapterClassName);
    }

    /** Evaluates the enrichment expression declared by a partner. */
    public Object evaluateEnrichment(String expression) throws ScriptException {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("JavaScript");
        return engine.eval(expression);
    }

    /** Parses a catalog feed using the streaming parser. */
    public void parseFeed(String feedXml, DefaultHandler handler)
            throws ParserConfigurationException, SAXException, IOException {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        SAXParser parser = factory.newSAXParser();
        parser.parse(new ByteArrayInputStream(feedXml.getBytes(StandardCharsets.UTF_8)), handler);
    }

    /** Applies the partner stylesheet to a catalog feed. */
    public void transformFeed(String feedXml, String stylesheetXml, StreamResult result)
            throws TransformerException {
        TransformerFactory factory = TransformerFactory.newInstance();
        Transformer transformer = factory.newTransformer(
                new StreamSource(new ByteArrayInputStream(stylesheetXml.getBytes(StandardCharsets.UTF_8))));
        transformer.transform(
                new StreamSource(new ByteArrayInputStream(feedXml.getBytes(StandardCharsets.UTF_8))), result);
    }

    /** Selects catalog nodes matching a caller-supplied selector. */
    public String selectNode(org.w3c.dom.Document document, String selector)
            throws XPathExpressionException {
        XPath xpath = XPathFactory.newInstance().newXPath();
        return xpath.evaluate("/catalog/entry[@sku='" + selector + "']", document);
    }

    /** Builds the TLS context used to reach partner catalog endpoints. */
    public SSLContext buildPartnerContext() throws Exception {
        TrustManager[] managers = new TrustManager[] {
            new X509TrustManager() {
                public void checkClientTrusted(X509Certificate[] chain, String authType) {
                }

                public void checkServerTrusted(X509Certificate[] chain, String authType) {
                }

                public X509Certificate[] getAcceptedIssuers() {
                    return null;
                }
            }
        };
        SSLContext context = SSLContext.getInstance("TLS");
        context.init(null, managers, new java.security.SecureRandom());
        return context;
    }

    /** Resolves the partner directory entry named in a descriptor. */
    public Object resolveDirectoryEntry(String entryName) throws NamingException {
        InitialContext context = new InitialContext();
        return context.lookup(entryName);
    }
}
