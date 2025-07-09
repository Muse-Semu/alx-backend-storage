# Redis Basic

This project implements a basic caching system using Redis in Python as part of the ALX Backend Storage curriculum.

## Repository
- **GitHub Repository**: alx-backend-storage
- **Directory**: 0x02-redis_basic
- **Main File**: exercise.py

## Description
The project focuses on creating a `Cache` class that interacts with a Redis database. The class provides functionality to:
- Initialize a Redis client and flush the database
- Store data (string, bytes, integer, or float) with a randomly generated key
- Return the generated key for later data retrieval

## Requirements
- Python 3.7+
- Redis server
- Python packages:
  - `redis`
  - `uuid`
  - `typing`

## Installation
1. Clone the repository:
   ```bash
   ```
2. Navigate to the project directory:
   ```bash
   cd alx-backend-storage/0x02-redis_basic
   ```
3. Install required packages:
   ```bash
   pip install redis
   ```
4. Ensure Redis server is running on your system.

## Usage
The main file (`main.py`) demonstrates the usage of the `Cache` class:
```python
#!/usr/bin/env python3
import redis
Cache = __import__('exercise').Cache

cache = Cache()
data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))
```

Run the script:
```bash
python3 main.py
```

Example output:
```
3a3e8231-b2f6-450d-8b0e-0f38f16e8ca2
b'hello'
```

## Files
- **exercise.py**: Contains the `Cache` class implementation with Redis operations
- **main.py**: Demonstration script showing how to use the `Cache` class
- **README.md**: Project documentation (this file)

## Implementation Details
- The `Cache` class uses `redis.Redis()` to create a client instance
- The database is flushed upon initialization using `flushdb()`
- The `store` method:
  - Generates random keys using `uuid.uuid4()`
  - Supports storing `str`, `bytes`, `int`, and `float` data types
  - Returns the generated key as a string
- Type hints are used for proper type annotation

## Author
Muse Semu