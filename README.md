# collections-cache 🚀

`collections-cache` is a fast and scalable key–value caching solution built on top of SQLite. It allows you to store, update, and retrieve data using unique keys, and it supports complex Python data types (thanks to `pickle`). Designed to harness the power of multiple CPU cores, the library shards data across multiple SQLite databases, enabling impressive performance scaling.

---

## Features ✨

- **Multiple SQLite Databases**: Distributes your data across several databases to optimize I/O and take advantage of multi-core systems.
- **Key–Value Store**: Simple and intuitive interface for storing and retrieving data.
- **Supports Complex Data Types**: Serialize and store lists, dictionaries, objects, and more using `pickle`.
- **Parallel Processing**: Uses Python’s `multiprocessing` and `concurrent.futures` modules to perform operations in parallel.
- **Efficient Data Retrieval**: Caches all keys in memory for super-fast lookups.
- **Cross-Platform**: Runs on Linux, macOS, and Windows.
- **Performance Scaling**: Benchmarks show near-linear scaling with the number of real CPU cores.

---

## Installation 📦

Use [Poetry](https://python-poetry.org/) to install and manage dependencies:

1. Clone the repository:

    ```bash
    git clone https://github.com/Luiz-Trindade/collections_cache.git
    cd collections-cache
    ```

2. Install the package with Poetry:

    ```bash
    poetry install
    ```

---

## Usage ⚙️

Simply import and start using the main class, `Collection_Cache`, to interact with your collection:

### Basic Example

```python
from collections_cache import Collection_Cache

# Create a new collection named "STORE"
cache = Collection_Cache("STORE")

# Set a key-value pair
cache.set_key("products", ["apple", "orange", "onion"])

# Retrieve the value by key
products = cache.get_key("products")
print(products)  # Output: ['apple', 'orange', 'onion']
```

### Bulk Insertion Example

For faster insertions, accumulate your data and use `set_multi_keys`:

```python
from collections_cache import Collection_Cache
from random import uniform, randint
from time import time

cache = Collection_Cache("web_cache")
insertions = 100_000
data = {}

# Generate data
for i in range(insertions):
    key = str(uniform(0.0, 100.0))
    value = "some text :)" * randint(1, 100)
    data[key] = value

# Bulk insert keys using multi-threaded execution
cache.set_multi_keys(data)

print(f"Inserted {len(cache.keys())} keys successfully!")
```

---

## API Overview 📚

- **`set_key(key, value)`**: Stores a key–value pair. Updates the value if the key already exists.
- **`set_multi_keys(key_and_value)`**: (Experimental) Inserts multiple key–value pairs in parallel.
- **`get_key(key)`**: Retrieves the value associated with a given key.
- **`delete_key(key)`**: Removes a key and its corresponding value.
- **`keys()`**: Returns a list of all stored keys.
- **`export_to_json()`**: (Future feature) Exports your collection to a JSON file.

---

## Performance Benchmark 📊

On a machine with 4 real CPU cores, benchmarks indicate around **781 insertions per second**. The library is designed to scale nearly linearly with the number of real cores. For example:
- **6 cores**: ~1,171 insertions per second.
- **16 cores**: ~3,125 insertions per second.
- **128 cores**: ~25,000 insertions per second (theoretically).

*Note: Actual performance will depend on disk I/O, SQLite contention, and system architecture.*

---

## Development & Contributing 👩‍💻👨‍💻

To contribute or run tests:

1. Install development dependencies:

    ```bash
    poetry install --dev
    ```

2. Run tests using:

    ```bash
    poetry run pytest
    ```

Feel free to submit issues, pull requests, or feature suggestions. Your contributions help make `collections-cache` even better!

---

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements 🙌

- Inspired by the need for efficient, multi-core caching with SQLite.
- Created by Luiz Trindade.
- Thanks to all contributors and users who provide feedback to keep improving the library!

---

Give `collections-cache` a try and let it power your high-performance caching needs! 🚀
