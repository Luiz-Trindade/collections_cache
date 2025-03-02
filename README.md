# collections-cache  

`collections-cache` is a simple and efficient caching solution built with SQLite databases. It allows storing, updating, and retrieving data using unique keys while supporting complex data types through `pickle`. Designed to scale across multiple CPU cores, it distributes data across multiple SQLite databases for improved performance.  

## Features  

- **Multiple SQLite databases**: Distributes data across multiple databases for better scalability.  
- **Key-value store**: Stores data as key-value pairs.  
- **Supports complex data types**: Data is serialized using `pickle`, allowing you to store lists, dictionaries, and other Python objects.  
- **Parallel processing**: Utilizes Python’s `multiprocessing` module to handle large collections in parallel across multiple CPU cores.  
- **Efficient data retrieval**: Retrieves stored data efficiently based on the key.  
- **Cross-platform**: Works on Linux, macOS, and Windows.  

## Installation  

To install the `collections-cache` package, use [Poetry](https://python-poetry.org/) to manage dependencies.  

1. Clone the repository:  

    ```bash
    git clone https://github.com/Luiz-Trindade/collections_cache.git
    cd collections-cache
    ```  

2. Install the package with Poetry:  

    ```bash
    poetry install
    ```  

## Usage  

To use the `collections-cache` package, import the main class `Collection_Cache` and interact with your collection.  

### Example  

```python
from collections_cache import Collection_Cache

# Create a new collection
cache = Collection_Cache("STORE")

# Set a key-value pair
cache.set_key("products", ["apple", "orange", "onion"])

# Get the value by key
products = cache.get_key("products")
print(products)  # Output: ['apple', 'orange', 'onion']
```  

### Methods  

- **`set_key(key, value)`**: Stores a key-value pair in the cache. If the key already exists, its value is updated.  
- **`get_key(key)`**: Retrieves the value associated with a key.  
- **`delete_key(key)`**: Removes an existing key from the cache.  

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

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.  

## Acknowledgements  

- This package was created to demonstrate how to work with SQLite, `pickle`, and Python's `multiprocessing` module.  
- Created by: Luiz Trindade.
