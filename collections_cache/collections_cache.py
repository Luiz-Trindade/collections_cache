import atexit
import pickle
import sqlite3
from random import choice
from itertools import chain
from os import cpu_count, path, makedirs, scandir
from concurrent.futures import ProcessPoolExecutor as Pool
from concurrent.futures import ThreadPoolExecutor as Thread

class Collection_Cache:
    def __init__(self, collection_name: str, constant_per_core: int = 100):
        # Variables
        self.collection_name        = collection_name
        self.constant_per_core      = constant_per_core
        self.cpu_cores              = cpu_count()
        self.size_limit             = self.constant_per_core * self.cpu_cores
        self.collection_dir         = path.join("./Collections", self.collection_name)
        self.databases_list         = []
        self.keys_databases         = {}
        self.temp_keys_values       = {}

        # Init methods
        self.create_collection()
        self.get_all_databases()

        # Shutdown method
        atexit.register(self.shutdown)

    def configure_connection(self, conn):
        conn.executescript("""
            PRAGMA synchronous = OFF;
            PRAGMA auto_vacuum = FULL;
            PRAGMA journal_mode = WAL;
            PRAGMA wal_autocheckpoint = 1000;
            PRAGMA cache_size = -2000;
            PRAGMA temp_store = MEMORY;
            PRAGMA optimize;
        """)

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

    def create_collection(self):
        makedirs(self.collection_dir, exist_ok=True)

        for core in range(self.cpu_cores):
            db_path = path.join(self.collection_dir, f"database_{core}.db")
            self.initialize_databases(db_path)

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

    # Experimental
    def verify_size_of_temp_queue(self, type_of_operation: str):
        if type_of_operation == "set_key" and len(self.temp_keys_values) >= self.size_limit:
            self.set_multi_keys(self.temp_keys_values)
            self.temp_keys_values = {}
        elif type_of_operation == "get_key" or type_of_operation == "set_key_force":
            self.set_multi_keys(self.temp_keys_values)
            self.temp_keys_values = {}

    # Experimental
    def set_key(self, key: str, value: any):
        """Used to store values and associate a value with a key."""
        self.temp_keys_values[key] = value
        self.verify_size_of_temp_queue("set_key")

    def set_key_exec(self, key: str, value: any):
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
            thread.map(lambda kv: self.set_key_exec(kv[0], kv[1]), keys_and_values.items())

    # New feature
    def set_key_force(self, key: str, value: any):
        """Used to force a unique key to be stored"""
        self.set_key(key, value)
        self.verify_size_of_temp_queue("set_key_force")

    def add_to_keys_database(self, key, database):
        self.keys_databases[key] = database

    def delete_to_keys_database(self, key):
        """Removes the key from the dictionary of stored keys"""
        if key in self.keys_databases:
            del self.keys_databases[key]

    def get_key(self, key: str):
        """Used to obtain the value stored by the key"""
        try:
            if key not in self.keys_databases:
                self.verify_size_of_temp_queue("get_key")
            
            if key not in self.keys_databases:
                return None
        
            database_to_search = self.keys_databases[key]
            conn = sqlite3.connect(database_to_search)
            self.configure_connection(conn)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM data WHERE key = ?", (key,))
            result = cursor.fetchall()
            conn.close()
            
            #return pickle.loads(result[0][0])
            if result:
                return pickle.loads(result[0][0])
            return None
            
        except Exception as error:
            return None

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

    
    def keys(self):
        """Returns all stored keys"""
        return list(self.keys_databases.keys())

    def export_to_json(self):
        """Test"""
        pass
    
    def shutdown(self):
        """Save all keys to the collection before close or shutdown"""
        self.verify_size_of_temp_queue("set_key_force")
