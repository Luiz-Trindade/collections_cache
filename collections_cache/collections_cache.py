import sqlite3
from multiprocessing import Pool
from os import cpu_count, path, makedirs, scandir
from itertools import chain
from random import choice
import pickle

class Collection_Cache:
    def __init__(self, collection_name):
        self.collection_name        = collection_name
        self.cpu_cores              = cpu_count()
        self.collection_dir         = path.join("./Collections", self.collection_name)
        self.databases_list         = []
        self.keys_databases         = {}

        #print(f"Collection '{self.collection_name}' created!")
        #print(f"Number of cpu cores: {self.cpu_cores}")
        self.create_collection()
        self.get_all_databases()

    def create_collection(self):
        makedirs(self.collection_dir, exist_ok=True)
        
        for core in range(self.cpu_cores):
            db_path = path.join(self.collection_dir, f"database_{core}.db")
            self.initialize_databases(db_path)

    def initialize_databases(self, db_path):
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS data(
                key     TEXT,
                value   BLOB
            );
        """)
        conn.close()

    def get_all_databases(self):
        #print("Obtaining all keys...")
        with scandir(self.collection_dir) as contents:
            self.databases_list = [path.join(self.collection_dir, content.name) for content in contents]
            
        with Pool(self.cpu_cores) as pool:
            self.keys_databases = dict(chain.from_iterable(pool.map(self.get_all_keys, self.databases_list)))
        #print(self.keys_databases)

    def get_all_keys(self, database):
        conn    = sqlite3.connect(database)
        cursor  = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("SELECT key FROM data;")
        result  = cursor.fetchall()
        keys    = [(line[0], database) for line in result]
        conn.close()
        return keys

    def set_key(self, key, value):
        if key not in self.keys_databases:
            database_to_insert = choice(self.databases_list)
            #print(f"Inserting in {database_to_insert}")
            conn = sqlite3.connect(database_to_insert)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("INSERT INTO data(key, value) VALUES (?, ?);", (key, pickle.dumps(value)))
            conn.commit()
            conn.close()
            self.add_to_keys_database(key, database_to_insert)

        else:
            #print(f"Updating key '{key}' in {self.keys_databases[key]}...")
            database_to_update = self.keys_databases[key]
            conn = sqlite3.connect(database_to_update)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("UPDATE data SET value = ? WHERE key = ?;", (pickle.dumps(value), key))
            conn.commit()
            conn.close()
            #print(f"Key '{key}' updated successfully in {database_to_update}")

    def add_to_keys_database(self, key, database):
        self.keys_databases[key] = database
        #print(self.keys_databases)

    def get_key(self, key):
        try:
            database_to_search = self.keys_databases[key]
            #print(database_to_search)

            conn = sqlite3.connect(database_to_search)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("SELECT value FROM data WHERE key = ?", (key,))
            result = cursor.fetchall()
            conn.close()
            return pickle.loads(result[0][0])
            
        except Exception as error:
            return error
