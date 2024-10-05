import time
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from neo4j_sanitizer.neo4j_utility import connect
from neo4j_sanitizer.neo4j_sanitizer import Neo4jSanitizer
from neo4j_sanitizer.context import Context
from neo4j_sanitizer import neo4j_utility
# patientv5 

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminadmin")
driver = connect(URI, AUTH, "neo4j")
context = Context([], all=True)

sanitizer = Neo4jSanitizer(driver, context, context, context, context, batch_size = 10000)
distinct_values = 0
for prop in sanitizer.warning_properties : 
    for label in sanitizer.labels :
        distinct_values += neo4j_utility.countDistintValueNodes(sanitizer.driver, label, prop)
    distinct_values += neo4j_utility.countDistintValueLabelessNodes(sanitizer.driver, prop)
    distinct_values += neo4j_utility.countDistintValueMultipleLabelsNodes(sanitizer.driver, prop)
for prop in sanitizer.warning_properties_in_rel : 
    for rel in sanitizer.relationships : 
        distinct_values += neo4j_utility.countDistintValueRels(sanitizer.driver, rel, prop)

driver.close()

start = time.perf_counter()

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminadmin")
driver = connect(URI, AUTH, "neo4j")
context = Context([], all=True)

sanitizer = Neo4jSanitizer(driver, context, context, context, context, batch_size = 10000)
count = sanitizer.estimate_sanitizationKeyword()
sanitizer.sanitization_faker([(prop, lambda : "test") for prop in sanitizer.warning_properties+sanitizer.warning_properties_in_rel])
driver.close()

end = time.perf_counter()
print("Property changed:", count) # 237878
print("Distinct values replaced:", distinct_values) # 45398
print("Tempo: ",  end-start, "s") # 
