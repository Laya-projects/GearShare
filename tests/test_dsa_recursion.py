from dsa.categories import build_category_tree, count_items, count_items_iterative, path_to
from dsa.recursion import factorial, fibonacci, sum_of_digits


def test_recursion_samples():
    assert factorial(6) == 720
    assert fibonacci(8) == 21
    assert sum_of_digits(5078) == 20


def test_recursion_edge_cases():
    assert factorial(0) == 1
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert sum_of_digits(0) == 0


def test_category_tree_and_paths():
    root = build_category_tree()
    captured = []

    def capture(node, indent=0):
        captured.append(f"{' ' * indent}{node.name} ({node.item_count()})")
        for child in sorted(node.children, key=lambda item: item.name):
            capture(child, indent + 2)

    capture(root)
    output = "\n".join(captured)
    assert "Gear Hub (7)" in output
    assert "  Accessories (1)" in output
    assert "  Photography (2)" in output
    assert "    Cameras (1)" in output
    assert "    Lenses (1)" in output
    assert count_items(root, "Photography") == 2
    assert count_items(root, "Lighting") is None
    assert path_to(root, "Lenses") == ["Gear Hub", "Photography", "Lenses"]
    assert path_to(root, "Lighting") is None


def test_iterative_counts_match_recursive_counts():
    root = build_category_tree()
    names = [
        "Gear Hub",
        "Accessories",
        "Audio",
        "Drones",
        "Photography",
        "Cameras",
        "Lenses",
        "Showcase",
        "Tripods",
    ]
    for name in names:
        assert count_items_iterative(root, name) == count_items(root, name)


def test_missing_category_and_empty_category():
    root = build_category_tree()
    assert count_items(root, "Unknown") is None
    assert path_to(root, "Unknown") is None

    empty_root = build_category_tree([])
    assert count_items(empty_root, "Gear Hub") == 0
