# collections-cache

`collections-cache` is a simple and efficient caching solution built using SQLite databases. It allows for storing, updating, and retrieving data using unique keys, supporting complex data types through the use of `pickle`. It is designed to scale across multiple CPU cores by distributing the data across multiple SQLite databases.

## Features

- **Multiple SQLite databases**: Distributes data across multiple databases for better scalability.
- **Key-value store**: Store data as key-value pairs.
- **Supports complex data types**: Data is serialized using `pickle`, so you can store lists, dictionaries, and other complex Python objects.
- **Parallel processing**: Uses Python’s `multiprocessing` to handle large collections in parallel across multiple CPU cores.
- **Efficient data retrieval**: Retrieves stored data based on the key using an efficient search across the collection.

## Installation

To install the `collections-cache` package, use [Poetry](https://python-poetry.org/) for managing dependencies.

1. Clone the repository:

    ```bash
    git clone https://github.com/Luiz-Trindade/collections_cache.git
    cd collection-cache
    ```

2. Install the package with Poetry:

    ```bash
    poetry install
    ```

## Usage

To use the `collections-cache` package, you can import the main class `Collection_Cache` and interact with your collection.

### Example:

```python
from collections_cache import Collection_Cache

# Create a new collection
cache = Collection_Cache("STORE")

# Set a key-value pair
cache.set_key("products", ["apple", "orange", "onion"])

# Get the value by key
students = cache.get_key("alunos")
print(students)  # Output: ['Luiz', 'Marcos', 'João']
```

### Methods:

- **`set_key(key, value)`**: Set a key-value pair in the cache. If the key already exists, it will be updated.
- **`get_key(key)`**: Retrieve the value associated with a key.
- **`delete_key(key)`**: Delete an existing key.

## Development

To contribute or run tests:

1. Install development dependencies:

    ```bash
    poetry install --dev
    ```

2. Run tests:

    ```bash
    poetry run pytest
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This package was created to demonstrate how to work with SQLite, `pickle`, and Python's `multiprocessing` module.
-Created by: Luiz Trindade.
