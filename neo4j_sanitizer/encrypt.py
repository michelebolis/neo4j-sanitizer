import base64
from typing import Dict, List, Tuple
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes

def random_key() -> bytes : 
    """Returns 32 random bytes

    Returns:
        bytes: 32 random bytes
    """
    return get_random_bytes(32)
def encrypt_with_key(text : str, aes_key : bytes, hmac_key : bytes) -> bytes :
    """Encrypt the text with AES using the aes_key and the hmac_key 

    Args:
        text (str): text to encrypt
        aes_key (bytes): key for AES encrypt (must be 32 bytes long)
        hmac_key (bytes): key for HMAC tag (must be 32 bytes long)

    Returns:
        bytes: 
        - 0-7: nonce
        - 8-40 tag
        - 40-... encryptedText
    """
    cipher = AES.new(aes_key, AES.MODE_CTR)
    ciphertext = cipher.encrypt(str(text).encode())

    hmac = HMAC.new(hmac_key, digestmod=SHA256)
    tag = hmac.update(cipher.nonce + ciphertext).digest()
    return cipher.nonce + tag + ciphertext

def decrypt(data : str, aes_key : bytes, hmac_key : bytes) -> str :
    """Decrypt the data, encrypted with AES, using the aes_key and the hmac_key 

    Args:
        data (str): text to dencrypt
        aes_key (bytes): key for AES dencrypt (must be 32 bytes long)
        hmac_key (bytes): key for check HMAC tag (must be 32 bytes long)

    Returns:
        str: original text
    
    Raises:
        ValueError: if the MAC does not match. It means that the message has been tampered with or that the MAC key is incorrect.
    """
    nonce = data[:8]
    tag = data[8:40]
    string = data[40:]

    hmac = HMAC.new(hmac_key, digestmod=SHA256)
    tag = hmac.update(nonce + string).verify(tag)
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
    return cipher.decrypt(string).decode()

def encrypt_list(records : List[str], aes_key : bytes, hmac_key : bytes) -> List[str]:
    """Encrypt the data and return a list containing the new values encrypted and saved as base64

    Args:
        records (List[str]): list of item to encrypt
        aes_key (bytes): key for AES dencrypt (must be 32 bytes long)
        hmac_key (bytes): key for check HMAC tag (must be 32 bytes long)

    Returns:
        List[str]: list of encrypted items 
    """
    return [str(base64.b64encode(encrypt_with_key(data, aes_key, hmac_key)), 'utf-8') for data in records]