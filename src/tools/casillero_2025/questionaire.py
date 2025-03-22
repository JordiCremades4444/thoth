import os
import random

import yaml
from PIL import Image


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


def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        exit(1)


def ensure_picture_exists(folder_path, picture_number):
    picture_path = f"{folder_path}/{picture_number}.png"
    if not os.path.exists(picture_path):
        print(f"Error: Picture '{picture_path}' does not exist.")
        exit(1)


def main():
    # Load configuration
    config = load_config()
    pictures_folder = config.get("pictures_folder")
    start_number = config.get("start_number")
    end_number = config.get("end_number")
    number_of_pictures = config.get("number_of_pictures")

    ensure_folder_exists(pictures_folder)

    # Question loop
    for i in range(0, number_of_pictures):
        random_number = random.randint(start_number, end_number)
        print(f"({i+1}/{number_of_pictures}) Random Number: {random_number}")

        input("Press Enter to see the image...")

        ensure_picture_exists(pictures_folder, random_number)

        try:
            with Image.open(f"{pictures_folder}/{random_number}.png") as img:
                img.show()
        except Exception as e:
            print(f"Error displaying image '{random_number}.png': {e}")
            exit(1)


if __name__ == "__main__":
    main()
