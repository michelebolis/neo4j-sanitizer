<!-- markdownlint-disable -->

<a href="..\..\neo4j_sanitizer\context.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `context`

---

<a href="..\..\neo4j_sanitizer\context.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Context`

<a href="..\..\neo4j_sanitizer\context.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(contexts: List[str], all=False)
```

Create an instance of Context 

**Args:**
 
 - <b>`contexts`</b> (List[str]):  list of contexts. Can be in the default contexts or not 
 - <b>`all`</b> (bool, optional):  true to includes all the default contexts. Defaults to False. 

---

<a href="..\..\neo4j_sanitizer\context.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `addKeyword`

```python
addKeyword(context: str, keywords: List[str]) → None
```

Add the keywords in the list to the context 

**Args:**
 
 - <b>`context`</b> (str):  context that can be in the default contexts or not 
 - <b>`keywords`</b> (List[str]):  keywords to add 

---

<a href="..\..\neo4j_sanitizer\context.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `evalInContext`

```python
evalInContext(list: List[str]) → List[str]
```

Returns a subset of the given list with only the words recognized in one of the context 

**Args:**
 
 - <b>`list`</b> (List[str]):  contains the words to be evaluated 

**Returns:**
 
 - <b>`List[str]`</b>:  contains the words in the contexts 

---

<a href="..\..\neo4j_sanitizer\context.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `getContexts`

```python
getContexts() → List[str]
```

Get all the contexts 

**Returns:**
 
 - <b>`List[str]`</b>:  list of contexts 

---

<a href="..\..\neo4j_sanitizer\context.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `removeContext`

```python
removeContext(context: str) → None
```

Removes a context from the context list. 

**Args:**
 
 - <b>`context`</b> (str):  The context to remove. 

---

<a href="..\..\neo4j_sanitizer\context.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `removeKeyword`

```python
removeKeyword(context: str, keywords: List[str]) → None
```

Remove the keywords in the list to the context 

**Args:**
 
 - <b>`context`</b> (str):  context that can be in the default contexts or not 
 - <b>`keywords`</b> (List[str]):  keywords to remove 

---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
