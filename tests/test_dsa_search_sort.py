import random
from types import SimpleNamespace

from gearshare import GearShare

from dsa.search import binary_search, linear_search_by_name
from dsa.sorting import bubble_sort, catalogue_sort, insertion_sort, selection_sort


def starter_items():
    service = GearShare()
    service.load_data()
    return service.list_items()


def test_linear_search_by_name():
    items = starter_items()
    assert linear_search_by_name(items, "Canon EOS 200D") == 0
    assert linear_search_by_name(items, "canon eos 200d") == 0
    assert linear_search_by_name(items, "Missing") == -1


def test_binary_search_samples():
    skus = [f"100000000{i}" for i in range(1, 8)]
    assert binary_search(skus, "1000000006") == (5, 2)
    assert binary_search(skus, "1000000008") == (-1, 3)
    assert binary_search([], "1000000001") == (-1, 0)


def test_binary_search_edges():
    skus = ["1000000001"]
    assert binary_search(skus, "1000000001") == (0, 1)
    assert binary_search(skus, "1000000000") == (-1, 1)
    skus = ["1000000001", "1000000002", "1000000003"]
    assert binary_search(skus, "1000000001")[0] == 0
    assert binary_search(skus, "1000000003")[0] == 2


def test_hand_sorts_match_sorted_random_lists():
    randomizer = random.Random(2205)
    values = randomizer.sample(range(1000), 30)
    for sorter in (bubble_sort, insertion_sort, selection_sort):
        assert sorter(values, print_passes=False) == sorted(values)


def test_sort_sample_output(capsys):
    assert bubble_sort([6, 3, 5, 2]) == [2, 3, 5, 6]
    assert "after pass 1: [3, 5, 2, 6]\n" in capsys.readouterr().out


def test_catalogue_sort_starter_order():
    items = starter_items()
    sorted_items = catalogue_sort(items)
    assert [(item.category, item.name) for item in sorted_items] == [
        ("Accessories", "SD Card 128GB"),
        ("Audio", "Rode Wireless Mic"),
        ("Drones", "DJI Mini Drone"),
        ("Cameras", "Canon EOS 200D"),
        ("Lenses", "Sony 50mm Lens"),
        ("Showcase", "Vintage Leica (Showcase)"),
        ("Tripods", "Manfrotto Tripod"),
    ]
