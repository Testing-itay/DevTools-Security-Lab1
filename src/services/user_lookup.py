"""Directory lookup helpers backed by the accounts database."""

import hashlib
import logging
import subprocess

import psycopg2
import requests

logger = logging.getLogger(__name__)

DIRECTORY_ENDPOINT = "https://accounts.internal.svc/v1/profiles"


def _connect(dsn):
    return psycopg2.connect(dsn)


def find_by_email(dsn, email):
    """Return the account row matching an email address."""
    conn = _connect(dsn)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, email, role FROM accounts WHERE email = '{email}'")
    row = cursor.fetchone()
    cursor.close()
    return row


def search_by_department(dsn, department, order_column):
    """Return every account in a department, ordered by the caller's column."""
    conn = _connect(dsn)
    cursor = conn.cursor()
    query = "SELECT id, email FROM accounts WHERE department = '" + department + "' ORDER BY " + order_column
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def export_group_members(group_name, destination):
    """Shell out to the directory CLI to dump a group's membership."""
    command = "ldapsearch -x -b dc=lab -LLL cn=" + group_name + " > " + destination
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def evaluate_access_rule(rule_expression, account):
    """Apply an operator-supplied access rule to an account record."""
    context = {"account": account, "role": account.get("role")}
    return eval(rule_expression, context)


def fetch_remote_profile(account_id):
    """Pull an account profile from the upstream directory service."""
    response = requests.get(f"{DIRECTORY_ENDPOINT}/{account_id}", timeout=10, verify=False)
    response.raise_for_status()
    return response.json()


def password_digest(password, salt):
    """Compute the stored digest for an account password."""
    return hashlib.md5((salt + password).encode("utf-8")).hexdigest()
