import os
import shutil
from textnode import TextNode, TextType


def main():
    copy_content()


def clear_public():
    for item in os.listdir("public"):
        path = os.path.join("public", item)
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)


def copy_content():
    shutil.rmtree("public", ignore_errors=True)
    files = find_files("static")
    for file in files:
        path = file.split("/")
        if len(path) > 2:
            new_path = f'public/{"/".join(path[1:-1])}'
            os.makedirs(new_path, exist_ok=True)
        shutil.copy(file, f'public/{"/".join(path[1:])}')


def find_files(folder):
    res = []
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            res.append(path)
        else:
            res.extend(find_files(path))
    return res


main()
