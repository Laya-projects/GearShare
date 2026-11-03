import csv

from gearshare import GearShare
from dsa.hashing import (
    build_word_index,
    format_packing_challenge,
    group_by_tag,
    most_rented,
    packing_challenge,
    print_group_by_tag,
    word_search,
)
from import_gear import import_gear


def starter_data():
    service = GearShare()
    service.load_data()
    return service


def test_duplicate_import_sample(capsys):
    import_gear("gear_with_duplicate.csv")
    assert capsys.readouterr().out.splitlines() == [
        "Line 9: duplicate SKU 1000000004 (already used by 'Manfrotto Tripod'), skipped.",
        "Imported 8 rows: 7 added, 1 duplicate skipped.",
    ]


def test_duplicate_import_no_duplicates(tmp_path, capsys):
    path = tmp_path / "gear.csv"
    path.write_text(open("data/gear.csv", encoding="utf-8").read(), encoding="utf-8")
    import_gear(path)
    assert capsys.readouterr().out == "Imported 7 rows: 7 added, 0 duplicate skipped.\n"


def test_group_by_tag_sample(capsys):
    service = starter_data()
    print_group_by_tag(service.list_items())
    assert capsys.readouterr().out.splitlines() == [
        "aerial: DJI Mini Drone",
        "audio: Rode Wireless Mic",
        "display: Vintage Leica (Showcase)",
        "dslr: Canon EOS 200D",
        "interview: Rode Wireless Mic",
        "lens: Sony 50mm Lens",
        "photo: Canon EOS 200D, Sony 50mm Lens",
        "storage: SD Card 128GB",
        "support: Manfrotto Tripod",
        "video: DJI Mini Drone",
    ]
    assert group_by_tag([]) == {}


def test_most_rented_sample():
    service = starter_data()
    assert most_rented(service.rentals, service.list_items(), 3) == [
        ("Canon EOS 200D", 3),
        ("DJI Mini Drone", 2),
        ("Rode Wireless Mic", 2),
    ]


def test_most_rented_ties_are_alphabetical():
    service = starter_data()
    counts = service.rentals[:]
    counts = counts + counts[:0]
    items = service.list_items()[:3]
    result = most_rented(counts, items, 3)
    assert all(result[i][0] <= result[i + 1][0] for i in range(len(result) - 1) if result[i][1] == result[i + 1][1])


def test_packing_challenge_samples():
    service = starter_data()
    items = service.list_items()
    assert format_packing_challenge(730, items) == (
        "packing_challenge(730)  -> Canon EOS 200D (450) + Sony 50mm Lens (280) = 730"
    )
    assert format_packing_challenge(1320, items) == (
        "packing_challenge(1320) -> Manfrotto Tripod (1200) + Rode Wireless Mic (120) = 1320"
    )
    assert format_packing_challenge(1000, items) == (
        "packing_challenge(1000) -> No pair found."
    )


def test_packing_does_not_use_display_or_same_item():
    service = starter_data()
    display = service.items["1000000006"]
    accessory = service.items["1000000007"]
    assert packing_challenge(display.weight_g * 2, [display]) is None
    assert packing_challenge(accessory.weight_g * 2, [accessory]) is None


def test_word_index_requires_all_words():
    service = starter_data()
    items = service.list_items()
    index = build_word_index(items)
    assert "canon" in index
    assert index["photo"]
    assert [item.name for item in word_search(items, "canon photo")] == ["Canon EOS 200D"]
    assert word_search(items, "canon drone") == []
