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


def get_image_files(folder_path):
    try:
        files = [
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        if not files:
            print(f"Error: No image files found in folder '{folder_path}'.")
            exit(1)
        return files
    except Exception as e:
        print(f"Error accessing folder '{folder_path}': {e}")
        exit(1)


def main():
    # Load configuration
    config = load_config()
    pictures_folder = config.get("pictures_folder")
    number_of_pictures = config.get("number_of_pictures")

    ensure_folder_exists(pictures_folder)

    # Get all image files in the folder
    image_files = get_image_files(pictures_folder)

    # Question loop
    for i in range(0, number_of_pictures):
        random_file = random.choice(image_files)
        print(f"({i+1}/{number_of_pictures}) Random File: {random_file}")

        input("Press Enter to see the image...")

        try:
            with Image.open(os.path.join(pictures_folder, random_file)) as img:
                img.show()
        except Exception as e:
            print(f"Error displaying image '{random_file}': {e}")
            exit(1)


if __name__ == "__main__":
    main()
