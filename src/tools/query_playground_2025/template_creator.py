import os
import shutil


def copy_template():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "templates", "template.ipynb")
    destination_path = os.path.join(current_dir, "000.ipynb")
    shutil.copy(template_path, destination_path)


def main():
    copy_template()


if __name__ == "__main__":
    main()
