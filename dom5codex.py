import argparse
import pypandoc
import os
import pathlib



def compile(folder, content_path=None, content_list_file="content.txt"):
    """Recursively merge all files in folder together.

    If there is content file, use only files and folders in that file."""
    if not content_path:
        content_path = tempfile_path(folder)

    # initialize content_list
    content_list = get_content_list(folder, content_list_file)
    content_list = parse_content_list(content_list, content_list_file)
    merge_files(content_list, content_list)


def tempfile_path(folder):
    filename = "_".join(os.path.normpath(folder).split(os.path.sep)) + ".md"
    return os.path.join("tmp", filename)


def get_content_list(folder, content_file):
    content_file_path = os.path.join(folder, content_file)
    if os.path.isfile(content_file_path):
        content_list = read_file(content_file_path)
    else:
        content_list = list_dir_with_path(folder)
    return content_list


def read_file(file):
    with open(file) as f:
        text = f.read().splitlines()
    return text


def list_dir_with_path(folder):
    return [os.path.join(folder, item) for item in os.listdir(folder)]


def parse_content_list(content_list, content_list_file):
    for i, item in enumerate(content_list):
        suffix = pathlib.Path(item).suffix
        if suffix == "":
            # item is folder
            item_content_file = tempfile_path(folder)
            compile(item, content_list_file=content_list_file)
            content_list[i] = item_content_file
        elif suffix == ".md"
            # everything OK
            pass
        elif suffix == ".txt"
            # possible content file
            raise RuntimeError("Should " + item + " be a file with content list?")
        else:
            raise RuntimeError("Unknown extension. Only .md files or folders"
                    " are allowed. Found: " + item)







def build():
    compile()
    pass #TODO


def serve():
    pass #TODO


