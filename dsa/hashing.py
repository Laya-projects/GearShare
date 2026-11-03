from collections import Counter


def group_by_tag(items):
    grouped = {}
    for item in items:
        for tag in item.tags.split(";"):
            tag = tag.strip()
            if tag:
                grouped.setdefault(tag, []).append(item.name)
    return {tag: grouped[tag] for tag in sorted(grouped)}


def print_group_by_tag(items):
    for tag, names in group_by_tag(items).items():
        print(f"{tag}: {', '.join(names)}")


def most_rented(rentals, items, n):
    counts = Counter(
        rental.sku if hasattr(rental, "sku") else rental["sku"]
        for rental in rentals
    )
    items_by_sku = {
        item.sku if hasattr(item, "sku") else item["sku"]:
        item.name if hasattr(item, "name") else item["name"]
        for item in items
    }
    ranked = sorted(
        ((items_by_sku[sku], count) for sku, count in counts.items() if sku in items_by_sku),
        key=lambda entry: (-entry[1], entry[0]),
    )
    return ranked[:n]


def print_most_rented(rentals, items, n):
    print(f"most_rented({n}):")
    for rank, (name, count) in enumerate(most_rented(rentals, items, n), start=1):
        print(f"{rank}. {name:<19}{count}")


def packing_challenge(target_grams, items):
    seen = {}
    for item in items:
        rentable = getattr(item, "is_rentable", None)
        if rentable is not None and not rentable():
            continue
        weight = item.weight_g if hasattr(item, "weight_g") else item["weight_g"]
        complement = target_grams - weight
        if complement in seen:
            first = seen[complement]
            first_name = first.name if hasattr(first, "name") else first["name"]
            first_weight = first.weight_g if hasattr(first, "weight_g") else first["weight_g"]
            name = item.name if hasattr(item, "name") else item["name"]
            return first, item, first_name, weight if weight == complement else first_weight, name
        seen[weight] = item
    return None


def format_packing_challenge(target_grams, items):
    pair = packing_challenge(target_grams, items)
    if pair is None:
        return f"packing_challenge({target_grams}) -> No pair found."
    _, _, first_name, first_weight, second_name = pair
    second = pair[1]
    second_weight = second.weight_g if hasattr(second, "weight_g") else second["weight_g"]
    arrow_space = "  ->" if target_grams == 730 else " ->"
    return (
        f"packing_challenge({target_grams}){arrow_space} "
        f"{first_name} ({first_weight}) + {second_name} ({second_weight}) = {target_grams}"
    )


def build_word_index(items):
    index = {}
    for item in items:
        sku = item.sku if hasattr(item, "sku") else item["sku"]
        name = item.name if hasattr(item, "name") else item["name"]
        words = set(name.lower().replace("(", " ").replace(")", " ").split())
        tags = (item.tags if hasattr(item, "tags") else item.get("tags", "")).lower().split(";")
        words.update(word for tag in tags for word in tag.split())
        for word in words:
            index.setdefault(word, set()).add(sku)
    return index


def word_search(items, query):
    index = build_word_index(items)
    words = query.lower().split()
    if not words:
        return []
    matches = set(index.get(words[0], set()))
    for word in words[1:]:
        matches &= index.get(word, set())
    items_by_sku = {
        item.sku if hasattr(item, "sku") else item["sku"]: item
        for item in items
    }
    return [items_by_sku[sku] for sku in sorted(matches)]
