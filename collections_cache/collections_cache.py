import pickle
import sqlite3
from random import choice
from itertools import chain
from os import cpu_count, path, makedirs, scandir
from concurrent.futures import ProcessPoolExecutor as Pool
from concurrent.futures import ThreadPoolExecutor as Thread

class Collection_Cache:
    def __init__(self, collection_name):
        # Variables
        self.collection_name        = collection_name
        self.cpu_cores              = cpu_count()
        self.collection_dir         = path.join("./Collections", self.collection_name)
        self.databases_list         = []
        self.keys_databases         = {}
        # Init methods
        self.create_collection()
        self.get_all_databases()

    def create_collection(self):
        makedirs(self.collection_dir, exist_ok=True)
        for core in range(self.cpu_cores):
            db_path = path.join(self.collection_dir, f"database_{core}.db")
            self.initialize_databases(db_path)

    def initialize_databases(self, db_path):
        conn = sqlite3.connect(db_path)
        self.configure_connection(conn)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS data(
                key     TEXT,
                value   BLOB
            );
        """)
        conn.close()

    def get_all_databases(self):
        with scandir(self.collection_dir) as contents:
            self.databases_list = [path.join(self.collection_dir, content.name) for content in contents]
        with Pool(self.cpu_cores) as pool:
            self.keys_databases = dict(chain.from_iterable(pool.map(self.get_all_keys, self.databases_list)))

    def get_all_keys(self, database):
        conn    = sqlite3.connect(database)
        self.configure_connection(conn)
        cursor  = conn.cursor()
        cursor.execute("SELECT key FROM data;")
        result  = cursor.fetchall()
        keys    = [(line[0], database) for line in result]
        conn.close()
        return keys

    def set_key(self, key: str, value: any):
        """Used to store values and associate a value with a key."""
        if key not in self.keys_databases:
            database_to_insert = choice(self.databases_list)
            conn = sqlite3.connect(database_to_insert)
            self.configure_connection(conn)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO data(key, value) VALUES (?, ?);", (key, pickle.dumps(value)))
            conn.commit()
            conn.close()
            self.add_to_keys_database(key, database_to_insert)
        else:
            database_to_update = self.keys_databases[key]
            conn = sqlite3.connect(database_to_update)
            self.configure_connection(conn)
            cursor = conn.cursor()
            cursor.execute("UPDATE data SET value = ? WHERE key = ?;", (pickle.dumps(value), key))
            conn.commit()
            conn.close()

    def set_multi_keys(self, keys_and_values: dict[str, any]):
        """Experimental. Set multiple keys and values at the same time."""
        with Thread(self.cpu_cores) as thread:
            thread.map(lambda kv: self.set_key(kv[0], kv[1]), keys_and_values.items())

    def add_to_keys_database(self, key, database):
        self.keys_databases[key] = database

    def delete_to_keys_database(self, key):
        """Removes the key from the dictionary of stored keys"""
        if key in self.keys_databases:
            del self.keys_databases[key]

    def get_key(self, key: str):
        """Used to obtain the value stored by the key"""
        try:
            database_to_search = self.keys_databases[key]
            conn = sqlite3.connect(database_to_search)
            self.configure_connection(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM data WHERE key = ?", (key,))
            result = cursor.fetchall()
            conn.close()
            return pickle.loads(result[0][0])
        except Exception as error:
            return error

    def delete_key(self, key: str):
        """Used to delete the value stored by the key"""
        try:
            database_to_delete = self.keys_databases[key]
            conn = sqlite3.connect(database_to_delete)
            self.configure_connection(conn)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM data WHERE key = ?", (key,))
            conn.commit()
            conn.close()
            self.delete_to_keys_database(key)
        except KeyError:
            return f"Key '{key}' not found."
        except Exception as error:
            return error

    def configure_connection(self, conn):
        conn.execute("PRAGMA auto_vacuum = FULL;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA wal_autocheckpoint = 1000;")
        conn.execute("PRAGMA cache_size = -2000;")
        conn.execute("PRAGMA temp_store = MEMORY;")
        conn.execute("PRAGMA optimize;")

    def keys(self):
        """Returns all stored keys"""
        return list(self.keys_databases.keys())

    def export_to_json(self):
        """Test"""
        pass
