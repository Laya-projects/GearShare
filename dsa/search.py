def linear_search_by_name(items, name):
    """Return the index of the first item whose name matches, or -1."""
    wanted = name.casefold()
    for index, item in enumerate(items):
        if item.name.casefold() == wanted:
            return index
    return -1


def binary_search(skus, target):
    """Return (index, comparisons) for target in a sorted SKU list."""
    low = 0
    high = len(skus) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        middle = (low + high) // 2
        if skus[middle] == target:
            return middle, comparisons
        if skus[middle] < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1, comparisons
