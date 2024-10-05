import base64
import multiprocessing
from typing import Any, Callable, Dict, List, Tuple
from neo4j import Driver, Record
import spacy
from . import neo4j_utility
from .encrypt import encrypt_with_key

def sanitization_suppression(sanitizer, blacklist = [], batch_size = 2000, multiprocessing = False) -> None :
    """
    Perform sanitization suppression on nodes and relationships

    Args:
        sanitizer (Neo4jSanitizer): The sanitizer containing the data to be sanitized.
        blacklist (List[str], optional): A list of properties to be excluded from sanitization. Defaults to an empty list.
        batch_size (int, optional): The number of values to process in each batch. Defaults to 2000.
        multiprocessing (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.

    Returns:
        None
    """
    count = 0
    if multiprocessing : sanitize = __sanitization_ner_multiprocessing
    else :  sanitize = __sanitization_ner
    contexts = [context for context in sanitizer.ner_context_node.getContexts() if context in sanitizer.models.keys()]
    print("Starting the sanitization (ner suppression) in nodes for contexts", contexts)
    count += sanitize(sanitizer, __properties_occurency(sanitizer.classified_properties_nodes, blacklist), contexts,
                       neo4j_utility.getDistinctValuesNodes, neo4j_utility.updateValueNodes, 
                       __ner_suppression, batch_size = batch_size)
    
    if neo4j_utility.countLabeless(sanitizer.driver) > 0 :
        print("Starting the sanitization (ner suppression) in nodes without label for contexts", contexts)
        count += sanitize(sanitizer, [(p, "") for p in sanitizer.nodes_properties if p not in blacklist], contexts,
                        __getterLabelessNodes, __updateLabelessNodes, 
                        __ner_suppression, batch_size = batch_size)
    
    if neo4j_utility.countMultipleLabelsNodes(sanitizer.driver) > 0 :
        print("Starting the sanitization (ner suppression) in nodes with multiple labels for contexts", contexts)
        count += sanitize(sanitizer, [(p, "") for p in sanitizer.nodes_properties if p not in blacklist], contexts,
                            __getterMultipleLabelsNodes, __updateMultipleLabelsNodes, 
                            __ner_suppression, batch_size = batch_size)

    contexts = [context for context in sanitizer.ner_context_rels.getContexts() if context in sanitizer.models.keys()]
    print("Starting the sanitization (ner suppression) in relationships for contexts", contexts)
    count += sanitize(sanitizer, __properties_occurency(sanitizer.classified_properties_rels, blacklist), contexts,
                       neo4j_utility.getDistinctValuesRels, neo4j_utility.updateValueRels, 
                       __ner_suppression, batch_size = batch_size)
    
    print("Inspected", count, "values with NER models")
    
def sanitization_anonimize(sanitizer, blacklist = [], batch_size = 2000, multiprocessing = False) -> None :
    """
    Perform sanitization (ner anonimize) on nodes and relationships

    Args:
        sanitizer (Neo4jSanitizer): The sanitizer containing the data to be sanitized.
        blacklist (List[str], optional): A list of properties to be excluded from sanitization. Defaults to an empty list.
        batch_size (int, optional): The number of values to process in each batch. Defaults to 2000.
        multiprocessing (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.

    Returns:
        None
    """
    count = 0
    if multiprocessing : sanitize = __sanitization_ner_multiprocessing
    else :  sanitize = __sanitization_ner
    contexts = [context for context in sanitizer.ner_context_node.getContexts() if context in sanitizer.models.keys()]
    print("Starting the sanitization (ner anonimize) in nodes for contexts", contexts)
    count += sanitize(sanitizer, __properties_occurency(sanitizer.classified_properties_nodes, blacklist), contexts,
                       neo4j_utility.getDistinctValuesNodes, neo4j_utility.updateValueNodes, 
                       __ner_anonimize, batch_size = batch_size)
    
    if neo4j_utility.countLabeless(sanitizer.driver) > 0 :
        print("Starting the sanitization (ner anonimize) in nodes without label for contexts", contexts)
        count += sanitize(sanitizer, [(p, "") for p in sanitizer.nodes_properties if p not in blacklist], contexts,
                            __getterLabelessNodes, __updateLabelessNodes, 
                            __ner_anonimize, batch_size = batch_size)
    
    if neo4j_utility.countMultipleLabelsNodes(sanitizer.driver) > 0 :
        print("Starting the sanitization (ner anonimize) in nodes with multiple labels for contexts", contexts)
        count += sanitize(sanitizer, [(p, "") for p in sanitizer.nodes_properties if p not in blacklist], contexts,
                            __getterMultipleLabelsNodes, __updateMultipleLabelsNodes, 
                            __ner_anonimize, batch_size = batch_size)

    contexts = [context for context in sanitizer.ner_context_rels.getContexts() if context in sanitizer.models.keys()]
    print("Starting the sanitization (ner anonimize) in relationships for contexts", contexts)
    count += sanitize(sanitizer, __properties_occurency(sanitizer.classified_properties_rels, blacklist), contexts,
                       neo4j_utility.getDistinctValuesRels, neo4j_utility.updateValueRels, 
                       __ner_anonimize, batch_size = batch_size)
    
    print("Inspected", count, "values with NER models")

def sanitization_ner_encrypt(sanitizer, blacklist = [], batch_size = 2000, multiprocessing = False) -> None :
    """
    Perform sanitization (ner encrypt) on nodes and relationships

    Args:
        sanitizer (Neo4jSanitizer): The sanitizer containing the data to be sanitized.
        blacklist (List[str], optional): A list of properties to be excluded from sanitization. Defaults to an empty list.
        batch_size (int, optional): The number of values to process in each batch. Defaults to 2000.
        multiprocessing (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.

    Returns:
        None
    """
    count = 0
    if multiprocessing : sanitize = __sanitization_ner_multiprocessing
    else :  sanitize = __sanitization_ner
    contexts = [context for context in sanitizer.ner_context_node.getContexts() if context in sanitizer.models.keys()]
    print("Starting the sanitization (ner encrypt) in nodes for contexts", contexts)
    count += sanitize(sanitizer, __properties_occurency(sanitizer.classified_properties_nodes, blacklist), contexts,
                       neo4j_utility.getDistinctValuesNodes, neo4j_utility.updateValueNodes, 
                       __ner_encrypt, batch_size = batch_size)
    
    if neo4j_utility.countLabeless(sanitizer.driver) > 0 :
        print("Starting the sanitization (ner encrypt) in nodes without label for contexts", contexts)
        count += sanitize(sanitizer, [(p, "") for p in sanitizer.nodes_properties if p not in blacklist], contexts,
                        __getterLabelessNodes, __updateLabelessNodes, 
                        __ner_encrypt, batch_size = batch_size)
    
    if neo4j_utility.countMultipleLabelsNodes(sanitizer.driver) > 0 :
        print("Starting the sanitization (ner encrypt) in nodes with multiple labels for contexts", contexts)
        count += sanitize(sanitizer, [(p, "") for p in sanitizer.nodes_properties if p not in blacklist], contexts,
                            __getterMultipleLabelsNodes, __updateMultipleLabelsNodes, 
                            __ner_encrypt, batch_size = batch_size)
    
    contexts = [context for context in sanitizer.ner_context_rels.getContexts() if context in sanitizer.models.keys()]
    print("Starting the sanitization (ner encrypt) in relationships for contexts", contexts)
    count += sanitize(sanitizer, __properties_occurency(sanitizer.classified_properties_rels, blacklist), contexts,
                       neo4j_utility.getDistinctValuesRels, neo4j_utility.updateValueRels, 
                       __ner_encrypt, batch_size = batch_size)
    
    print("Inspected", count, "values with NER models")
    
def sanitization_ner_faker(sanitizer, blacklist = [], batch_size = 2000, multiprocessing = False) -> None :
    """
    Perform sanitization (ner faker) on nodes and relationships

    Args:
        sanitizer (Neo4jSanitizer): The sanitizer containing the data to be sanitized.
        blacklist (List[str], optional): A list of properties to be excluded from sanitization. Defaults to an empty list.
        batch_size (int, optional): The number of values to process in each batch. Defaults to 2000.
        multiprocessing (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.

    Returns:
        None
    """
    count = 0
    if multiprocessing : sanitize = __sanitization_ner_multiprocessing
    else :  sanitize = __sanitization_ner
    contexts = [context for context in sanitizer.ner_context_node.getContexts() if context in sanitizer.models.keys()]
    print("Starting the sanitization (ner faker) in nodes for contexts", contexts)
    count += sanitize(sanitizer, __properties_occurency(sanitizer.classified_properties_nodes, blacklist), contexts,
                       neo4j_utility.getDistinctValuesNodes, neo4j_utility.updateValueNodes, 
                       __ner_faker, batch_size = batch_size)
    
    if neo4j_utility.countLabeless(sanitizer.driver) > 0 :
        print("Starting the sanitization (ner faker) in nodes without label for contexts", contexts)
        count += sanitize(sanitizer, [(p, "") for p in sanitizer.nodes_properties if p not in blacklist], contexts,
                        __getterLabelessNodes, __updateLabelessNodes, 
                        __ner_faker, batch_size = batch_size)
    
    if neo4j_utility.countMultipleLabelsNodes(sanitizer.driver) > 0 :
        print("Starting the sanitization (ner faker) in nodes with multiple labels for contexts", contexts)
        count += sanitize(sanitizer, [(p, "") for p in sanitizer.nodes_properties if p not in blacklist], contexts,
                            __getterMultipleLabelsNodes, __updateMultipleLabelsNodes, 
                            __ner_faker, batch_size = batch_size)
    
    contexts = [context for context in sanitizer.ner_context_rels.getContexts() if context in sanitizer.models.keys()]
    print("Starting the sanitization (ner faker) in relationships for contexts", contexts)
    count += sanitize(sanitizer, __properties_occurency(sanitizer.classified_properties_rels, blacklist), contexts,
                       neo4j_utility.getDistinctValuesRels, neo4j_utility.updateValueRels, 
                       __ner_faker, batch_size = batch_size)
    print("Inspected", count, "values with NER models")

def __getterLabelessNodes(driver, label : str, prop : str) :
    """
	Wrapper function for labeless nodes

	Args:
	    driver: access point to Neo4j
	    label: label of nodes
	    prop: key of the property

	Returns:
	    the result of getDistinctValuesLabelessNodes(driver, prop)
	"""
    return neo4j_utility.getDistinctValuesLabelessNodes(driver, prop)


def __updateLabelessNodes(driver, label : str, prop : str, oldText : str, newText : str, batch_size = 2000) :
    """
	Wrapper function for updating labeless nodes

	Args:
	    driver: access point to Neo4j
	    label: label of nodes
	    prop: key of the property
	    oldText: the old text that needs to be updated
	    newText: the new text to update to
	    batch_size: number of updates in a transaction. Defaults to 2000.

	Returns:
	    the result of updating the value of a property in nodes without a label
	"""
    return neo4j_utility.updateValueLabelessNodes(driver, prop, oldText, newText, batch_size = batch_size)

def __getterMultipleLabelsNodes(driver, label : str, prop : str) :
    """
	Wrapper function for multiple labels nodes

	Args:
	    driver: access point to Neo4j
	    label: label of nodes
	    prop: key of the property

	Returns:
	    the result of getDistinctValuesMultipleLabelsNodes(driver, prop)
	"""
    return neo4j_utility.getDistinctValuesMultipleLabelsNodes(driver, prop)


def __updateMultipleLabelsNodes(driver, label : str, prop : str, oldText : str, newText : str, batch_size = 2000) :
    """
	Wrapper function for updating for multiple labels nodes

	Args:
	    driver: access point to Neo4j
	    label: label of nodes
	    prop: key of the property
	    oldText: the old text that needs to be updated
	    newText: the new text to update to
	    batch_size: number of updates in a transaction. Defaults to 2000.

	Returns:
	    the result of updating the value of a property in nodes with multiple labels
	"""
    return neo4j_utility.updateValueMultipleLabelsNodes(driver, prop, oldText, newText, batch_size = batch_size)

def __properties_occurency(dict : Dict[Tuple[str, str], Any], blacklist : List[str]) -> List[str] :
    """
    Calculates the occurrences list of properties in a given dictionary, excluding properties in a blacklist.

    Args:
        dict (Dict[Tuple[str, str], Any]): A dictionary containing tuples as keys and any value as values.
        blacklist (List[str]): A list of properties to be excluded.

    Returns:
        List[str]: A list of tuples, where each tuple contains a property and its corresponding label.

    """
    properties_list = []
    for label, ((l1, l2), (l3, l4)) in dict.items() :
        for prop, _ in l1 + l2 + l3 + l4 :
            if prop not in blacklist : properties_list.append((prop, label))
    return properties_list

def __sanitization_ner(sanitizer, properties : List[Tuple[str, str]], contexts : List[str],
                       getterValues : Callable[[Driver, str, str], List[Record]], 
                       update : Callable[[Driver, str, str, List[Dict[str, Any]]], None], 
                       replace : Callable[[str], str], batch_size = 2000) -> int :
    """
    Function for sanitizing Named Entity Recognition (NER) data based on the provided properties, contexts, and functions for data retrieval and update.

    Args:
        sanitizer (Neo4jSanitizer): The sanitizer containing the data to be sanitized.
        properties: A list of tuples, each containing a property in nodes with a given label.
        contexts: A list of contexts to consider for sanitization.
        getterValues: A callable function to retrieve data records.
        update: A callable function to update data records.
        replace: A callable function to replace entities recognized in a text.
        batch_size: An integer representing the batch size for updating data.

    Returns:
        int: Total count of processed items.
    """
    print("Getting distinct values of properties...")
    data = {}
    tot = 0
    for prop, label in properties :
        res = getterValues(sanitizer.driver, label, prop)
        data[(prop, label)] = [({}, item["prop"]) for item in res]
    for context, (model, entity_labels, skip) in sanitizer.models.items() :
        if context not in contexts : continue
        print(f"Evaluating distinct values for context {context} with ner model {model}...")
        nlp_ner = spacy.load(model)
        for (prop, label), res in data.items() :
            for index, (oldEnts, oldText) in enumerate(res) :
                if skip and __is_numeric(oldText) : continue
                text = str(oldText)
                tot += 1
                ents = __ent_recognition(text, nlp_ner, entity_labels)
                for start, stop, recognizedLabel in ents :
                    if recognizedLabel == None : continue
                    if (start, stop) in oldEnts : 
                        oldEnts[(start, stop)] = oldEnts[(start, stop)].append(recognizedLabel)
                    else : oldEnts[(start, stop)] = [recognizedLabel]
                res[index] = (oldEnts, oldText)
    print("Updating values of properties...")
    for (prop, label), items in data.items() :
        for ents, oldText in items :
            if len(ents) == 0 : continue
            newText = __ent_sanitization(sanitizer, oldText, ents, replace)
            update(sanitizer.driver, label, prop, oldText, newText, batch_size = batch_size)
    return tot

def __sanitization_ner_multiprocessing(sanitizer, properties : List[Tuple[str, str]], contexts : List[str],
                       getterValues : Callable[[Driver, str, str], List[Record]], 
                       update : Callable[[Driver, str, str, List[Dict[str, Any]]], None], 
                       replace : Callable[[str], str], batch_size = 2000) -> int :
    """
    A function that performs sanitization using multiprocessing for a given set of properties. 
    Args:
        sanitizer: The sanitizer object.
        properties: A list of tuples containing property in nodes with a given label.
        contexts: A list of context strings.
        getterValues: A method that retrieves values using a driver, label, and property.
        update: A method that updates values using a driver, label, property, and a list of dictionaries.
        replace: A method that replaces entities recognized in a text.
        batch_size: An integer specifying the batch size for processing.
        
    Returns:
        An integer representing the total count of processed items.
    """
    print("Getting distinct values of properties...")
    data = {}
    for prop, label in properties :
        res = getterValues(sanitizer.driver, label, prop)
        data[(prop, label)] = [({}, item["prop"]) for item in res]
    newData, tot = __handle_multiprocessing(data, sanitizer, contexts)
    print("Updating values of properties...")
    for (prop, label), items in newData.items() :
        for ents, oldText in items :
            if len(ents) == 0 : continue
            newText = __ent_sanitization(sanitizer, oldText, ents, replace)
            update(sanitizer.driver, label, prop, oldText, newText, batch_size = batch_size)
    return tot
def __handle_multiprocessing(data : Dict[Tuple[str, str], Tuple[Tuple, List[str]]], sanitizer, contexts : List[str]) -> Tuple[Dict, int]:
    """
    Handles multiprocessing for the given data, sanitizer, and contexts.

    Args:
        data (dict): The data to be processed.
        sanitizer (Neo4jSanitizer): The sanitizer object.
        contexts (List[str]): The list of contexts to process.

    Returns:
        newData: updated data 
        tot: total count of processed items
    """
    newData = {}
    pool = multiprocessing.Pool()
    processes = [pool.apply_async(__apply_ner, args=(model, data, entity_labels, skip)) for context, (model, entity_labels, skip) in sanitizer.models.items() if context in contexts]
    result = [p.get() for p in processes]
    tot = 0
    for item, count in result:
        tot += count
        for key, value in item.items():
            if key in newData : newData[key].extend(value)
            else : newData[key] = value
    for (prop, label), items in newData.items() :
        newData[(prop, label)] = [(ents, oldText) for ents, oldText in items if len(ents) > 0]
    return newData, tot
def __apply_ner(model : str, data : Dict[Tuple[str, str], Tuple[Tuple, List[str]]], entity_labels : List[str], skip : bool) -> Tuple[Dict, int]:
    """
    Apply named entity recognition (NER) to a given data set.

    Args:
        model (str): The name of the NER model to use.
        data (dict): The data set to process.
        entity_labels (List[str]): The list of entity labels to recognize.
        skip (bool): Whether to skip processing numeric values.

    Returns:
        data: updated data set
        count: total count of processed items.
    """
    count = 0
    nlp_ner = spacy.load(model)
    for (_, _), res in data.items() :
        for index, (oldEnts, oldText) in enumerate(res) :
            if skip and __is_numeric(oldText) : continue
            text = str(oldText)
            count += 1
            ents = __ent_recognition(text, nlp_ner, entity_labels)
            for start, stop, recognizedLabel in ents :
                if recognizedLabel == None : continue
                if (start, stop) in oldEnts : 
                    oldEnts[(start, stop)] = oldEnts[(start, stop)].append(recognizedLabel)
                else : oldEnts[(start, stop)] = [recognizedLabel]
            res[index] = (oldEnts, oldText)
    return data, count

def __is_numeric(s : str) -> bool :
    """
    Check if the given string `s` is a numeric value.

    Parameters:
        s (str): The string to check.

    Returns:
        bool: True if the string is a numeric value, False otherwise.
    """
    try :
        float(s)
        return True
    except : 
        try :
            int(s)
            return True
        except : return False

def __ent_recognition(text : str, ner : spacy.Language, entity_labels : List[str]) :
    """
	Extracts entities from the given text using the specified NER model and the allowed entity labels.

	Parameters:
	    text (str): The text to extract entities from.
	    ner (spacy.Language): The NER model to use for entity recognition.
	    entity_labels (List[str]): The list of entity labels to extract.

	Returns:
	    List[Tuple[int, int, str]]: A list of tuples representing the start index, end index, and label of the recognized entities.
	"""
    doc = ner(text)
    ents = [(ent.start_char, ent.start_char + len(ent.text), ent.label_) for ent in doc.ents if ent.label_ in entity_labels]
    return ents

def __ent_sanitization(sanitizer, text : str, ents : Dict[Tuple[str, str], List[str]], 
                       replace : Callable[[str, List[str]], str]) -> str :
    """
    Sanitizes the given text by replacing the entities found by the NER model with the result of applying the given replace function to the entity text and labels.

    Parameters:
        sanitizer (Neo4jSanitizer): The sanitizer object used for context.
        text (str): The text to sanitize.
        ents (Dict[Tuple[str, str], List[str]]): A dictionary mapping entity start and end positions to a list of labels for each entity.
        replace (Callable[[str, List[str]], str]): The function to apply to each entity text and labels.

    Returns:
        str: The sanitized text.
    """
    newtext = ""
    prev = 0
    for (start, stop), labels in ents.items() : 
        for i in range(prev, start) :
            newtext += text[i]
        if labels == None : newtext += text[start : stop]
        else : newtext += replace(sanitizer, text[start : stop], labels)
        prev = stop
    newtext += text[prev: len(text)]
    return newtext

def __ner_suppression(sanitizer, text : str, labels : List[str]) -> str : 
    """
    Suppresses entities.

    Parameters:
        sanitizer (Neo4jSanitizer): The sanitizer object used for context. (Ignored)
        text (str): The text containing of the named entities to suppress. (Ignored)
        labels (List[str]): The list of entity labels to suppress. (Ignored)

    Returns:
        str: The text with suppressed named entities.
    """
    return "*"

def __ner_anonimize(sanitizer, text : str, labels : List[str]) -> str : 
    """
    Anonymizes named entities in the given text by concatenating the labels of the entities

    Parameters:
        sanitizer (Neo4jSanitizer): The sanitizer object used for context. (Ignored)
        text (str): The text containing named entities. (Ignored)
        labels (List[str]): The list of labels of the named entities.

    Returns:
        str: The anonymized text with labels concatenated with forward slashes.
    """
    s = ""
    if len(labels) == 1 : return labels[0]
    for label in labels : s += f"{label}/"
    return s
def __ner_faker(sanitizer, text : str, labels : List[str]) -> str : 
    """
    Generates a fake value for the given text and labels using the provided sanitizer object.

    Parameters:
        sanitizer (Neo4jSanitizer): The sanitizer object used for context. 
        text (str): The text containing named entities. (Ignored)
        labels (List[str]): The list of labels of the named entities.

    Returns:
        str: The generated fake value for the named entities, or "*" if no fake value is available.
    """
    for label in labels : 
        if label in sanitizer.fakers : return sanitizer.fakers[label]()
    return "*"
def __ner_encrypt(sanitizer, text : str, labels : List[str]) -> str : 
    """
    Encrypts the given text using the provided AES key and HMAC key.

    Args:
        sanitizer (Neo4jSanitizer): The sanitizer object used for context. 
        text (str): The text to be encrypted.
        labels (List[str]): The list of labels associated with the text. (Ignored)

    Returns:
        str: The encrypted text encoded in base64.
    """
    return str(base64.b64encode(encrypt_with_key(text, sanitizer.aes_key, sanitizer.hmac_key)), 'utf-8')