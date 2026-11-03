from gearshare import GearShare


class Node:
    def __init__(self, name, children=None, direct_items=0):
        self.name = name
        self.children = list(children or [])
        self.direct_items = direct_items

    def item_count(self):
        return self.direct_items + sum(child.item_count() for child in self.children)


def find_node(root, name):
    if root.name == name:
        return root
    for child in root.children:
        found = find_node(child, name)
        if found is not None:
            return found
    return None


def print_node(node, indentation=0):
    print(" " * indentation + f"{node.name} ({node.item_count()})")
    for child in sorted(node.children, key=lambda child: child.name):
        print_node(child, indentation + 2)


def print_tree(root):
    print_node(root)


def build_category_tree(items=None):
    if items is None:
        service = GearShare()
        service.load_data()
        items = service.list_items()

    root = Node("Gear Hub")
    roots_by_name = {root.name: root}

    for item in items:
        top_level = item.parent_category or item.category
        if top_level not in roots_by_name:
            roots_by_name[top_level] = Node(top_level)
            root.children.append(roots_by_name[top_level])

        if item.parent_category:
            if item.category not in roots_by_name:
                roots_by_name[item.category] = Node(item.category)
                roots_by_name[top_level].children.append(roots_by_name[item.category])
            roots_by_name[item.category].direct_items += 1
        else:
            roots_by_name[top_level].direct_items += 1

    root.children.sort(key=lambda child: child.name)
    for child in root.children:
        child.children.sort(key=lambda grandchild: grandchild.name)
    return root


def count_items(root, name=None):
    if name is None:
        name = root
        # Import lazily so callers can use count_items('Photography').
        from dsa.categories import build_category_tree
        root = build_category_tree()
    node = find_node(root, name)
    return None if node is None else node.item_count()


def count_items_iterative(root, name=None):
    if name is None:
        name = root
        root = build_category_tree()
    node = find_node(root, name)
    if node is None:
        return None
    stack = [node]
    total = 0
    while stack:
        current = stack.pop()
        total += current.direct_items
        stack.extend(current.children)
    return total


def path_to(root, name=None):
    if name is None:
        name = root
        root = build_category_tree()

    def search(node, path):
        current_path = path + [node.name]
        if node.name == name:
            return current_path
        for child in node.children:
            result = search(child, current_path)
            if result is not None:
                return result
        return None

    return search(root, [])
