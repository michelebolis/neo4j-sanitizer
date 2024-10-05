<!-- markdownlint-disable -->

<a href="..\..\neo4j_sanitizer\sanitizationKeyword.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `sanitizationKeyword`

---

<a href="..\..\neo4j_sanitizer\sanitizationKeyword.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sanitization_brutal_delete`

```python
sanitization_brutal_delete(sanitizer, batch_size = 2000) → None
```

Perform brutal deletion of warning properties in nodes and relationships.

**Args:**
 
 - <b>`sanitizer`</b>: The sanitizer containing information about warning properties and relationships.
 - <b>`batch_size`</b> (optional): The number of items to process in each batch. Defaults to 2000. 

---

<a href="..\..\neo4j_sanitizer\sanitizationKeyword.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sanitization_encrypt`

```python
sanitization_encrypt(sanitizer, batch_size = 2000) → None
```

Perform the sanitization process by encrypting data in nodes and relationships.

**Args:**
 
 - <b>`sanitizer`</b>: The sanitizer containing information about warning properties and relationships.
 - <b>`batch_size`</b> (optional): The batch size for updating the data. Defaults to 2000. 

---

<a href="..\..\neo4j_sanitizer\sanitizationKeyword.py#L132"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sanitization_faker`

```python
sanitization_faker(sanitizer, fakers : List[Tuple[str, Callable[[], str]]], batch_size = 2000) → None
```

A function that performs sanitization using faker functions on nodes and relationships for given properties.

**Args:**
 
 - <b>`sanitizer`</b>: The sanitizer containing information about warning properties and relationships.
 - <b>`fakers`</b>: A list of tuples containing the property key and a function that returns a random value for the property.
 - <b>`batch_size`</b> (optional): The number of values to process in each batch. Defaults to 2000.

---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
