def read(table_name: str):
    with open(f"data/{table_name}.json", "r") as file:
        return file.read()