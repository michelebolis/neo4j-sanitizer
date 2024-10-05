from typing import Callable, List, Tuple
from .encrypt import encrypt_list
from . import neo4j_utility

def sanitization_brutal_delete(sanitizer, batch_size = 2000) -> None :
    """
    Perform brutal deletion of warning properties in nodes and relationships.
    
    Args:
        sanitizer: The sanitizer containing information about warning properties and relationships.
        batch_size (optional): The number of items to process in each batch. Defaults to 2000.
    
    Returns:
        None
    """
    print("Starting the sanitization (brutal delete) in nodes for contexts", sanitizer.keyword_context_rels.getContexts())
    for label, ((warning_always, warning_optional), (always, optional)) in sanitizer.classified_properties_nodes.items() :
        warning_always = [p2 for p2, _ in warning_always]
        warning_optional = [p2 for p2, _ in warning_optional]
        if (len(warning_optional) + len(warning_always) == 0) : continue
        print("Nodes with Label:", label)
        if len(always) == 0 and len(optional) == 0 : 
            print("\tThere are no properties other than the warning ones: delete all the relationships and then the node")
            neo4j_utility.deleteNodes(sanitizer.driver, label, batch_size = batch_size)
        if len(warning_optional) > 0 : 
            print("\tRemove the", len(warning_optional), "optional warning properties")
            for prop in warning_optional : neo4j_utility.removePropertyNodes(sanitizer.driver, label, prop, batch_size = batch_size)
        if len(warning_always) > 0 :
            print("\tThere are properties other than the warning ones: remove only the warning properties")
            for prop in warning_always : neo4j_utility.removePropertyNodes(sanitizer.driver, label, prop, batch_size = batch_size)
    
    if neo4j_utility.countLabeless(sanitizer.driver) == 0 : print("No labeless nodes to handle")
    else :
        for property in sanitizer.warning_properties : 
            if neo4j_utility.countDistintValueLabelessNodes(sanitizer.driver, property) == 0 : continue
            neo4j_utility.removePropertyLabelessNodes(sanitizer.driver, property, batch_size = batch_size)
        neo4j_utility.deletePropertylessNodes(sanitizer.driver)

    if neo4j_utility.countMultipleLabelsNodes(sanitizer.driver) == 0 : print("No multiple labels nodes to handle")
    else :
        for property in sanitizer.warning_properties : 
            if neo4j_utility.countDistintValueMultipleLabelsNodes(sanitizer.driver, property) == 0 : continue
            neo4j_utility.removePropertyLabelessNodes(sanitizer.driver, property, batch_size = batch_size)
        neo4j_utility.deletePropertylessNodes(sanitizer.driver)

    print("Starting the sanitization (brutal delete) in relationships for contexts", sanitizer.keyword_context_rels.getContexts())
    for rel, ((warning_always, warning_optional), _) in sanitizer.classified_properties_rels.items() :
        if not(len(warning_optional) > 0 or len(warning_always) > 0) : continue
        print("Relation with label", rel)
        print("\tRemoving the", len(warning_always) + len(warning_optional), "warning properties")
        for prop, _ in warning_always + warning_optional : neo4j_utility.removePropertyRels(sanitizer.driver, rel, prop, batch_size = batch_size)

def sanitization_encrypt(sanitizer, batch_size = 2000) -> None : 
    """
    Perform the sanitization process by encrypting data in nodes and relationships.

    Args:
        sanitizer (Neo4jSanitizer): The sanitizer object containing info.
        batch_size (int, optional): The batch size for updating the data. Defaults to 2000.

    Returns:
        None
    """
    print("Starting the sanitization (encrypt) in nodes for contexts", sanitizer.keyword_context_node.getContexts())
    for label, ((warning_always, warning_optional), _) in sanitizer.classified_properties_nodes.items() :
        if not(len(warning_optional) > 0 or len(warning_always) > 0) : continue
        props_nodes = [prop for prop, _ in warning_optional + warning_always]
        __encrypt_properties_in_nodes(sanitizer, props_nodes, label)

    for property in sanitizer.warning_properties :
        if neo4j_utility.countDistintValueLabelessNodes(sanitizer.driver, property) == 0 : continue
        res = neo4j_utility.getDistinctValuesLabelessNodes(sanitizer.driver, property)
        newTexts = encrypt_list(res, sanitizer.aes_key, sanitizer.hmac_key)
        print("Executing update for", property, "in labeless nodes")
        for i, newText in enumerate(newTexts) :
            neo4j_utility.updateValueLabelessNodes(sanitizer.driver, property, res[i][0], newText, batch_size = batch_size)
    
    for property in sanitizer.warning_properties :
        if neo4j_utility.countDistintValueMultipleLabelsNodes(sanitizer.driver, property) == 0 : continue
        res = neo4j_utility.getDistinctValuesMultipleLabelsNodes(sanitizer.driver, property)
        newTexts = encrypt_list(res, sanitizer.aes_key, sanitizer.hmac_key)
        print("Executing update for", property, "in multiple labels nodes")
        for i, newText in enumerate(newTexts) :
            neo4j_utility.updateValueMultipleLabelsNodes(sanitizer.driver, property, res[i][0], newText, batch_size = batch_size)

    print("Starting the sanitization (encrypt) in relationships for contexts", sanitizer.keyword_context_rels.getContexts())
    for rel, ((warning_always, warning_optional), _) in sanitizer.classified_properties_rels.items() :
        if not(len(warning_optional) > 0 or len(warning_always) > 0) : continue
        props_rels = [prop for prop, _ in warning_optional + warning_always]
        __encrypt_properties_in_rels(sanitizer, props_rels, rel)

def __encrypt_properties_in_nodes(sanitizer, to_encrypt : List[str], label : str, batch_size = 2000) -> None:
    """
    Encrypt properties in nodes based on the provided parameters.

    Args:
        sanitizer (Neo4jSanitizer): The sanitizer containing the data to be sanitized.
        to_encrypt (List[str]): A list of properties to be encrypted.
        label (str): The label of the nodes to be updated.
        batch_size (int, optional): The number of values to process in each batch. Defaults to 2000.

    Returns:
        None
    """
    for property in to_encrypt :
        res = neo4j_utility.getDistinctValuesNodes(sanitizer.driver, label, property)
        newTexts = encrypt_list(res, sanitizer.aes_key, sanitizer.hmac_key)
        print("Executing update for", property, "in", label)
        for i, newText in enumerate(newTexts) :
            neo4j_utility.updateValueNodes(sanitizer.driver, label, property, res[i][0], newText, batch_size = batch_size)

def __encrypt_properties_in_rels(sanitizer, to_encrypt : List[str], rel : str, batch_size = 2000) -> None:
    """
    Encrypt properties in relationships based on the provided parameters.

    Args:
        sanitizer (Neo4jSanitizer): The sanitizer containing the data to be sanitized.
        to_encrypt (List[str]): A list of properties to be encrypted.
        rel (str): The relationship type to be updated.
        batch_size (int, optional): The number of values to process in each batch. Defaults to 2000.

    Returns:
        None
    """
    for property in to_encrypt :
        res = neo4j_utility.getDistinctValuesRels(sanitizer.driver, rel, property)
        newTexts = encrypt_list(res, sanitizer.aes_key, sanitizer.hmac_key)
        print("Executing update for", property, "in", rel)
        for i, newText in enumerate(newTexts) :
            neo4j_utility.updateValueRels(sanitizer.driver, rel, property, res[i][0], newText, batch_size = batch_size)

def sanitization_faker(sanitizer, fakers : List[Tuple[str, Callable[[], str]]], batch_size = 2000) -> None : 
    """
    A function that performs sanitization using faker functions on nodes and relationships for given properties.

    Args:
        sanitizer: The sanitizer containing the data to be sanitized.
        fakers: A list of tuples containing the property key and a function that returns a random value for the property.
        batch_size (int, optional): The number of values to process in each batch. Defaults to 2000.

    Returns:
        None
    """
    print("Starting the sanitization (by fakers) in nodes and relationships for properties", [prop for prop, _ in fakers])
    for prop, faker in fakers :
        labels = neo4j_utility.countProperties(sanitizer.driver, [prop])[prop]
        for _, label in labels :
            if len(label) == 0 :
                res = neo4j_utility.getDistinctValuesLabelessNodes(sanitizer.driver, prop)
                for value in res :
                    neo4j_utility.updateValueLabelessNodes(sanitizer.driver, prop, value[0], faker(), batch_size = batch_size)
            elif len(label) == 1 :
                res = neo4j_utility.getDistinctValuesNodes(sanitizer.driver, label[0], prop)
                for value in res :
                    neo4j_utility.updateValueNodes(sanitizer.driver, label[0], prop, value[0], faker(), batch_size = batch_size)
            else : 
                res = neo4j_utility.getDistinctValuesMultipleLabelsNodes(sanitizer.driver, prop)
                for value in res :
                    neo4j_utility.updateValueMultipleLabelsNodes(sanitizer.driver, prop, value[0], faker(), batch_size = batch_size)
        if len(labels) > 0 : 
            print(f"Updated value of {prop} with fakers in nodes")
        else : print(f"No value of {prop} in nodes")
        dict = neo4j_utility.countPropertiesRels(sanitizer.driver, [prop])
        rels = dict[prop]
        for rel in rels :
            res = neo4j_utility.getDistinctValuesRels(sanitizer.driver, rel[1], prop)
            for value in res : 
                neo4j_utility.updateValueRels(sanitizer.driver, rel[1], prop, value[0], faker(), batch_size = batch_size)
        if len(dict[prop]) > 0 : 
            print(f"Updated value of {prop} with fakers in relationships")
        else : print(f"No value of {prop} in relationships")