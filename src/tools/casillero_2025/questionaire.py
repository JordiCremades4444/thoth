import json
import os
import random

import yaml


def load_config(config_path="config.yaml"):
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        exit(1)


def ensure_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        exit(1)


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: JSON file '{file_path}' not found.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
        exit(1)


def main():
    # Load configuration
    config = load_config()

    json_file_path = config.get("casillero_file")
    number_of_questions = config.get("number_of_questions")

    ensure_file_exists(json_file_path)

    data = load_json(json_file_path)

    # Loop number_of_questions times and select a random item each time
    for i in range(1, number_of_questions + 1):
        selected_item = random.choice(list(data.items()))
        print(f"({i}/{number_of_questions}) Selected Key: {selected_item[0]}")
        input("Press Enter to continue...")
        print(f"Value: {selected_item[1]}")


if __name__ == "__main__":
    main()
