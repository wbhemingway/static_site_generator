def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [s for b in blocks if (s := b.strip()) != ""]
    return blocks
