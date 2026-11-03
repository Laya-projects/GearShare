import pytest

from benchmarks.generate_items import generate_items


@pytest.mark.parametrize("count", [1, 25, 1000])
def test_generated_items_are_unique_valid_and_counted(count):
    items = generate_items(count)
    assert len(items) == count
    assert len(set(items)) == count
    assert all(sku.isdigit() and len(sku) == 10 for sku in items)
