# Free Fire API Client

A Python client for interacting with Free Fire's API endpoints, allowing various in-game actions through encrypted protobuf requests.

## Features

- Change player signature
- Choose player title
- Set player gallery show info
- Buy chat items
- Request to join a clan
- Like player profiles
- any feature? do it urself fkup

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

## Available Methods
Change Signature
```python
freefire_api.ChangeSignature("Your new signature")
```
Choose Title
```python
freefire_api.ChooseTitle(title_id)  # Replace with actual title ID
```
Set Player Gallery Show Info
```python
freefire_api.SetPlayerGalleryShowInfo(slot_number, item_id)
```
Buy Chat Items
```python
freefire_api.BuyChatItems(item_id)
```
Request to Join Clan
```python
freefire_api.RequestJoinClan(guild_id)
```
Like Profile
```python
freefire_api.LikeProfile(user_id, 'region_code')  # e.g. 'ID' for Indonesia
```

## Encryption
All requests are encrypted using AES-CBC with:
- Key: WWcmdGMlREV1aDYlWmNeOA== (base64 decoded)
- IV: Nm95WkRyMjJFM3ljaGpNJQ== (base64 decoded)

# Disclaimer
This code is for educational purposes only. Use at your own risk. The authors are not responsible for any account bans or violations of Terms of Service that may result from using this code.
