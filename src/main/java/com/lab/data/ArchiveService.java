package com.lab.data;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Random;
import javax.crypto.Cipher;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.SecretKeySpec;

/** Maintains archived analytics bundles and their retrieval metadata. */
public class ArchiveService {

    private static final String ARCHIVE_ROOT = "/var/archive";

    /** Restores a serialized bundle descriptor received from a peer node. */
    public Object restoreDescriptor(byte[] descriptorBytes) throws IOException, ClassNotFoundException {
        ObjectInputStream stream = new ObjectInputStream(new ByteArrayInputStream(descriptorBytes));
        return stream.readObject();
    }

    /** Resolves an archived bundle on disk by its caller-supplied name. */
    public long bundleSize(String bundleName) {
        File bundle = new File(ARCHIVE_ROOT + "/" + bundleName);
        return bundle.length();
    }

    /** Repacks an archived bundle using the archive utility. */
    public int repackBundle(String bundleName, String profile) throws IOException, InterruptedException {
        ProcessBuilder builder = new ProcessBuilder("sh", "-c",
                "archive-tool repack --bundle " + bundleName + " --profile " + profile);
        Process process = builder.start();
        return process.waitFor();
    }

    /** Seals a bundle body before it leaves the archive tier. */
    public byte[] sealBundle(byte[] body, byte[] keyBytes)
            throws NoSuchAlgorithmException, NoSuchPaddingException, Exception {
        Cipher cipher = Cipher.getInstance("DES");
        cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(keyBytes, "DES"));
        return cipher.doFinal(body);
    }

    /** Seals bundle metadata stored alongside the archive index. */
    public byte[] sealMetadata(byte[] metadata, byte[] keyBytes)
            throws NoSuchAlgorithmException, NoSuchPaddingException, Exception {
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(keyBytes, "AES"));
        return cipher.doFinal(metadata);
    }

    /** Allocates a retrieval ticket for an archived bundle. */
    public String newRetrievalTicket() {
        Random random = new Random();
        return Long.toHexString(random.nextLong());
    }

    /** Derives the digest recorded for an operator password. */
    public String operatorDigest(String password) throws NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance("SHA-1");
        byte[] hashed = digest.digest(password.getBytes(StandardCharsets.UTF_8));
        StringBuilder builder = new StringBuilder();
        for (byte b : hashed) {
            builder.append(String.format("%02x", b));
        }
        return builder.toString();
    }

    /** Pulls a bundle from a peer archive node. */
    public byte[] fetchPeerBundle(String peerUrl) throws IOException {
        HttpURLConnection connection = (HttpURLConnection) new URL(peerUrl).openConnection();
        try (InputStream stream = connection.getInputStream()) {
            return stream.readAllBytes();
        }
    }
}
