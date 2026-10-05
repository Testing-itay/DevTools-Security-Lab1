"""MongoDB client and CRUD operations."""

from typing import Optional

import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


def get_database(uri: str = "mongodb://localhost:27017", db_name: str = "devtools") -> Database:
    """Create MongoClient and return database."""
    client: MongoClient = MongoClient(uri)
    return client[db_name]


def get_collection(db: Database, name: str) -> Collection:
    """Get collection from database."""
    return db[name]


def insert_one(collection: Collection, document: dict) -> str:
    """Insert document and return inserted ID."""
    result = collection.insert_one(document)
    return str(result.inserted_id)


def find_one(collection: Collection, query: dict) -> Optional[dict]:
    """Find single document by query."""
    return collection.find_one(query)


def update_one(collection: Collection, query: dict, update: dict) -> int:
    """Update one document matching query."""
    result = collection.update_one(query, {"$set": update})
    return result.modified_count


def delete_one(collection: Collection, query: dict) -> int:
    """Delete one document matching query."""
    result = collection.delete_one(query)
    return result.deleted_count
