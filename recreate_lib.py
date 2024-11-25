import json


with open('storage_schema.json', 'r') as f:
    cont = json.load(f)
    print(cont)
with open('library.json', 'w') as f:
    f.write(json.dumps(cont))
