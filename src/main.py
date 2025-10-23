import os
import shutil
import sys

from copy_static import copy_static
from generate_page import recursively_generate_pages

dir_path_static = os.path.abspath("./static")
dir_path_public = os.path.abspath("./docs")
dir_path_content = os.path.abspath("./content")
template_path = os.path.abspath("./template.html")
base_path = sys.argv[1] if len(sys.argv) >= 2 else "/"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_static(dir_path_static, dir_path_public)

    print("Generating pages...")
    recursively_generate_pages(
        dir_path_content,
        template_path,
        dir_path_public,
        base_path,
    )


if __name__ == "__main__":
    main()
