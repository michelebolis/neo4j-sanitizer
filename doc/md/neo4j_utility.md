<!-- markdownlint-disable -->

<a href="..\neo4j_sanitizer\neo4j_utility.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `neo4j_utility`





---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `connect`

```python
connect(URI: str, AUTH: Tuple[str, str], DB: str) → Driver
```

Connect and return an access point to Neo4j database 



**Args:**
 
 - <b>`URI`</b> (str):  link for the database session 
 - <b>`AUTH`</b> (Tuple[str, str]):  tuple containing name of the use and the password 
 - <b>`DB`</b> (str):  name of the database to use 



**Returns:**
 
 - <b>`Driver`</b>:  the access point to the database 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `db_profiling`

```python
db_profiling(driver: Driver) → Tuple[List[str], List[str], List[str], List[str]]
```

Profiles the structure of the database 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 



**Returns:**
 Tuple[List[str], List[str], List[str], List[str]]:  
    - keys of properties in nodes 
    - keys of properties in relationships 
    - labels of the nodes 
    - types of relationships 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `findCentralNode`

```python
findCentralNode(driver: Driver) → Tuple[Record, int]
```

Finds and returns the node with the largest number of relationships 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 



**Returns:**
 None if there are no relationships 
 - <b>`Tuple[Record, int]`</b>:  tuple containing the central nodes and the number of relationships  ['node'] → Record  ['count'] → int 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `findIsolatedNodes`

```python
findIsolatedNodes(driver: Driver) → List[Record]
```

Finds and returns the nodes with no relationships 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 



**Returns:**
 
 - <b>`List[Record]`</b>:  list of isolated nodes 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countDBNodes`

```python
countDBNodes(driver: Driver) → int
```

Returns the number of nodes in the database 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 



**Returns:**
 
 - <b>`int`</b>:  number of nodes 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `printNodeInfo`

```python
printNodeInfo(node: Record) → None
```

Prints the information of the node 



**Args:**
 
 - <b>`node`</b> (Record):  node with the information to be printed 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countLabels`

```python
countLabels(driver: Driver, labels: List[str]) → Dict[str, int]
```

Counts the occurrences of each label in the nodes 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`labels`</b> (List[str]):  list of labels 



**Returns:**
 
 - <b>`Dict[str, int]`</b>:  dictionary containing for each label, the number of occurencies 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countLabel`

```python
countLabel(driver: Driver, label: str) → int
```

Counts the occurrences of the label in the nodes 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  label to count 



**Returns:**
 
 - <b>`int`</b>:  number of occurencies 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L150"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countLabeless`

```python
countLabeless(driver: Driver) → int
```

Counts the occurences of nodes without a label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 



**Returns:**
 
 - <b>`int`</b>:  number of occurencies 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countMultipleLabelsNodes`

```python
countMultipleLabelsNodes(driver: Driver) → int
```

Counts the number of nodes with multiple labels 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 



**Returns:**
 
 - <b>`int`</b>:  number of nodes with multiple labels 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countPropertyLabelessNode`

```python
countPropertyLabelessNode(driver: Driver, property: str) → int
```

Counts the occurrences of nodes without labels for a given property. 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`property`</b> (str):  property to count 



**Returns:**
 
 - <b>`int`</b>:  number of occurrences 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countPropertyMultipleLabelsNode`

```python
countPropertyMultipleLabelsNode(driver: Driver, property: str) → int
```

Counts the occurrences of nodes with multiple labels for a given property. 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`property`</b> (str):  property to count 



**Returns:**
 
 - <b>`int`</b>:  number of occurrences 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L210"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `deleteNodes`

```python
deleteNodes(driver: Driver, label: str, batch_size=2000) → None
```

Deletes all the nodes with the given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  given label  
 - <b>`batch_size`</b> (int, optional):  number of operation in a transaction. Defaults to 2000. 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `deletePropertylessNodes`

```python
deletePropertylessNodes(driver: Driver) → None
```

Deletes all nodes that do not have any labels or properties. 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L232"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countDBRelationships`

```python
countDBRelationships(driver: Driver) → int
```

Returns the number of relationships in the database 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 



**Returns:**
 
 - <b>`int`</b>:  number of relationships 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L246"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countRelationships`

```python
countRelationships(driver: Driver, rels: List[str]) → Dict[str, int]
```

Returns the occurences of relationships for each types 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`rels`</b> (List[str]):  types of relationships 



**Returns:**
 
 - <b>`Dict[str, int]`</b>:  dictionary containing for each type, the number of occurencies 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L260"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countRelationship`

```python
countRelationship(driver: Driver, label: str) → int
```

Returns the number of relatinships with the given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  given label 

**Returns:**
 
 - <b>`int`</b>:  number of relatinships with the given label 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L274"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getOutgoingRelationships`

```python
getOutgoingRelationships(
    driver: Driver,
    labels: List[str]
) → Dict[str, List[Tuple[int, str, str, int]]]
```

Returns for each label, the list of outgoing relationships  



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`labels`</b> (List[str]):  list of labels 



**Returns:**
 
 - <b>`Dict[str, List[Tuple[int, str, str, int]]]`</b>:  _description_ #TODO 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L286"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getIngoingRelationships`

```python
getIngoingRelationships(
    driver: Driver,
    labels: List[str]
) → Dict[str, List[Tuple[int, str, str, int]]]
```

Returns for each label, the list of ingoing relationships  



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`labels`</b> (List[str]):  list of labels 



**Returns:**
 
 - <b>`Dict[str, List[Tuple[int, str, str, int]]]`</b>:  _description_ #TODO 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L330"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countProperties`

```python
countProperties(
    driver: Driver,
    properties: List[str]
) → Dict[str, List[Tuple[int, str]]]
```

Returns for each property, the number of occurencies for each label of nodes 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`properties`</b> (List[str]):  list of properties 



**Returns:**
 
 - <b>`Dict[str, List[Tuple[int, str]]]`</b>:  for each property contains the occurences in each node with a label 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L348"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countPropertiesRels`

```python
countPropertiesRels(
    driver: Driver,
    properties: List[str]
) → Dict[str, Tuple[int, str]]
```

Returns for each property, the number of occurencies for each type of relationship 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`properties`</b> (List[str]):  list of properties 



**Returns:**
 
 - <b>`Dict[str, Tuple[int, str]]`</b>:  for each property contains the occurences in each relationship with a type 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L366"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countPropertyNode`

```python
countPropertyNode(driver: Driver, property: str, label: str) → int
```

Returns the number of occurencies of the properity in nodes with the given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`property`</b> (str):  property to count 
 - <b>`label`</b> (str):  given label for the nodes 



**Returns:**
 
 - <b>`int`</b>:  number of occurencies 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L382"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countPropertyRel`

```python
countPropertyRel(driver: Driver, property: str, rel: str) → int
```

Returns the number of occurencies of the properity in relationships with the given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`property`</b> (str):  key of the property to count 
 - <b>`rel`</b> (str):  given type for the relationship 



**Returns:**
 
 - <b>`int`</b>:  number of occurencies 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L398"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countDistintValueNodes`

```python
countDistintValueNodes(driver: Driver, label: str, property: str) → int
```

Returns the number of distinct values of the property in nodes with the given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  given label for the nodes 
 - <b>`property`</b> (str):  property to count 



**Returns:**
 
 - <b>`int`</b>:  number of distinct values 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L414"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countDistintValueLabelessNodes`

```python
countDistintValueLabelessNodes(driver: Driver, property: str) → int
```

Returns the number of distinct values of the property in nodes without labels 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`property`</b> (str):  property to count 



**Returns:**
 
 - <b>`int`</b>:  number of distinct values 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L429"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countDistintValueMultipleLabelsNodes`

```python
countDistintValueMultipleLabelsNodes(driver: Driver, property: str) → int
```

Returns the number of distinct values of a property in nodes with multiple labels. 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`property`</b> (str):  property to count 



**Returns:**
 
 - <b>`int`</b>:  number of distinct values 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L444"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `countDistintValueRels`

```python
countDistintValueRels(driver: Driver, rel: str, property: str) → int
```

Returns the number of distinct values of the relationships in nodes with the given type 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`property`</b> (str):  key of the property to count 
 - <b>`rel`</b> (str):  given type for the relationship 



**Returns:**
 
 - <b>`int`</b>:  number of distinct values 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L460"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getValuesNodes`

```python
getValuesNodes(driver: Driver, label: str, property: str) → List[Record]
```

Returns the list of all the pair (id, value) of the given property in nodes 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  label of the nodes 
 - <b>`property`</b> (str):  key of the property 



**Returns:**
 
 - <b>`List[Record]`</b>:  list of record with (id, value) 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L476"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getValuesRels`

```python
getValuesRels(driver: Driver, rel: str, property: str) → List[Record]
```

Returns the list of all the pair (id, value) of the given property in relationships 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`rel`</b> (str):  type of relation 
 - <b>`property`</b> (str):  key of the property 



**Returns:**
 
 - <b>`List[Record]`</b>:  list of record with (id, value) 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L492"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getDistinctValuesNodes`

```python
getDistinctValuesNodes(driver: Driver, label: str, prop: str) → List[Record]
```

Returns all the distinct value of a property in nodes with a given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  label of nodes 
 - <b>`prop`</b> (str):  key of the property 



**Returns:**
 
 - <b>`List[Record]`</b>:  list of record with (prop) 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L506"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getDistinctValuesLabelessNodes`

```python
getDistinctValuesLabelessNodes(driver: Driver, prop: str) → List[Record]
```

Returns all the distinct value of a property in nodes with a given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`prop`</b> (str):  key of the property 



**Returns:**
 
 - <b>`List[Record]`</b>:  list of record with (prop) 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L519"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getDistinctValuesMultipleLabelsNodes`

```python
getDistinctValuesMultipleLabelsNodes(driver: Driver, prop: str) → List[Record]
```

Returns all the distinct value of a property in nodes with multiple labels 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`prop`</b> (str):  key of the property 



**Returns:**
 
 - <b>`List[Record]`</b>:  list of record with (prop) 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L532"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getDistinctValuesRels`

```python
getDistinctValuesRels(driver: Driver, rel: str, prop: str) → List[Record]
```

Returns all the distinct value of a property in relationships with a given type 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`rel`</b> (str):  type of relationships 
 - <b>`prop`</b> (str):  key of the property 



**Returns:**
 
 - <b>`List[Record]`</b>:  list of record with (prop) 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L546"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `updateValueRels`

```python
updateValueRels(
    driver: Driver,
    rel: str,
    property: str,
    oldvalue: Any,
    newvalue: Any,
    batch_size=2000
) → None
```

Update the value of property in relationships with the given type 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`rel`</b> (str):  type of relationships 
 - <b>`property`</b> (str):  key of the property 
 - <b>`oldvalue`</b> (Any):  old value of the property 
 - <b>`newvalue`</b> (Any):  new value of the property 
 - <b>`batch_size`</b> (int, optional):  number of update in a transaction. Defaults to 2000. 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L565"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `updateValueNodes`

```python
updateValueNodes(
    driver: Driver,
    label: str,
    property: str,
    oldvalue: Any,
    newvalue: Any,
    batch_size=2000
) → None
```

Update the value of property in relationships with the given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  label of the nodes 
 - <b>`property`</b> (str):  key of the property 
 - <b>`oldvalue`</b> (Any):  old value of the property 
 - <b>`newvalue`</b> (Any):  new value of the property 
 - <b>`batch_size`</b> (int, optional):  number of update in a transaction. Defaults to 2000. 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L584"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `updateValueLabelessNodes`

```python
updateValueLabelessNodes(
    driver: Driver,
    property: str,
    oldvalue: Any,
    newvalue: Any,
    batch_size=2000
) → None
```

Update the value of property in nodes without label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`property`</b> (str):  key of the property 
 - <b>`oldvalue`</b> (Any):  old value of the property 
 - <b>`newvalue`</b> (Any):  new value of the property 
 - <b>`batch_size`</b> (int, optional):  number of update in a transaction. Defaults to 2000. 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L602"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `updateValueMultipleLabelsNodes`

```python
updateValueMultipleLabelsNodes(
    driver: Driver,
    property: str,
    oldvalue: Any,
    newvalue: Any,
    batch_size=2000
) → None
```

Update the value of property in nodes with multiple labels 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`property`</b> (str):  key of the property 
 - <b>`oldvalue`</b> (Any):  old value of the property 
 - <b>`newvalue`</b> (Any):  new value of the property 
 - <b>`batch_size`</b> (int, optional):  number of update in a transaction. Defaults to 2000. 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L620"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `removePropertyNodes`

```python
removePropertyNodes(driver: Driver, label: str, property: str, batch_size=2000)
```

Remove the property in the nodes with the given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  label of the node 
 - <b>`property`</b> (str):  property to remove 
 - <b>`batch_size`</b> (int, optional):  number of update in a transaction. Defaults to 2000. 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L636"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `removePropertyLabelessNodes`

```python
removePropertyLabelessNodes(driver: Driver, property: str, batch_size=2000)
```

Remove the property in the nodes with the given label 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  label of the node 
 - <b>`property`</b> (str):  property to remove 
 - <b>`batch_size`</b> (int, optional):  number of update in a transaction. Defaults to 2000. 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L652"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `removePropertyMultipleLabelsNodes`

```python
removePropertyMultipleLabelsNodes(
    driver: Driver,
    property: str,
    batch_size=2000
)
```

Remove the property in the nodes with multiple labels 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`label`</b> (str):  label of the node 
 - <b>`property`</b> (str):  property to remove 
 - <b>`batch_size`</b> (int, optional):  number of update in a transaction. Defaults to 2000. 


---

<a href="..\neo4j_sanitizer\neo4j_utility.py#L668"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `removePropertyRels`

```python
removePropertyRels(driver: Driver, rel: str, property: str, batch_size=2000)
```

Remove the property in the relationships with the given type 



**Args:**
 
 - <b>`driver`</b> (Driver):  access point to Neo4j 
 - <b>`rel`</b> (str):  type of the relation 
 - <b>`property`</b> (str):  property to remove 
 - <b>`batch_size`</b> (int, optional):  number of update in a transaction. Defaults to 2000. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
