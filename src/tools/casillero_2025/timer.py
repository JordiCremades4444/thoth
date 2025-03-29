import random
import time

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


def main():
    print("Welcome to the Number Trainer!")

    # Load configuration
    config = load_config()

    # Get lower and upper bounds from the configuration
    lower_bound = config.get("lower_bound", 0)  # Default to 0 if not specified
    upper_bound = config.get("upper_bound", 99)  # Default to 99 if not specified

    # Ask how many numbers to show
    try:
        num_questions = int(input("How many numbers should I show? "))
    except ValueError:
        print(
            "Invalid input. Please enter an integer value for the number of questions."
        )
        return

    # Get user input for the timer duration
    try:
        seconds = int(input("Enter the number of seconds to wait between numbers: "))
    except ValueError:
        print("Invalid input. Please enter an integer value for seconds.")
        return

    # Loop to show the numbers
    for i in range(1, num_questions + 1):
        print(f"Waiting for {seconds} seconds...")
        time.sleep(seconds)  # Wait for the specified number of seconds

        # Generate and display a random number
        random_number = random.randint(lower_bound, upper_bound)
        print(f"Number ({i}/{num_questions}) is {random_number}")


if __name__ == "__main__":
    main()
