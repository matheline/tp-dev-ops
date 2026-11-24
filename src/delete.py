import os

def delete(table_name: str):
    file_path = f"data/{table_name}.json"
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")