
# Neo4jSanitizer

Neo4jSanitizer is a Python library for sanitize your Neo4j database instance in order to be published as microdata.  

To do so we define a list of `Context` each one associated with a list of keywords that represent what is a sensitive information. This will help us identify the propriety that must be sanitized, by sintax similarity.  
Another method to identify dangerous information, to prevent it from being published, is by using `NLPs models`, in our case [spaCy models](https://spacy.io/models). The portion of text to sanitize is the one identified as a NER model's entity.

We also provide a full collection of optiomized API to interact with the neo4j instance in case of self sanitization is preferred.

# Repository organization

- `neo4j_sanitizer`: contains the source code of the framework  
  - [neo4j_sanitizer.py](neo4j_sanitizer/neo4j_sanitizer.py): contains the main framework object
  - [context.py](neo4j_sanitizer/context.py): contains the Context object used to inizialized the framework
  - [neo4j_utility.py](neo4j_sanitizer/neo4j_utility.py): contains all the API used to interact with the db instance
  - [encrypt.py](neo4j_sanitizer/encrypt.py): contains the code used in the encrypt sanitization
  - [sanitizationKeyword.py](neo4j_sanitizer/sanitizationKeyword.py): contains the sanitizations which use the keyword concept
  - [sanitizationNer.py](neo4j_sanitizer/sanitizationNer): contains the sanitizations which use the NER models
- `doc`: contains the [documentation](doc/doc.md) for the code provided  
- `benchmark`: contains some scalability tests and related [statistics](benchmark/benchmarks.md)  
- `dumps`: contains the dumps of the dbs used in the benchmarks
  - [patient.dump](dumps/patient.dump): db containing synthetic provided by [Synthetic Mass](https://synthea.mitre.org/downloads)
  - [pole-50.dump](dumps/pole-50.dump) and [twitter-v2-50.dump](dumps/twitter-v2-50.dump) simple db examples provided by [Neo4j](https://github.com/neo4j-examples)
  - [esempio.dump](dumps/esempio.dump) dummy example
- `llm_test`: contains experimental [tests](llm_test/log_test.md) to integrade this framework with LLM models (ChatGPT, GeminiAI, Claude)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.

- [Neo4j API](https://neo4j.com/docs/python-manual/current/)

```bash
pip install neo4j
```

- For the string similarity evaluation [TheFuzz](https://github.com/seatgeek/thefuzz)

```bash
pip install thefuzz
```

- For the encrypt process [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)

```bash
pip install pycryptodome
```

- For the [multiprocessing](https://docs.python.org/3/library/multiprocessing.html#) feature

```bash
pip install multiprocessing
```

- For the NER [spaCy](https://spacy.io/) models  

```bash
pip install -U spacy
```

To install the recommended NER models:

- [en_core_web_lg](https://spacy.io/models/en#en_core_web_lg) provided by spaCy, used to identify person name and location

```bash
python -m spacy download en_core_web_lg
```

- [en_ner_bc5cdr_md](https://allenai.github.io/scispacy/) provided by ScispaCy to identify disease and chemical

```bash
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz
```

## Framework Usage

1. **Create a driver**

Create a driver instance to connect the client to your neo4j database

```python
from neo4j_sanitizer.neo4j_utility import connect
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminadmin")
driver = connect(URI, AUTH, "neo4j")
```

2. **Create the contexts**

You can simply use all the contexts and keywords provided by defaults simply using the optional argument `all`

```python
context = Context([], all=True)
```

Another option is to fully customize your set of contexts and keywords by using `addKeyword` / `removeKeyword` / `removeContext` methods

3. **Create the Neo4jSanitizer instance**

Create the instance of the sanitizer by giving a driver, 4 contexts for nodes (keywords sanitization), relationships (keyword sanitization), nodes (NER sanitization) and relationships (NER sanitization). You can also specify in batch_size the number of updates/deletes to be executed in a single transactions

```python
sanitizer = Neo4jSanitizer(driver, context, context, context, context, batch_size = 10000)
sanitizer.getInfoFromDb()
```

Now you can visualize the informations gathered by the sanitizer before choose which sanitization method to use.

You can also change the models to be used in the NER sanitization by customize the sanitizer.models attribute.

4. **Choose a sanitization methods**

The sanitization methods provided are:

- [sanitizationKeyword](neo4j_sanitizer/sanitizationKeyword.py)
  - sanitization_brutal_delete: remove all the properties identified as dangerous.
  - sanitization_encrypt: ecrypt all the properties identified as dangerous with AES.
  - sanitization_faker: replace the dangerous info with a random generated value.
- [sanitizationNER](neo4j_sanitizer/sanitizationNer.py)
  - sanitization_suppression: replace the identified entity with `*`.
  - sanitization_anonimize: replace the identified entity with the label of the entity (es. "John" become "PERSON").
  - sanitization_ner_encrypt: ecrypt all the entities identified with AES.
  - sanitization_ner_faker: replace the identified entity with a random generated value.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](LICENCE)
