from typing import Any, Callable, Dict, List, Self, Tuple
from neo4j import Driver
from .encrypt import random_key
from . import neo4j_utility
from .context import Context
from .sanitizationKeyword import sanitization_brutal_delete, sanitization_encrypt, sanitization_faker
from .sanitizationNer import sanitization_anonimize, sanitization_ner_encrypt, sanitization_ner_faker, sanitization_suppression

class Neo4jSanitizer : 
    models : Dict[str, Tuple[str, List[str]]] = {
        "geolocalization" : ("en_core_web_lg", ["GPE"], False),
        "identification" : ("en_core_web_lg", ["PERSON"], True),
        "health" : ("en_ner_bc5cdr_md" , ["DISEASE", "CHEMICAL"], True)
    }
    def __init__(self : Self, driver : Driver, 
                 keyword_context_node : Context, keyword_context_rels : Context, 
                 ner_context_node : Context, ner_context_rels : Context,
                 batch_size = 10000) -> Self :
        """Inizialization of the class

        Args:
            self (Self): instance of the class
            driver (Driver): access point to Neo4j
            keyword_context_node (Context): contexts to use for the sanitization strategy in nodes considering the keywords
            keyword_context_rels (Context): contexts to use for the sanitization strategy in relationships considering the keywords
            ner_context_node (Context): contexts to use for the sanitization strategy in nodes using ner models
            ner_context_rels (Context): contexts to use for the sanitization strategy in relationships using ner models

        Returns:
            Self: instance of the class
        """
        self.driver : Driver = driver
        self.keyword_context_node : Context = keyword_context_node
        self.keyword_context_rels : Context = keyword_context_rels
        self.ner_context_node : Context = ner_context_node
        self.ner_context_rels : Context = ner_context_rels
        self.aes_key : bytes = random_key()
        self.hmac_key : bytes = random_key()
        if batch_size <= 0 : raise Exception("Batch size must be positive")
        self._batch_size : int = batch_size
        self.getInfoFromDb()

    def getInfoFromDb(self : Self) -> None :
        """Get all the information from the database needed for sanitization

        Args:
            self (Self): instance of the class
        """
        print("Counting nodes and relationships...")
        self.countNodes : int = neo4j_utility.countDBNodes(self.driver)
        self.countRelationships : int = neo4j_utility.countDBRelationships(self.driver)
        print("Profiling the database...")
        self.nodes_properties, self.relationships_properties, self.labels, self.relationships = neo4j_utility.db_profiling(self.driver)
        print("Getting outgoing/ingoing relationships...")
        self.outgoing_relationships : Dict[str, List[Tuple[int, str, str, int]]] = neo4j_utility.getOutgoingRelationships(self.driver, self.labels)
        self.ingoing_relationships : Dict[str, List[Tuple[int, str, str, int]]] = neo4j_utility.getIngoingRelationships(self.driver, self.labels)
        print("Eval properties keys...")
        self.__classify_properties()
        
    def __classify_properties(self : Self) -> None :
        """Evaluate the properties of the databases into warning or not and 
           then classify each one as always included in the node/relationship or optional

        Args:
            self (Self): instance of the class
        """
        self.warning_properties = self.keyword_context_node.evalInContext(self.nodes_properties)
        self.warning_properties_in_rel = self.keyword_context_rels.evalInContext(self.relationships_properties)
        self.classified_properties_nodes = {}
        for label in self.labels :
            if neo4j_utility.countLabel(self.driver, label) > 0 :
                self.classified_properties_nodes[label] = (
                    self.__classify_property_in_node(label, self.warning_properties), 
                    self.__classify_property_in_node(label, [prop for prop in self.nodes_properties if prop not in self.warning_properties])
                )
        self.classified_properties_rels = {}
        for rel in self.relationships : 
            self.classified_properties_rels[rel] = (
                self.__classify_property_in_rel(rel, self.warning_properties_in_rel), 
                self.__classify_property_in_rel(rel, [prop for prop in self.relationships_properties if prop not in self.warning_properties_in_rel])
            )
        
    def print_info(self : Self) -> None :
        """Print the info got with getInfoFromDb()

        Args:
            self (Self): instance of the class
        """
        print("countNodes:", self.countNodes)
        print("countRelationships", self.countRelationships)
        print("properties", self.nodes_properties)
        print("labels", self.labels)
        print("relationships", self.relationships)
        print("outgoing_relationships", self.outgoing_relationships)
        print("ingoing_relationships", self.ingoing_relationships)

    def show_info(self : Self) -> None :
        """Better visualization of the infos got with getInfoFromDb()

        Args:
            self (Self): instance of the class
        """
        print("Nodes in db:", self.countNodes)
        print("Relationships in db:", self.countRelationships)
        print("Properties in nodes:", self.nodes_properties)
        print("Properties in relationships:", self.relationships_properties)
        print("Labels:", self.labels)
        print("Relationships:", self.relationships)

        #########
        # Labels analysis
        #########

        print()
        # Given a warning label, count the type of relationship what go out to/in a specific label
        print(" - Outgoing relationships analyses")
        for label, relation in self.outgoing_relationships.items() :
            if len(relation) == 0 : print("No outgoing relation for", label)
            else :
                total = 0
                for rel in relation : total += rel[0] 
                print("from", label, "there are", total, "outgoing relationship with:")
                for rel in relation :
                    count = neo4j_utility.countLabel(self.driver, label)
                    if count > 0 :
                        print(f"\t {rel[1]} to {rel[2]} times {rel[0]} {format(rel[0] / total, '.2%')} of outgoing relationship; no rel in {rel[3]} nodes {format(rel[3]/count, '.2%')}")

        print()
        print(" - Ingoing relationships analyses")    
        for label, relation in self.ingoing_relationships.items() :
            if len(relation) == 0 : print("No ingoing relation for", label)
            else :
                total = 0
                for rel in relation : total += rel[0] 
                print("to", label, "there are", total, "ingoing relationship with:")
                for rel in relation :
                    count = neo4j_utility.countLabel(self.driver, label)
                    if count > 0 : 
                        print(f"\t {rel[1]} from {rel[2]} times {rel[0]} {format(rel[0] / total, '.2%')} of ingoing relationship; no rel in {str(rel[3])} nodes {format(rel[3]/count, '.2%')}")

        #########
        # Properties analysis
        #########
        # Count the warning property and what's label of the node
        print()
        print(" - Warning properties analyses")
        for key, ((warning_always, warning_optional), (always, optional)) in self.classified_properties_nodes.items() :
            if len(warning_always)>0 or len(warning_optional)>0 or len(always)>0 or len(optional)>0 :
                print("In label", key)
                if len(warning_always) > 0 : 
                    print("\talways warning") 
                    for prop, count in warning_always : print("\t\t", prop, count)
                if len(warning_optional) > 0 : 
                    print("\toptional warning")
                    for prop, count in warning_optional : print("\t\t", prop, count)
                if len(always) > 0 : 
                    print("\talways no warning")
                    for prop, count in always : print("\t\t", prop, count)
                if len(optional) > 0 : 
                    print("\toptional no warning")
                    for prop, count in optional : print("\t\t", prop, count)

        if neo4j_utility.countLabeless(self.driver) > 0 :
            print("\nIn labeless nodes:")
            for property in self.nodes_properties :
                n = neo4j_utility.countPropertyLabelessNode(self.driver, property)
                if n > 0 : 
                    if property in self.warning_properties :
                        print("\twarning", property, n)
                    else : print("\tno warning", property, n)
        
        if neo4j_utility.countMultipleLabelsNodes(self.driver) > 0 :
            print("\nIn nodes with multiple labels:")
            for property in self.nodes_properties :
                n = neo4j_utility.countPropertyMultipleLabelsNode(self.driver, property)
                if n > 0 :
                    if property in self.warning_properties :
                        print("\twarning", property, n)
                    else : print("\tno warning", property, n)

        for key, ((warning_always, warning_optional), (always, optional)) in self.classified_properties_rels.items() :
            if len(warning_always)>0 or len(warning_optional)>0 or len(always)>0 or len(optional)>0 :
                print("In rel", key)
                if len(warning_always) > 0 : 
                    print("\talways warning") 
                    for prop, count in warning_always : print("\t\t", prop, count)
                if len(warning_optional) > 0 : 
                    print("\toptional warning")
                    for prop, count in warning_optional : print("\t\t", prop, count)
                if len(always) > 0 : 
                    print("\talways no warning")
                    for prop, count in always : print("\t\t", prop, count)
                if len(optional) > 0 : 
                    print("\toptional no warning")
                    for prop, count in optional : print("\t\t", prop, count)
        # Outliners
        #######
        # Count the node without labels and to what node with labels are in relation
        print()
        print(" - Node without labels:", neo4j_utility.countLabeless(self.driver))

        # Central Node (node with max number of relationships)
        print()
        print(" - Central Node")
        node = neo4j_utility.findCentralNode(self.driver)
        if node == None : print("No central node found")
        else :
            neo4j_utility.printNodeInfo(node['node'])
            print("In relation with", node['count'], "nodes")

        # Isoleted Nodes (no relationships)
        print()
        isolatedNodes = neo4j_utility.findIsolatedNodes(self.driver)
        print(" - Isolated Nodes:", len(isolatedNodes))
        print()
    
    def __classify_property_in_node(self : Self, label : str, properties : List[str]) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]] :
        """Classify each property in nodes with the given label, as always included in the node or optional

        Args:
            self (Self): instance of the class
            label (str): label of the nodes
            properties (List[str]): list of properties

        Returns:
            Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]: 
            returns two lists
            - the list of the always included warning properties with their occurencies and the optional included warning properties with their occurencies 
            - the list of the always included non warning properties with their occurencies and the optional included non warning properties with their occurencies 
        """
        always = []
        optional = []
        count_label = neo4j_utility.countLabel(self.driver, label)
        for prop in properties :
            times = neo4j_utility.countPropertyNode(self.driver, prop, label)
            if times == count_label : always.append((prop, times))
            elif times > 0 : optional.append((prop, times))
        return (always, optional)
    
    def __classify_property_in_rel(self, relation : str, properties : List[str]) -> Tuple[List[str], List[Tuple[str, int]]] :  
        """Classify each property in relationships with the given type, as always included in the relationship or optional

        Args:
            self (Self): instance of the class
            relation (str): type of relationship
            properties (List[str]): list of properties

        Returns:
            Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]: 
            returns two lists
            - the list of the always included warning properties with their occurencies and the optional included warning properties with their occurencies 
            - the list of the always included non warning properties with their occurencies and the optional included non warning properties with their occurencies 
        """
        always = []
        optional = []
        count_rel = neo4j_utility.countRelationship(self.driver, relation)
        for prop in properties :
            times = neo4j_utility.countPropertyRel(self.driver, prop, relation)
            if times == count_rel : always.append((prop, times))
            elif times > 0 : optional.append((prop, times))
        return (always, optional)

    ###############
    # Sanitizations
    ############### 
    def sanitization_brutal_delete(self : Self) -> None :
        """Sanitize all the detected warning properties by removing them in nodes and relationship. 
           If there are no other properties in the node, it'll be deleted
        Args:
            self (Self): instance of the class
        """
        sanitization_brutal_delete(self, batch_size = self._batch_size)
        print("Updating info of the database...")
        self.getInfoFromDb()
    
    def sanitization_encrypt(self : Self) -> None : 
        """Sanitize all the detected warning properties by encrypting their values. 
        The keys used are accessible by self.aes_key and self.hmac_key.

        Args:
            self (Self): instance of the class
        """
        sanitization_encrypt(self, batch_size = self._batch_size)
        print("aes_key:", self.aes_key)
        print("hmac_key:", self.hmac_key)
        print("Updating info of the database...")
        for label, ((encrypted1, encrypted2), (l1, l2)) in self.classified_properties_nodes.items() :
            self.classified_properties_nodes[label] = (([], []), (l1 + encrypted1, l2 + encrypted2))
        for label, ((encrypted1, encrypted2), (l1, l2)) in self.classified_properties_rels.items() :
            self.classified_properties_rels[label] = (([], []), (l1 + encrypted1, l2 + encrypted2))

    def sanitization_faker(self : Self, fakers : List[Tuple[str, Callable[[], Any]]]) -> None :
        """Sanitize all the properties for which has been given a faker function

        Args:
            self (Self): instance of the class
            fakers (List[Tuple[str, Callable[[], Any]]]): list of Tuple containing
            - key of the property
            - function that returns a random value for the property
        """
        fakers_list = []
        for prop, faker in fakers :
            if prop in self.nodes_properties + self.relationships_properties :
                fakers_list.append((prop, faker)) 
            else : print("Property", prop, "not in the database instance")
        sanitization_faker(self, fakers_list, batch_size = self._batch_size)
    
    def sanitization_ner_suppression(self : Self, blacklist = [], multiprocessing = False) -> None :
        """Sanitize all the entities recognized by NER models by replacing the entity with *.

        Args:
            self (Self): instance of the class
            blacklist (list, optional): list of properties to ignore in NER process. Defaults to [].
            multiprocessing (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.
        """
        sanitization_suppression(self, blacklist = blacklist, batch_size = self._batch_size, multiprocessing = multiprocessing)

    def sanitization_ner_anonimize(self : Self, blacklist = [], multiprocessing = False) -> None :
        """Sanitize all the entities recognized by NER models by replacing the entity with its label.

        Args:
            self (Self): instance of the class
            blacklist (list, optional): list of properties to ignore in NER process. Defaults to [].
            multiprocessing (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.
        """
        sanitization_anonimize(self, blacklist = blacklist, batch_size = self._batch_size, multiprocessing = multiprocessing)

    def sanitization_ner_encrypt(self : Self, blacklist = [], multiprocessing = False) -> None :
        """Sanitize all the entities recognized by NER models by replacing the entity with its encrypted value.
        The keys used are accessible by self.aes_key and self.hmac_key.

        Args:
            self (Self): instance of the class
            blacklist (list, optional): list of properties to ignore in NER process. Defaults to [].
            multiprocessing (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.
        """
        sanitization_ner_encrypt(self, blacklist = blacklist, batch_size = self._batch_size, multiprocessing = multiprocessing)
        print("aes_key:", self.aes_key)
        print("hmac_key:", self.hmac_key)

    def sanitization_ner_faker(self : Self, fakers : Dict[str, Callable[[], str]], blacklist = [], multiprocessing = False) -> None :
        """Sanitize all the entities recognized by NER models by replacing the entity with a random value provided by a faker method.
        If the faker for the label of the entity is not provided, the entity value will be replaced with "*".

        Args:
            self (Self): instance of the class
            fakers (Dict[str, Callable[[], str]]): lists for each label of entity, a method f() -> str that returns a random value for the label
            blacklist (list, optional): list of properties to ignore in NER process. Defaults to [].
            multiprocessing (bool, optional): Whether to use multiprocessing for sanitization. Defaults to False.
        """
        self.fakers = fakers
        sanitization_ner_faker(self, blacklist = blacklist, batch_size = self._batch_size, multiprocessing = multiprocessing)

    def __tot_properties(self : Self) -> int :
        tot = 0
        for label, ((warning_always, warning_optional), (always, optional)) in self.classified_properties_nodes.items() :
            tot += neo4j_utility.countLabel(self.driver, label) * (len(warning_always) + len(always))
            for _, count in warning_optional+optional : tot += count
        for label, ((warning_always, warning_optional), (always, optional)) in self.classified_properties_rels.items() :
            tot += neo4j_utility.countRelationship(self.driver, label) * (len(warning_always) + len(always))
            for _, count in warning_optional+optional : tot += count
        return tot
    
    def estimate_sanitizationKeyword(self : Self) -> int :
        """Estimate the number of property affected by any of the sanitization that use the keyword

        Args:
            self (Self): instance of the class

        Returns:
            int: number of property
        """
        tot = 0
        for _, ((warning_always, warning_optional), _) in self.classified_properties_nodes.items() :
            for _, count in warning_always + warning_optional : tot += count
        for _, ((warning_always, warning_optional), _) in self.classified_properties_rels.items() :
            for _, count in warning_always + warning_optional : tot += count
        for prop in self.warning_properties : tot += neo4j_utility.countPropertyLabelessNode(self.driver, prop)
        for prop in self.warning_properties : tot += neo4j_utility.countPropertyMultipleLabelsNode(self.driver, prop)
        return tot
    
    def estimate_sanitizationNer(self : Self, blacklist = []) -> int :
        """Estimate the number of distinct values affected by any of the sanitization that use the NER
        Note: numeric values are included in this counting but skipped in the NER sanitization

        Args:
            self (Self): instance of the class
            blacklist (list, optional): list of properties to ignore in NER process. Defaults to [].

        Returns:
            int: number of distinct values
        """
        tot = 0
        for label, ((warning_always, warning_optional), (always, optional)) in self.classified_properties_nodes.items() :
            for prop, _ in warning_always + warning_optional + always + optional :
                if prop in blacklist : continue
                tot += neo4j_utility.countDistintValueNodes(self.driver, label, prop)
        for label, ((warning_always, warning_optional), (always, optional)) in self.classified_properties_rels.items() :
            for prop, _ in warning_always + warning_optional + always + optional :
                if prop in blacklist : continue
                tot += neo4j_utility.countDistintValueRels(self.driver, label, prop)
        for prop in self.warning_properties : tot += neo4j_utility.countDistintValueLabelessNodes(self.driver, prop)
        for prop in self.warning_properties : tot += neo4j_utility.countDistintValueMultipleLabelsNodes(self.driver, prop)
        return tot