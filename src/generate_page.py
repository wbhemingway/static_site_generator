import os

from markdown import extract_title, markdown_to_html_node


def generate_page(
    from_path: str, template_path: str, dest_path: str, base_path: str
) -> str:
    print(f" * {from_path} {template_path} -> {dest_path}")

    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'scr="{base_path}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    to_file = open(dest_path, "w")
    to_file.write(template)


def recursively_generate_pages(
    from_path: str, template_path: str, dest_path: str, base_path: str
) -> str:

    for filename in os.listdir(from_path):
        cur_from_path = os.path.join(from_path, filename)
        cur_dest_path = os.path.join(dest_path, filename)
        if os.path.isfile(cur_from_path):
            cur_dest_path, _ = os.path.splitext(cur_dest_path)
            cur_dest_path += ".html"
            generate_page(cur_from_path, template_path, cur_dest_path, base_path)
        else:
            recursively_generate_pages(
                cur_from_path, template_path, cur_dest_path, base_path
            )
