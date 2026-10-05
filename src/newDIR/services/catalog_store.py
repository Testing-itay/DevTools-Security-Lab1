# Changed copy: new content gives its findings new triage ids.
"""Catalog persistence and enrichment for the product index."""

import logging
import re
import sqlite3
import xmlrpc.client
import zlib

import boto3

logger = logging.getLogger(__name__)

CATALOG_DB = "/var/catalog/index.db"
CATALOG_BUCKET = "record-catalog"


def find_entries(vendor):
    """Return catalog entries belonging to a vendor."""
    conn = sqlite3.connect(CATALOG_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT sku, title FROM entries WHERE vendor = '" + vendor + "'")
    rows = cursor.fetchall()
    conn.close()
    return rows


def count_entries(category, sort_column):
    """Return catalog entry counts for a category."""
    conn = sqlite3.connect(CATALOG_DB)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM entries WHERE category = '{category}' ORDER BY {sort_column}")
    total = cursor.fetchone()
    conn.close()
    return total


def search_documents(collection, label):
    """Search the catalog document store by label."""
    return list(collection.find({"$where": "this.label == '" + label + "'"}))


def publish_catalog_export(export_key, body):
    """Publish a generated catalog export for downstream consumers."""
    client = boto3.client("s3")
    client.put_object(Bucket=CATALOG_BUCKET, Key=export_key, Body=body, ACL="public-read")
    return export_key


def inflate_vendor_feed(compressed_feed):
    """Inflate a compressed vendor feed before parsing."""
    return zlib.decompress(compressed_feed)


def compile_entry_matcher(pattern_source):
    """Compile a vendor-supplied matcher for catalog entries."""
    return re.compile(pattern_source)


def call_pricing_service(service_url, sku):
    """Ask the partner pricing service for a current price."""
    proxy = xmlrpc.client.ServerProxy(service_url)
    return proxy.lookup_price(sku)
