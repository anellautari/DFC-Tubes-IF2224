class Node:
    def __init__(self, label, token=None):
        self.label = label
        self.token = token
        self.children = []

    def add_children(self, node):
        if node:
            self.children.append(node)
        return node

    def print_tree(self, prefix: str = "", is_last: bool = True):
        connector = "└── " if is_last else "├── "
        if self.token:
            print(prefix + connector + f"{self.label}({self.token.value})")
        else:
            print(prefix + connector + f"{self.label}")

        # Prefix untuk anak-anak (indentasi)
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            child.print_tree(child_prefix, is_last_child)
