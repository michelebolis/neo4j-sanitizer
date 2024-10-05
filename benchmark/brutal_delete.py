import time
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from neo4j_sanitizer.neo4j_utility import connect
from neo4j_sanitizer.neo4j_sanitizer import Neo4jSanitizer
from neo4j_sanitizer.context import Context
# patientv5 
start = time.perf_counter()

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminadmin")
driver = connect(URI, AUTH, "neo4j")
context = Context([], all=True)

sanitizer = Neo4jSanitizer(driver, context, context, context, context, batch_size = 10000)
count = sanitizer.estimate_sanitizationKeyword()
sanitizer.sanitization_brutal_delete()
driver.close()

end = time.perf_counter()
print("Property deleted:", count)
print("Tempo: ",  end-start, "s") 
