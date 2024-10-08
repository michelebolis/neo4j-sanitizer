import time
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from neo4j_sanitizer.neo4j_utility import connect
from neo4j_sanitizer.neo4j_sanitizer import Neo4jSanitizer
from neo4j_sanitizer.context import Context
# patientv5 after brutal_delete multiprocessing
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminadmin")
driver = connect(URI, AUTH, "neo4j")
context = Context([], all=True)

sanitizer = Neo4jSanitizer(driver, context, context, context, context, batch_size = 10000)
sanitizer.sanitization_brutal_delete()
driver.close()

start = time.perf_counter()

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminadmin")
driver = connect(URI, AUTH, "neo4j")
context = Context([], all=True)

sanitizer = Neo4jSanitizer(driver, context, context, context, context, batch_size = 10000)
print()
sanitizer.sanitization_ner_suppression(blacklist=["id", "code", "date"])
driver.close()

end = time.perf_counter()
print("Tempo: ",  end-start, "s")  # 1964.91 s