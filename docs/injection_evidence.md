# SQL injection experiment

## Unsafe

```text
Unsafe SQL injection demo
search_unsafe("Drone") -> 1 row
search_unsafe("' OR '1'='1") -> 7 rows
Unsafe attack SQL: SELECT sku, name FROM items WHERE name LIKE '%' OR '1'='1%' ORDER BY name
```

## Safe

```text
Safe parameterised demo
search_safe("' OR '1'='1") -> 0 rows
search_safe("Drone") -> 1 row
```

## What the parameterised query did differently

TODO: Write how the safe query sent the attack text as data rather than executable SQL.

TODO: Explain what changed because wildcard characters were added in Python.

TODO: Describe why placeholders prevent the input's quote characters from altering the SQL structure.

TODO: Add one sentence comparing what remained fixed in the SQL and what became a bound parameter.
