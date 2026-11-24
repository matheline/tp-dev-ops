from create import insertOne, insertMany
from read import read, find, findOne

# Exemple de find
# print(find("table1", {"age":24}))

# Exemple de find avec filtre simple
# print(find("table1", { "age": { "$gte": 18 }}))

# Exemple de find avec filtre imbriqué
# print(find("table1", { "$or": [{ "age": 18 }, { "nom": "Henry" }] }))