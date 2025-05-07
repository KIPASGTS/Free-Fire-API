# Free Fire API Client

A Python client for interacting with Free Fire's API endpoints, allowing various in-game actions through encrypted protobuf requests.

## Features

- Change player signature
- Choose player title
- Set player gallery show info
- Buy chat items
- Request to join a clan
- Like player profiles

## Requirements

- Python 3.x
- Required packages:
  - `requests`
  - `pycryptodomex` (or `pycryptodome`)

Install dependencies with:
```bash
pip install requests pycryptodomex
```

## Usage

Initialize the API client:
```python
freefire_api = FreeFireApi()
```
Set your authentication token (replace 'yourbarrier'):
```python
freefire_api.Auth = 'Bearer your_actual_token_here'
```
