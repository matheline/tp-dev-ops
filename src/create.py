def create(table_name: str):
    with open(f"data/{table_name}.json", "w") as file:
        file.write("[]")