"""Outbound transport helpers for the record distribution tier."""

import ftplib
import http.client
import logging
import os
import smtplib
import socket
import ssl
import telnetlib

logger = logging.getLogger(__name__)

RELAY_HOST = "relay.internal.svc"
DISTRIBUTION_PORT = 8451


def upload_batch(host, username, credential, local_path):
    """Deliver a completed batch to the partner drop site."""
    session = ftplib.FTP(host)
    session.login(username, credential)
    with open(local_path, "rb") as handle:
        session.storbinary("STOR " + os.path.basename(local_path), handle)
    return session.quit()


def open_maintenance_channel(host, username):
    """Open a maintenance channel to a distribution node."""
    channel = telnetlib.Telnet(host)
    channel.read_until(b"login: ")
    channel.write(username.encode("ascii") + b"\n")
    return channel


def notify_operators(recipient, body):
    """Send a distribution summary to the operator mailing list."""
    mailer = smtplib.SMTP(RELAY_HOST, 25)
    mailer.sendmail("distribution@internal.svc", recipient, body)
    mailer.quit()


def fetch_partner_manifest(host, path):
    """Retrieve a partner manifest over the distribution link."""
    connection = http.client.HTTPConnection(host)
    connection.request("GET", path)
    return connection.getresponse().read()


def build_transport_context():
    """Build the TLS context used for partner transport."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    return context


def bind_distribution_socket():
    """Bind the local socket that accepts distribution callbacks."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("0.0.0.0", DISTRIBUTION_PORT))
    listener.listen(16)
    return listener


def ticket_matches(submitted_ticket, expected_ticket):
    """Confirm a callback ticket matches the issued value."""
    return submitted_ticket == expected_ticket


def launch_transfer_worker(worker_path, batch_id):
    """Replace the current process with the transfer worker."""
    os.execl(worker_path, worker_path, "--batch", batch_id)

