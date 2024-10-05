<!-- markdownlint-disable -->

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `neo4j_sanitizer`

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Neo4jSanitizer`

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(self : Self, driver : Driver, 
                 keyword_context_node : Context, keyword_context_rels : Context, 
                 ner_context_node : Context, ner_context_rels : Context,
                 batch_size = 10000) 
```

Inizialization of the class

**Args:**
 
 - <b>`contexts`</b> (List[str]):  list of contexts. Can be in the default contexts or not 
 - <b>`all`</b> (bool, optional):  true to includes all the default contexts. Defaults to False. 

 - <b>`self`</b> (Self): instance of the class
 - <b>`driver`</b> (Driver): access point to Neo4j
 - <b>`keyword_context_node`</b> (Context): contexts to use for the sanitization strategy in nodes considering the keywords
 - <b>`keyword_context_rels`</b> (Context): contexts to use for the sanitization strategy in relationships considering the keywords
 - <b>`ner_context_node`</b> (Context): contexts to use for the sanitization strategy in nodes using ner models
 - <b>`ner_context_rels`</b> (Context): contexts to use for the sanitization strategy in relationships using ner models

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getInfoFromDb`

```python
getInfoFromDb(self : Self) → None
```

Get all the information from the database needed for sanitization

**Args:**
 
 - <b>`self`</b> (Self): instance of the class 

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `print_info`

```python
print_info(self : Self) → None
```

Print the info got with getInfoFromDb()

**Args:**
 
 - <b>`self`</b> (Self): instance of the class 

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_info`

```python
show_info(self : Self) → None
```

Better visualization of the infos got with getInfoFromDb()

**Args:**
 
 - <b>`self`</b> (Self): instance of the class 

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L266"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sanitization_brutal_delete`

```python
sanitization_brutal_delete(self : Self) → None
```

Sanitize all the detected warning properties by removing them in nodes and relationship.  
If there are no other properties in the node, it'll be deleted

**Args:**
 
 - <b>`self`</b> (Self): instance of the class 


---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L276"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sanitization_encrypt`

```python
sanitization_encrypt(self : Self) → None
```

Sanitize all the detected warning properties by encrypting their values.  
The keys used are accessible by self.aes_key and self.hmac_key.

**Args:**
 
 - <b>`self`</b> (Self): instance of the class 


---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L292"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sanitization_faker`

```python
sanitization_faker(self : Self, fakers : List[Tuple[str, Callable[[], Any]]]) → None
```

Sanitize all the properties for which has been given a faker function

**Args:**
 
 - <b>`self`</b> (Self): instance of the class 
 - <b>`fakers`</b> (List[Tuple[str, Callable[[], Any]]]): list of Tuple containing
    - key of the property
    - function that returns a random value for the property

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sanitization_ner_suppression`

```python
sanitization_ner_suppression(self : Self, blacklist = [], multiprocessing = False) → None
```

Sanitize all the entities recognized by NER models by replacing the entity with *.

**Args:**
 
 - <b>`self`</b> (Self): instance of the class
 - <b>`blacklist`</b> (list, optional): list of properties to ignore in NER process. Defaults to [].
 - <b>`multiprocessing`</b> (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sanitization_ner_anonimize`

```python
sanitization_ner_anonimize(self : Self, blacklist = [], multiprocessing = False) → None
```

Sanitize all the entities recognized by NER models by replacing the entity with its label.

**Args:**
 
 - <b>`self`</b> (Self): instance of the class
 - <b>`blacklist`</b> (list, optional): list of properties to ignore in NER process. Defaults to [].
 - <b>`multiprocessing`</b> (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L328"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sanitization_ner_encrypt`

```python
sanitization_ner_encrypt(self : Self, blacklist = [], multiprocessing = False) → None
```

Sanitize all the entities recognized by NER models by replacing the entity with its encrypted value.  
The keys used are accessible by self.aes_key and self.hmac_key.

**Args:**
 
 - <b>`self`</b> (Self): instance of the class
 - <b>`blacklist`</b> (list, optional): list of properties to ignore in NER process. Defaults to [].
 - <b>`multiprocessing`</b> (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sanitization_ner_faker`

```python
sanitization_ner_faker(self : Self, fakers : Dict[str, Callable[[], str]], blacklist = [], multiprocessing = False) → None
```

Sanitize all the entities recognized by NER models by replacing the entity with a random value provided by a faker method.  
If the faker for the label of the entity is not provided, the entity value will be replaced with "*".

**Args:**
 
 - <b>`self`</b> (Self): instance of the class
 - <b>`fakers`</b> (Dict[str, Callable[[], str]]): lists for each label of entity, a method f() → str that returns a random value for the label
 - <b>`blacklist`</b> (list, optional): list of properties to ignore in NER process. Defaults to [].
 - <b>`multiprocessing`</b> (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L364"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `estimate_sanitizationKeyword`

```python
estimate_sanitizationKeyword(self : Self) → int
```

Estimate the number of property affected by any of the sanitization that use the keyword

**Args:**
 
 - <b>`self`</b> (Self): instance of the class

**Returns:**
 
 - <b>`int`</b>: number of property

---

<a href="..\..\neo4j_sanitizer\neo4j_sanitizer.py#L382"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `estimate_sanitizationKeyword`

```python
estimate_sanitizationNer(self : Self, blacklist = []) → int :
```

Estimate the number of distinct values affected by any of the sanitization that use the NER  
Note: numeric values are included in this counting but skipped in the NER sanitization

**Args:**
 
 - <b>`self`</b> (Self): instance of the class
 - <b>`blacklist`</b> (list, optional): list of properties to ignore in NER process. Defaults to [].

**Returns:**
 
 - <b>`int`</b>: number of property

---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

