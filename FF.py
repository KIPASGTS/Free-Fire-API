import base64
import requests
from Cryptodome.Cipher import AES

def encode_varint(value):
    buffer = bytearray()
    while value > 0x7F:
        buffer.append((value & 0x7F) | 0x80)
        value >>= 7
    buffer.append(value)
    return buffer

def encode_field(tag, wire_type):
    return encode_varint((tag << 3) | wire_type)

def build_protobuf(fields):
    result = bytearray()
    for field in fields:
        tag = field['tag']
        wire_type = field['wire_type']
        value = field['value']
        result += encode_field(tag, wire_type)
        
        if wire_type == 0:  # Varint
            result += encode_varint(value)
        elif wire_type == 2:  # Length-delimited (string, bytes, or nested protobuf)
            if isinstance(value, (bytes, bytearray)):
                result += encode_varint(len(value))
                result += value
            else:
                encoded = value.encode('utf-8')
                result += encode_varint(len(encoded))
                result += encoded

        else:
            raise ValueError(f"Unsupported wire type: {wire_type}")

    return result

def pad(text: bytes) -> bytes:
    padding_length = AES.block_size - (len(text) % AES.block_size)
    padding = bytes([padding_length] * padding_length)
    return text + padding

def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    aes = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext)
    ciphertext = aes.encrypt(padded_plaintext)
    return ciphertext

MAIN_KEY = base64.b64decode('WWcmdGMlREV1aDYlWmNeOA==')
MAIN_IV = base64.b64decode('Nm95WkRyMjJFM3ljaGpNJQ==')


class FreeFireApi:
    def __init__(self):
        self.MAIN_KEY = base64.b64decode('WWcmdGMlREV1aDYlWmNeOA==')
        self.MAIN_IV = base64.b64decode('Nm95WkRyMjJFM3ljaGpNJQ==')
        self.Auth = 'Bearer yourbarrier'
        self.headets = headers = {
            'Host': 'clientbp.ggblueshark.com',
            'X-Unity-Version': '2018.4.11f1',
            'Accept': '*/*',
            'Authorization': self.Auth,
            'ReleaseVersion': 'OB48',
            'X-GA': 'v1 1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'id-ID,id;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Free%20Fire/2019118071 CFNetwork/1568.200.51 Darwin/24.1.0',
            'Connection': 'keep-alive'
        }
        self.url = "https://clientbp.ggblueshark.com"

    def ChangeSignature(self, signature_update):
        fields = [
            {'tag': 1, 'wire_type': 0, 'value': 1},                  # Field #1
            {'tag': 2, 'wire_type': 0, 'value': 6},                  # Field #2
            {'tag': 4, 'wire_type': 0, 'value': 2},                  # Field #4
            {'tag': 5, 'wire_type': 2, 'value': ''},                 # Field #5
            {'tag': 6, 'wire_type': 2, 'value': ''},                 # Field #6
            {'tag': 8, 'wire_type': 2, 'value': signature_update},       # Field #8
            {'tag': 9, 'wire_type': 0, 'value': 1},                  # Field #9
            {'tag': 11, 'wire_type': 2, 'value': ''},                # Field #11
            {'tag': 12, 'wire_type': 2, 'value': ''},                # Field #12
        ]

        protobuf_bytes = build_protobuf(fields)
        encrypted_data = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, protobuf_bytes)

        url = self.url + "/UpdateSocialBasicInfo"

        request = requests.post(url, data=encrypted_data, headers=self.headets)
        print(request.text)
    
    def ChooseTitle(self, title_id: int):
        fields = [
            {'tag': 1, 'wire_type': 0, 'value': title_id},
        ]

        protobuf_bytes = build_protobuf(fields)
        encrypted_data = aes_cbc_encrypt(self.MAIN_KEY, self.MAIN_IV, protobuf_bytes)

        url = self.url + "/ChooseTitle"

        response = requests.post(url, data=encrypted_data, headers=self.headets)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.content}")

    def SetPlayerGalleryShowInfo(self, slot: int, itemid: int):
        object_itemid = build_protobuf([
            {'tag': 6, 'wire_type': 0, 'value': itemid},
        ])

        object_slot = build_protobuf([
            {'tag': 1, 'wire_type': 0, 'value': slot},
            {'tag': 6, 'wire_type': 2, 'value': object_itemid},
        ])

        objects = build_protobuf([
            {'tag': 1, 'wire_type': 0, 'value': 1},
            {'tag': 2, 'wire_type': 2, 'value': object_slot},
        ])

        # Final message:
        fields = [
            {'tag': 1, 'wire_type': 0, 'value': 1},
            {'tag': 2, 'wire_type': 2, 'value': objects},
        ]

        protobuf_bytes = build_protobuf(fields)
        encrypted_data = aes_cbc_encrypt(self.MAIN_KEY, self.MAIN_IV, protobuf_bytes)

        url = self.url + "/SetPlayerGalleryShowInfo"

        response = requests.post(url, data=encrypted_data, headers=self.headets)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.content}")


    def BuyChatItems(self, itemid: int):
        # Final message:
        fields = [
            {'tag': 2, 'wire_type': 0, 'value': itemid},
        ]

        protobuf_bytes = build_protobuf(fields)
        encrypted_data = aes_cbc_encrypt(self.MAIN_KEY, self.MAIN_IV, protobuf_bytes)

        url = self.url + "/BuyChatItems"

        response = requests.post(url, data=encrypted_data, headers=self.headets)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.content}")
    
    def RequestJoinClan(self, guildid: int):
        # Final message:
        fields = [
            {'tag': 1, 'wire_type': 0, 'value': guildid},
        ]

        protobuf_bytes = build_protobuf(fields)
        encrypted_data = aes_cbc_encrypt(self.MAIN_KEY, self.MAIN_IV, protobuf_bytes)

        url = self.url + "/RequestJoinClan"
        

        response = requests.post(url, data=encrypted_data, headers=self.headets)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.content}")

    def LikeProfile(self, userid: int, region: str):
        # Final message:
        fields = [
            {'tag': 1, 'wire_type': 0, 'value': userid},
            {'tag': 2, 'wire_type': 2, 'value': region},
        ]

        protobuf_bytes = build_protobuf(fields)
        encrypted_data = aes_cbc_encrypt(self.MAIN_KEY, self.MAIN_IV, protobuf_bytes)

        url = self.url + "/LikeProfile"
        

        response = requests.post(url, data=encrypted_data, headers=self.headets)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.content}")
