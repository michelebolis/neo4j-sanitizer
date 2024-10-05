from typing import Any, Dict, List, Tuple
from neo4j import GraphDatabase
from neo4j import Driver, Record

def connect(URI : str, AUTH : Tuple[str, str], DB : str) -> Driver :
    """Connect and return an access point to Neo4j database

    Args:
        URI (str): link for the database session
        AUTH (Tuple[str, str]): tuple containing name of the use and the password
        DB (str): name of the database to use

    Returns:
        Driver: the access point to the database
    """
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    driver.session(database=DB)
    return driver

def db_profiling(driver : Driver) -> Tuple[List[str], List[str], List[str], List[str]] :
    """Profiles the structure of the database

    Args:
        driver (Driver): access point to Neo4j

    Returns:
        Tuple[List[str], List[str], List[str], List[str]]: 
        - keys of properties in nodes
        - keys of properties in relationships
        - labels of the nodes
        - types of relationships
    """
    records, _, _ = driver.execute_query(
        "MATCH (a) UNWIND keys(a) AS key RETURN collect(distinct key)"
    )
    nodes_properties = records[0][0]

    records, _, _ = driver.execute_query(
        "MATCH ()-[r]-() UNWIND keys(r) AS key RETURN collect(distinct key)"
    )
    relationships_properties = records[0][0]

    records, _, _ = driver.execute_query(
        "CALL db.labels()"
    )
    labels = [record['label'] for record in records]

    records, _, _ = driver.execute_query(
        "CALL db.relationshipTypes()"
    )
    relationships = [record["relationshipType"] for record in records]

    return nodes_properties, relationships_properties, labels, relationships, 

# Nodes
def findCentralNode(driver : Driver) -> Tuple[Record, int] :
    """Finds and returns the node with the largest number of relationships

    Args:
        driver (Driver): access point to Neo4j

    Returns:
        None if there are no relationships
        Tuple[Record, int]: tuple containing the central nodes and the number of relationships
            ['node'] -> Record
            ['count'] -> int
    """
    record, _, _ = driver.execute_query(
        """
        MATCH (n)-[r]-() WITH n as node, count(*) as c 
        WITH max(c) as target 
        MATCH (n)-[r]-() WITH n as node, count(r) as candidate, target WHERE candidate=target RETURN node as node, candidate as count
        """
    )
    if len(record) > 0 : return record[0]
    return None

def findIsolatedNodes(driver : Driver) -> List[Record] : 
    """Finds and returns the nodes with no relationships

    Args:
        driver (Driver): access point to Neo4j

    Returns:
        List[Record]: list of isolated nodes
    """
    record, _, _ = driver.execute_query(
        "MATCH (n) WHERE NOT (n)-[]-() RETURN n"
    )
    return record

def countDBNodes(driver : Driver) -> int : 
    """Returns the number of nodes in the database

    Args:
        driver (Driver): access point to Neo4j

    Returns:
        int: number of nodes
    """
    record, _, _ = driver.execute_query(
        "MATCH (n) RETURN count(*) as count"
    )
    return record[0]['count']

def printNodeInfo(node : Record) -> None :
    """Prints the information of the node

    Args:
        node (Record): node with the information to be printed
    """
    s = ""
    for label in node.labels : s += label + ", "
    s = s[0 : len(s) - 2]
    print(" - Labels:", s)
    print(" - Properties:")
    for attr in iter(node) : print(f"\t {attr} : {node.get(attr)}")

# Labels
def countLabels(driver : Driver, labels : List[str]) -> Dict[str, int] : 
    """Counts the occurrences of each label in the nodes

    Args:
        driver (Driver): access point to Neo4j
        labels (List[str]): list of labels

    Returns:
        Dict[str, int]: dictionary containing for each label, the number of occurencies
    """
    count_labels = {}
    for label in labels : count_labels[label] = countLabel(driver, label)
    return count_labels

def countLabel(driver : Driver, label : str) -> int : 
    """Counts the occurrences of the label in the nodes

    Args:
        driver (Driver): access point to Neo4j
        label (str): label to count

    Returns:
        int: number of occurencies
    """
    record, _, _ = driver.execute_query(
        "MATCH (n:" + label + ") WHERE size(labels(n)) = 1 RETURN COUNT(n) as count"
    )
    return record[0]['count']

def countLabeless(driver : Driver) -> int :
    """Counts the occurences of nodes without a label

    Args:
        driver (Driver): access point to Neo4j

    Returns:
        int: number of occurencies
    """
    record, _, _ = driver.execute_query(
        "MATCH (n) WHERE size(labels(n)) = 0 RETURN COUNT(n) as count"
    )
    return record[0]['count']   

def countMultipleLabelsNodes(driver : Driver) -> int :
    """Counts the number of nodes with multiple labels

    Args:
        driver (Driver): access point to Neo4j

    Returns:
        int: number of nodes with multiple labels
    """
    record, _, _ = driver.execute_query(
        "MATCH (n) WHERE size(labels(n)) > 1 RETURN COUNT(n) as count"
    )
    return record[0]['count'] 

def countPropertyLabelessNode(driver : Driver, property : str) -> int :
    """Counts the occurrences of nodes without labels for a given property.

    Args:
        driver (Driver): access point to Neo4j
        property (str): property to count

    Returns:
        int: number of occurrences
    """

    record, _, _ = driver.execute_query(
        f"MATCH (n) WHERE size(labels(n)) = 0 AND n.{property} IS NOT NULL RETURN COUNT(n) as count"
    )
    return record[0]['count']  

def countPropertyMultipleLabelsNode(driver : Driver, property : str) -> int :
    """Counts the occurrences of nodes with multiple labels for a given property.

    Args:
        driver (Driver): access point to Neo4j
        property (str): property to count

    Returns:
        int: number of occurrences
    """

    record, _, _ = driver.execute_query(
        f"MATCH (n) WHERE size(labels(n)) > 1 AND n.{property} IS NOT NULL RETURN COUNT(n) as count"
    )
    return record[0]['count']  

def deleteNodes(driver : Driver, label : str, batch_size = 2000) -> None :
    """Deletes all the nodes with the given label

    Args:
        driver (Driver): access point to Neo4j
        label (str): given label 
        batch_size (int, optional): number of operation in a transaction. Defaults to 2000.
    """
    count = countLabel(driver, label)
    while count > 0 :
        driver.execute_query(f"MATCH (n:{label}) WITH n LIMIT {batch_size} DETACH DELETE n")
        count -= batch_size

def deletePropertylessNodes(driver : Driver) -> None :
    """Deletes all nodes that do not have any labels or properties.

    Args:
        driver (Driver): access point to Neo4j
    """
    driver.execute_query(f"MATCH (n) WHERE size(labels(n)) = 0 AND size(keys(n)) = 0 WITH n DETACH DELETE n")

# Relationships
def countDBRelationships(driver : Driver) -> int :
    """Returns the number of relationships in the database

    Args:
        driver (Driver): access point to Neo4j

    Returns:
        int: number of relationships
    """
    record, _, _ = driver.execute_query(
        "MATCH (n)-->() RETURN count(*) as count"
    )
    return record[0]['count']

def countRelationships(driver : Driver, rels : List[str]) -> Dict[str, int] :
    """Returns the occurences of relationships for each types

    Args:
        driver (Driver): access point to Neo4j
        rels (List[str]): types of relationships

    Returns:
        Dict[str, int]: dictionary containing for each type, the number of occurencies
    """
    dictionary = {}
    for rel in rels : dictionary[rel] = countRelationship(driver, rel)
    return dictionary

def countRelationship(driver : Driver, label : str) -> int : 
    """Returns the number of relatinships with the given label

    Args:
        driver (Driver): access point to Neo4j
        label (str): given label
    Returns:
        int: number of relatinships with the given label
    """
    record, _, _ = driver.execute_query(
        "MATCH ()-[r:" + label + "]-() RETURN COUNT(r) as count"
    )
    return record[0]['count']

def getOutgoingRelationships(driver : Driver, labels : List[str]) -> Dict[str, List[Tuple[int, str, str, int]]] : 
    """Returns for each label, the list of outgoing relationships 

    Args:
        driver (Driver): access point to Neo4j
        labels (List[str]): list of labels

    Returns:
        Dict[str, List[Tuple[int, str, str, int]]]: _description_ #TODO
    """
    return __getRelationships(driver, labels, True)

def getIngoingRelationships(driver : Driver, labels : List[str]) -> Dict[str, List[Tuple[int, str, str, int]]] : 
    """Returns for each label, the list of ingoing relationships 

    Args:
        driver (Driver): access point to Neo4j
        labels (List[str]): list of labels

    Returns:
        Dict[str, List[Tuple[int, str, str, int]]]: _description_ #TODO
    """
    return __getRelationships(driver, labels, False)

def __getRelationships(driver : Driver, labels : List[str], out : bool) -> Dict[str, List[Tuple[int, str, str, int]]] :
    """Returns for each label, the list of ingoing/outgoing relationships 

    Args:
        driver (Driver): access point to Neo4j
        labels (List[str]): list of labels
        out (bool): true if outgoing relationships else ingoing relationships

    Returns:
        Dict[str, List[Tuple[int, str, str, int]]]: _description_ #TODO
    """
    rel = ""
    dictionary = {}
    for label in labels :
        if out : rel = "-[r]->"
        else : rel = "<-[r]-"
        res, _, _ = driver.execute_query(
            f"MATCH (n1: {label}){rel}(n2) RETURN labels(n2) AS label, TYPE(r) AS rel, COUNT(*) AS count"
        )
        relations = []
        if len(res) > 0 : 
            for relation in res :
                if out : rel = f"-[:{relation['rel']}]->"
                else :   rel = f"<-[:{relation['rel']}]-"
                count, _, _ = driver.execute_query(
                    f"MATCH (p: {label}) WHERE NOT (p){rel}() RETURN COUNT(*) as nocount"
                )
                relations.append((relation['count'], relation['rel'], relation['label'][0], count[0]['nocount']))
        dictionary[label] = relations
    return dictionary

# Properties
def countProperties(driver : Driver, properties : List[str]) -> Dict[str, List[Tuple[int, str]]] :
    """Returns for each property, the number of occurencies for each label of nodes

    Args:
        driver (Driver): access point to Neo4j
        properties (List[str]): list of properties

    Returns:
        Dict[str, List[Tuple[int, str]]]: for each property contains the occurences in each node with a label
    """
    count_properties = {}
    for property in properties :
        res, _, _ = driver.execute_query(
            f"MATCH (n) WHERE n.{property} IS NOT NULL RETURN COUNT(n) as count, LABELS(n) as labels"
        )
        count_properties[property] = [(count['count'], count['labels']) for count in res]
    return count_properties

def countPropertiesRels(driver : Driver, properties : List[str]) -> Dict[str, Tuple[int, str]] :
    """Returns for each property, the number of occurencies for each type of relationship

    Args:
        driver (Driver): access point to Neo4j
        properties (List[str]): list of properties

    Returns:
        Dict[str, Tuple[int, str]]: for each property contains the occurences in each relationship with a type
    """
    count_properties = {}
    for property in properties :
        res, _, _ = driver.execute_query(
            f"MATCH ()-[n]-() WHERE n.{property} IS NOT NULL RETURN COUNT(n) as count, TYPE(n) as type"
        )
        count_properties[property] = [(count['count'], count['type']) for count in res]
    return count_properties

def countPropertyNode(driver : Driver, property : str, label : str) -> int :
    """Returns the number of occurencies of the properity in nodes with the given label

    Args:
        driver (Driver): access point to Neo4j
        property (str): property to count
        label (str): given label for the nodes

    Returns:
        int: number of occurencies
    """
    record, _, _ = driver.execute_query(
        f"MATCH (n:{label}) WHERE size(labels(n)) = 1 AND n.{property} IS NOT NULL RETURN COUNT(n) as count"
    )
    return record[0]['count']

def countPropertyRel(driver : Driver, property : str, rel : str) -> int :
    """Returns the number of occurencies of the properity in relationships with the given label

    Args:
        driver (Driver): access point to Neo4j
        property (str): key of the property to count
        rel (str): given type for the relationship

    Returns:
        int: number of occurencies
    """
    record, _, _ = driver.execute_query(
        f"MATCH ()-[r:{rel}]->() WHERE r.{property} IS NOT NULL RETURN COUNT(r) as count"
    )
    return record[0]['count']

def countDistintValueNodes(driver : Driver, label : str, property : str) -> int :
    """Returns the number of distinct values of the property in nodes with the given label

    Args:
        driver (Driver): access point to Neo4j
        label (str): given label for the nodes
        property (str): property to count
        
    Returns:
        int: number of distinct values
    """
    record, _, _ = driver.execute_query(
        f"MATCH (n:{label}) WHERE size(labels(n)) = 1 AND n.{property} IS NOT NULL RETURN COUNT(DISTINCT n.{property}) as count"
    )
    return record[0]['count']

def countDistintValueLabelessNodes(driver : Driver, property : str) -> int :
    """Returns the number of distinct values of the property in nodes without labels

    Args:
        driver (Driver): access point to Neo4j
        property (str): property to count

    Returns:
        int: number of distinct values
    """
    record, _, _ = driver.execute_query(
        f"MATCH (n) WHERE size(labels(n)) = 0 AND n.{property} IS NOT NULL RETURN COUNT(DISTINCT n.{property}) as count"
    )
    return record[0]['count']

def countDistintValueMultipleLabelsNodes(driver : Driver, property : str) -> int :
    """Returns the number of distinct values of a property in nodes with multiple labels.

    Args:
        driver (Driver): access point to Neo4j
        property (str): property to count

    Returns:
        int: number of distinct values
    """
    record, _, _ = driver.execute_query(
        f"MATCH (n) WHERE size(labels(n)) > 1 AND n.{property} IS NOT NULL RETURN COUNT(DISTINCT n.{property}) as count"
    )
    return record[0]['count']

def countDistintValueRels(driver : Driver, rel : str, property : str) -> int :
    """Returns the number of distinct values of the relationships in nodes with the given type

    Args:
        driver (Driver): access point to Neo4j
        property (str): key of the property to count
        rel (str): given type for the relationship

    Returns:
        int: number of distinct values
    """
    record, _, _ = driver.execute_query(
        f"MATCH ()-[r:{rel}]->() WHERE r.{property} IS NOT NULL RETURN COUNT(DISTINCT r.{property}) as count"
    )
    return record[0]['count']

def getValuesNodes(driver : Driver, label : str, property : str) -> List[Record] :
    """Returns the list of all the pair (id, value) of the given property in nodes

    Args:
        driver (Driver): access point to Neo4j
        label (str): label of the nodes
        property (str): key of the property

    Returns:
        List[Record]: list of record with (id, value)
    """
    res, _, _ = driver.execute_query(
        f"MATCH (n:{label}) WHERE n.{property} IS NOT NULL RETURN elementId(n), n.{property}"
    )
    return res

def getValuesRels(driver : Driver, rel : str, property : str) -> List[Record] :
    """Returns the list of all the pair (id, value) of the given property in relationships

    Args:
        driver (Driver): access point to Neo4j
        rel (str): type of relation
        property (str): key of the property

    Returns:
        List[Record]: list of record with (id, value)
    """
    res, _, _ = driver.execute_query(
        f"MATCH ()-[n:{rel}]->() WHERE n.{property} IS NOT NULL RETURN elementId(n), n.{property}"
    )
    return res

def getDistinctValuesNodes(driver : Driver, label : str, prop : str) -> List[Record] :
    """Returns all the distinct value of a property in nodes with a given label

    Args:
        driver (Driver): access point to Neo4j
        label (str): label of nodes
        prop (str): key of the property

    Returns:
        List[Record]: list of record with (prop)
    """
    res, _, _ = driver.execute_query(f"MATCH (n:{label}) WHERE size(labels(n)) = 1 AND n.{prop} IS NOT NULL RETURN DISTINCT n.{prop} as prop")
    return res

def getDistinctValuesLabelessNodes(driver : Driver, prop : str) -> List[Record] :
    """Returns all the distinct value of a property in nodes with a given label

    Args:
        driver (Driver): access point to Neo4j
        prop (str): key of the property

    Returns:
        List[Record]: list of record with (prop)
    """
    res, _, _ = driver.execute_query(f"MATCH (n) WHERE size(labels(n)) = 0 AND n.{prop} IS NOT NULL RETURN DISTINCT n.{prop} as prop")
    return res

def getDistinctValuesMultipleLabelsNodes(driver : Driver, prop : str) -> List[Record] :
    """Returns all the distinct value of a property in nodes with multiple labels

    Args:
        driver (Driver): access point to Neo4j
        prop (str): key of the property

    Returns:
        List[Record]: list of record with (prop)
    """
    res, _, _ = driver.execute_query(f"MATCH (n) WHERE size(labels(n)) > 1 AND n.{prop} IS NOT NULL RETURN DISTINCT n.{prop} as prop")
    return res

def getDistinctValuesRels(driver : Driver, rel : str, prop : str) -> List[Record] :
    """Returns all the distinct value of a property in relationships with a given type

    Args:
        driver (Driver): access point to Neo4j
        rel (str): type of relationships
        prop (str): key of the property

    Returns:
        List[Record]: list of record with (prop)
    """
    res, _, _ = driver.execute_query(f"MATCH ()-[n:{rel}]->() WHERE n.{prop} IS NOT NULL RETURN DISTINCT n.{prop} as prop")
    return res

def updateValueRels(driver : Driver, rel : str, property : str, oldvalue : Any, newvalue : Any, batch_size = 2000) -> None : 
    """Update the value of property in relationships with the given type

    Args:
        driver (Driver): access point to Neo4j
        rel (str): type of relationships
        property (str): key of the property
        oldvalue (Any): old value of the property
        newvalue (Any): new value of the property
        batch_size (int, optional): number of update in a transaction. Defaults to 2000.
    """
    count = driver.execute_query(f"MATCH ()-[r:{rel}]->() WHERE r.{property} = \"{oldvalue}\" RETURN COUNT(*)")
    count = count[0][0][0]
    while count > 0 :
        driver.execute_query(
            f"MATCH ()-[r:{rel}]->() WHERE r.{property} = \"{oldvalue}\" WITH r LIMIT {batch_size} SET r.{property} = \"{newvalue}\""
        )
        count -= batch_size

def updateValueNodes(driver : Driver, label : str, property : str, oldvalue : Any, newvalue : Any, batch_size = 2000) -> None : 
    """Update the value of property in relationships with the given label

    Args:
        driver (Driver): access point to Neo4j
        label (str): label of the nodes
        property (str): key of the property
        oldvalue (Any): old value of the property
        newvalue (Any): new value of the property
        batch_size (int, optional): number of update in a transaction. Defaults to 2000.
    """
    count = driver.execute_query(f"MATCH (n:{label}) WHERE size(labels(n)) = 1 AND n.{property} = \"{oldvalue}\" RETURN COUNT(*)")
    count = count[0][0][0]
    while count > 0 :
        driver.execute_query(
            f"MATCH (n:{label}) WHERE size(labels(n)) = 1 AND n.{property} = \"{oldvalue}\" WITH n LIMIT {batch_size} SET n.{property} = \"{newvalue}\""
        )
        count -= batch_size

def updateValueLabelessNodes(driver : Driver, property : str, oldvalue : Any, newvalue : Any, batch_size = 2000) -> None : 
    """Update the value of property in nodes without label

    Args:
        driver (Driver): access point to Neo4j
        property (str): key of the property
        oldvalue (Any): old value of the property
        newvalue (Any): new value of the property
        batch_size (int, optional): number of update in a transaction. Defaults to 2000.
    """
    count = driver.execute_query(f"MATCH (n) WHERE size(labels(n)) = 0 AND n.{property} = \"{oldvalue}\" RETURN COUNT(*)")
    count = count[0][0][0]
    while count > 0 :
        driver.execute_query(
            f"MATCH (n) WHERE size(labels(n)) = 0 AND n.{property} = \"{oldvalue}\" WITH n LIMIT {batch_size} SET n.{property} = \"{newvalue}\""
        )
        count -= batch_size
    
def updateValueMultipleLabelsNodes(driver : Driver, property : str, oldvalue : Any, newvalue : Any, batch_size = 2000) -> None : 
    """Update the value of property in nodes with multiple labels

    Args:
        driver (Driver): access point to Neo4j
        property (str): key of the property
        oldvalue (Any): old value of the property
        newvalue (Any): new value of the property
        batch_size (int, optional): number of update in a transaction. Defaults to 2000.
    """
    count = driver.execute_query(f"MATCH (n) WHERE size(labels(n)) > 1 AND n.{property} = \"{oldvalue}\" RETURN COUNT(*)")
    count = count[0][0][0]
    while count > 0 :
        driver.execute_query(
            f"MATCH (n) WHERE size(labels(n)) > 1 AND n.{property} = \"{oldvalue}\" WITH n LIMIT {batch_size} SET n.{property} = \"{newvalue}\""
        )
        count -= batch_size

def removePropertyNodes(driver : Driver, label : str, property : str, batch_size = 2000) :
    """Remove the property in the nodes with the given label

    Args:
        driver (Driver): access point to Neo4j
        label (str): label of the node
        property (str): property to remove
        batch_size (int, optional): number of update in a transaction. Defaults to 2000.
    """
    count = countPropertyNode(driver, property, label) 
    while count > 0 :
        query = f"""MATCH (n:{label}) WHERE n.{property} IS NOT NULL WITH n LIMIT {batch_size} 
                    MATCH (q) WHERE elementId(q) = elementId(n) remove q.{property}"""
        driver.execute_query(query)
        count -= batch_size

def removePropertyLabelessNodes(driver : Driver, property : str, batch_size = 2000) :
    """Remove the property in the nodes with the given label

    Args:
        driver (Driver): access point to Neo4j
        label (str): label of the node
        property (str): property to remove
        batch_size (int, optional): number of update in a transaction. Defaults to 2000.
    """
    count = countPropertyLabelessNode(driver, property) 
    while count > 0 :
        query = f"""MATCH (n) WHERE size(labels(n)) = 0 AND n.{property} IS NOT NULL WITH n LIMIT {batch_size} 
                    MATCH (q) WHERE elementId(q) = elementId(n) remove q.{property}"""
        driver.execute_query(query)
        count -= batch_size

def removePropertyMultipleLabelsNodes(driver : Driver, property : str, batch_size = 2000) :
    """Remove the property in the nodes with multiple labels

    Args:
        driver (Driver): access point to Neo4j
        label (str): label of the node
        property (str): property to remove
        batch_size (int, optional): number of update in a transaction. Defaults to 2000.
    """
    count = countPropertyMultipleLabelsNode(driver, property) 
    while count > 0 :
        query = f"""MATCH (n) WHERE size(labels(n)) > 1 AND n.{property} IS NOT NULL WITH n LIMIT {batch_size} 
                    MATCH (q) WHERE elementId(q) = elementId(n) remove q.{property}"""
        driver.execute_query(query)
        count -= batch_size

def removePropertyRels(driver : Driver, rel : str, property : str, batch_size = 2000) :
    """Remove the property in the relationships with the given type

    Args:
        driver (Driver): access point to Neo4j
        rel (str): type of the relation
        property (str): property to remove
        batch_size (int, optional): number of update in a transaction. Defaults to 2000.
    """
    count = countPropertyRel(driver, property, rel) 
    while count > 0 :
        query = f"""MATCH ()-[r:{rel}]->() WHERE r.{property} IS NOT NULL WITH r LIMIT {batch_size} 
                    MATCH ()-[q]->() WHERE elementId(q) = elementId(r) remove q.{property}"""
        driver.execute_query(query)
        count -= batch_size