from typing import List
from thefuzz import process
from thefuzz import fuzz

class Context :
    warning_keywords = {
        "health" : ["health", "disease", "vaccine"],
        "geolocalization" : ["address", "latitude", "longitude", "post", "zip"],
        "finance" : ["creditcard", "income", "expense", "cost", "revenue", "balance", "bank", "pay"],
        "contact" : ["email", "phone", "contact"],
        "anagraphic" : ["birth", "born", "death", "died", "age"],
        "identification" : ["ssn", "nhs", "pass", "license", "name"],
        "biometric" : ["gender", "ethnic", "race", "skin", "sex"],
        "social" : ["religion", "orientation", "partner", "wife", "husband", "live", "work", "job", "role"]
    }
    def __init__(self, contexts : List[str], all = False) :
        """Create an instance of Context

        Args:
            contexts (List[str]): list of contexts. Can be in the default contexts or not
            all (bool, optional): true to includes all the default contexts. Defaults to False.
        """
        if all : return
        warning_keywords = {}
        for context in contexts :
            if context in self.warning_keywords.keys() :
                warning_keywords[context] = self.warning_keywords[context]
            else : warning_keywords[context] = []
        self.warning_keywords = warning_keywords

    def addKeyword(self, context : str, keywords : List[str]) -> None :
        """Add the keywords in the list to the context

        Args:
            context (str): context that can be in the default contexts or not
            keywords (List[str]): keywords to add
        """
        if context in self.warning_keywords.keys() :
            for keyword in keywords : self.warning_keywords[context].append(keyword)
        else : self.warning_keywords[context] = keywords

    def removeKeyword(self, context : str, keywords : List[str]) -> None :
        """Remove the keywords in the list to the context

        Args:
            context (str): context that can be in the default contexts or not
            keywords (List[str]): keywords to remove
        """
        if context in self.warning_keywords.keys() :
            for keyword in keywords : self.warning_keywords[context].remove(keyword)

    def removeContext(self, context : str) -> None:
        """Removes a context from the context list.

        Args:
            context (str): The context to remove.
        """
        if context in self.warning_keywords.keys() : del self.warning_keywords[context]

    def getContexts(self) -> List[str]:
        """Get all the contexts

        Returns:
            List[str]: list of contexts
        """
        return list(self.warning_keywords.keys())

    def evalInContext(self, list : List[str]) -> List[str] : 
        """Returns a subset of the given list with only the words recognized in one of the context
        Args:
            list (List[str]): contains the words to be evaluated

        Returns:
            List[str]: contains the words in the contexts
        """
        warning_list = [x for xs in self.warning_keywords.values() for x in xs]
        to_return = []
        for item in list : 
            tokens = item.split("_")
            for token in tokens :
                res = process.extractOne(token.lower(), warning_list, score_cutoff=90, scorer=fuzz.WRatio)
                if res is not None : 
                    # print(item, "similar to", res[0], res[1])
                    to_return.append(item)
                    break
        return to_return