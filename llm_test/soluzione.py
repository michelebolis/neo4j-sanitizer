import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from neo4j_sanitizer.neo4j_utility import connect
from neo4j_sanitizer.neo4j_sanitizer import Neo4jSanitizer
from neo4j_sanitizer.context import Context

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminadmin")
driver = connect(URI, AUTH, "neo4j")
context = Context([], all=True)
context.addKeyword("identification", ["first", "last"])
context.addKeyword("geolocation", ["city"])
context.addKeyword("finance", ["amount"])

sanitizer = Neo4jSanitizer(driver, context, context, context, context, batch_size = 10000)
sanitizer.show_info()
print("Value affected by sanitization using keyword:", sanitizer.estimate_sanitizationKeyword())
print("Value not affected by sanitization using keyword:", sanitizer.estimate_NON_sanitizationKeyword())
print()
driver.close()