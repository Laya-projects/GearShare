def bubble_sort(values, print_passes=True):
    for end in range(len(values) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
                swapped = True
        if print_passes:
            print(f"after pass {len(values) - end}: {values}")
        if not swapped:
            break
    return values


def insertion_sort(values, print_passes=True):
    for index in range(1, len(values)):
        current = values[index]
        position = index
        while position > 0 and values[position - 1] > current:
            values[position] = values[position - 1]
            position -= 1
        values[position] = current
        if print_passes:
            print(f"after inserting index {index}: {values}")
    return values


def selection_sort(values, print_passes=True):
    for start in range(len(values) - 1):
        minimum = start
        for index in range(start + 1, len(values)):
            if values[index] < values[minimum]:
                minimum = index
        values[start], values[minimum] = values[minimum], values[start]
        if print_passes:
            print(f"after pass {start + 1} (min={values[start]}): {values}")
    return values


def top_level_category(item):
    return item.parent_category or item.category


def catalogue_sort(items):
    return sorted(
        items,
        key=lambda item: (
            top_level_category(item),
            -item.weight_g,
            item.name,
        ),
    )
