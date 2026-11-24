def insertOne(table_name: str):
    with open(f"data/{table_name}.json", "w") as file:
        file.write("[]")
        
def insertMany(table_names: list[str]):
    for t in table_names:
        with open(f"data/{t}.json", "w") as file:
            file.write("[]")