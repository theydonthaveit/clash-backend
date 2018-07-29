from neo4j.v1 import GraphDatabase

db = GraphDatabase.driver(
    "bolt://0.0.0.0:7687",
    auth=(
        "OverpowAdmin",
        "a@28090aW" ))
