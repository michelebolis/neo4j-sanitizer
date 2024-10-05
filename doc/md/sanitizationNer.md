<!-- markdownlint-disable -->

<a href="..\..\neo4j_sanitizer\sanitizationNer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `sanitizationNer`

---

<a href="..\..\neo4j_sanitizer\sanitizationNer.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sanitization_suppression`

```python
sanitization_suppression(sanitizer, blacklist = [], batch_size = 2000, multiprocessing = False) → None
```

Perform sanitization suppression on nodes and relationships

**Args:**
 
 - <b>`sanitizer`</b>: The sanitizer containing the data to be sanitized.
 - <b>`blacklist`</b> (List[str], optional): A list of properties to be excluded from sanitization. Defaults to an empty list.
 - <b>`batch_size`</b> (int, optional): The number of values to process in each batch. Defaults to 2000.
 - <b>`multiprocessing`</b> (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.
---

<a href="..\..\neo4j_sanitizer\sanitizationNer.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sanitization_anonimize`

```python
sanitization_anonimize(sanitizer, blacklist = [], batch_size = 2000, multiprocessing = False) → None
```

Perform sanitization (ner anonimize) on nodes and relationships

**Args:**
 
 - <b>`sanitizer`</b>: The sanitizer containing the data to be sanitized.
 - <b>`blacklist`</b> (List[str], optional): A list of properties to be excluded from sanitization. Defaults to an empty list.
 - <b>`batch_size`</b> (int, optional): The number of values to process in each batch. Defaults to 2000.
 - <b>`multiprocessing`</b> (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.
 
---

<a href="..\..\neo4j_sanitizer\sanitizationNer.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sanitization_ner_encrypt`

```python
sanitization_ner_encrypt(sanitizer, blacklist = [], batch_size = 2000, multiprocessing = False) → None
```

Perform sanitization (ner encrypt) on nodes and relationships

**Args:**
 
 - <b>`sanitizer`</b>: The sanitizer containing the data to be sanitized.
 - <b>`blacklist`</b> (List[str], optional): A list of properties to be excluded from sanitization. Defaults to an empty list.
 - <b>`batch_size`</b> (int, optional): The number of values to process in each batch. Defaults to 2000.
 - <b>`multiprocessing`</b> (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.
 
---

<a href="..\..\neo4j_sanitizer\sanitizationNer.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sanitization_ner_faker`

```python
sanitization_ner_faker(sanitizer, blacklist = [], batch_size = 2000, multiprocessing = False) → None
```

Perform sanitization (ner faker) on nodes and relationships

**Args:**
 
 - <b>`sanitizer`</b>: The sanitizer containing the data to be sanitized.
 - <b>`blacklist`</b> (List[str], optional): A list of properties to be excluded from sanitization. Defaults to an empty list.
 - <b>`batch_size`</b> (int, optional): The number of values to process in each batch. Defaults to 2000.
 - <b>`multiprocessing`</b> (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.
 
---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._