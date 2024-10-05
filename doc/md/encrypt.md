<!-- markdownlint-disable -->

<a href="..\..\neo4j_sanitizer\encrypt.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `encrypt`

---

<a href="..\..\neo4j_sanitizer\encrypt.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `random_key`

```python
random_key() → bytes
```

Returns 32 random bytes 

**Returns:**
 
 - <b>`bytes`</b>:  32 random bytes 

---

<a href="..\..\neo4j_sanitizer\encrypt.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `encrypt_with_key`

```python
encrypt_with_key(text: str, aes_key: bytes, hmac_key: bytes) → bytes
```

Encrypt the text with AES using the aes_key and the hmac_key  

**Args:**
 
 - <b>`text`</b> (str):  text to encrypt 
 - <b>`aes_key`</b> (bytes):  key for AES encrypt (must be 32 bytes long) 
 - <b>`hmac_key`</b> (bytes):  key for HMAC tag (must be 32 bytes long) 

**Returns:**
 bytes:  
 - 0-7: nonce 
 - 8-40 tag 
 - 40-... encryptedText 

---

<a href="..\..\neo4j_sanitizer\encrypt.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `decrypt`

```python
decrypt(data: str, aes_key: bytes, hmac_key: bytes) → str
```

Decrypt the data, encrypted with AES, using the aes_key and the hmac_key  

**Args:**
 
 - <b>`data`</b> (str):  text to dencrypt 
 - <b>`aes_key`</b> (bytes):  key for AES dencrypt (must be 32 bytes long) 
 - <b>`hmac_key`</b> (bytes):  key for check HMAC tag (must be 32 bytes long) 

**Returns:**
 
 - <b>`str`</b>:  original text 

**Raises:**
 
 - <b>`ValueError`</b>:  if the MAC does not match. It means that the message has been tampered with or that the MAC key is incorrect. 

---

<a href="..\..\neo4j_sanitizer\encrypt.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `encrypt_list`

```python
encrypt_list(records: List[str], aes_key: bytes, hmac_key: bytes) → List[str]
```

Encrypt the data and return a list containing the new values encrypted and saved as base64 

**Args:**
 
 - <b>`records`</b> (List[str]):  list of item to encrypt 
 - <b>`aes_key`</b> (bytes):  key for AES dencrypt (must be 32 bytes long) 
 - <b>`hmac_key`</b> (bytes):  key for check HMAC tag (must be 32 bytes long) 

**Returns:**
 
 - <b>`List[str]`</b>:  list of encrypted items  

---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
