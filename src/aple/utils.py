import json
import yaml

def write_json_file(file_path, content: dict):
    try:
        with open(file_path, "w") as f:
            json.dump(content, f, indent=4)
    except IOError as e:
        print(f"Error writing to JSON file {file_path}: {e}")

def write_markdown_file(file_path, content: str):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        print(f"Error writing to Markdown file {file_path}: {e}")

def load_yaml(file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except (IOError, yaml.YAMLError) as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return None