import argparse
#import pypandoc
import os
import pathlib


class Content():
    def __init__(self, folder, result=None):
        self.folder = folder
        self.result = result
        self.temp_path = "tmp"
        self.content_file = "content.txt"
        if not self.result:
            self.remake_result_path()

    def remake_result_path(self):
        self.result = tempfile_path(self.folder, self.temp_path)

    def subcontent(self, folder):
        subcontent = Content(folder)
        subcontent.temp_path = self.temp_path
        subcontent.content_file = self.content_file
        subcontent.remake_result_path()
        return subcontent

    def compile(self):
        self.content_list = self.get_content_list()
        self.parse_content_list()
        merge_files(self.content_list, self.result)

    def get_content_list(self):
        content_file_path = os.path.join(self.folder, self.content_file)
        if os.path.isfile(content_file_path):
            content_list = self.get_content_list_from_file(content_file_path)
        else:
            content_list = list_dir_with_path(self.folder)
        return content_list

    def get_content_list_from_file(self, content_file_path):
        content_list = read_file(content_file_path)
        content_list = [os.path.join(self.folder, item) for item in content_list]
        return content_list

    def parse_content_list(self):
        for i, item in enumerate(self.content_list):
            suffix = pathlib.Path(item).suffix
            if suffix == "":
                # item is folder
                subcontent = self.subcontent(item)
                subcontent.compile()
                self.content_list[i] = subcontent.result
            elif suffix == ".md":
                # everything OK
                pass
            elif suffix == ".txt":
                # possible content file
                raise RuntimeError("Should " + item + " be a file with content list?")
            else:
                raise RuntimeError("Unknown extension. Only .md files or folders"
                        " are allowed. Found: " + item)


def tempfile_path(folder, temp_path):
    filename = "_".join(os.path.normpath(folder).split(os.path.sep))
    return os.path.join(temp_path, filename + ".md")

def read_file(file):
    with open(file) as f:
        text = f.read().splitlines()
    return text

def list_dir_with_path(folder):
    return [os.path.join(folder, item) for item in os.listdir(folder)]

def merge_files(files, result):
    mkdir(os.path.dirname(result))
    with open(result, "w") as result_file:
        for file in files:
            text = read_file(file)
            result_file.write("\n".join(text) + "\n")


def mkdir(folder):
    if not folder == "" and not os.path.exists(folder):
        os.makedirs(folder)


def get_parser():
    parser = argparse.ArgumentParser(
        prog="dom5Codex.py",
        description=(
            ""
            )
        )
    parser.add_argument("-c", "--compile", action="store_true",
        help="Compile individual markdown files into a single document"
        )
    parser.add_argument("-b", "--build", action="store_true",
        help="Build a HTML for web browsing"
        )
    parser.add_argument("--pdf", action="store_true",
        help="Build a PDF file"
        )
    parser.add_argument("--html", action="store_true",
        help="Build a HTML file for local browsing"
        )
    return(parser)


def compile():
    Content("content", "dom5codex.md").compile()


def build():
    compile()
    pass #TODO


def build_pdf():
    compile()
    pass #TODO


def build_local_html():
    compile()
    pass #TODO


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    if args.compile:
        compile()
    elif args.build:
        build()
    elif args.pdf:
        build_pdf()
    elif args.html:
        build_local_html()
    else:
        parser.print_help()
        parser.exit(1)
