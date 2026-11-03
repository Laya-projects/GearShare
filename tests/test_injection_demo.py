import ast
from pathlib import Path

from experiments.injection_demo import (
    create_database,
    search_safe,
    search_unsafe,
)


ROOT = Path(__file__).resolve().parents[1]


def test_injection_demo_results():
    connection = create_database()
    try:
        unsafe_drone, _ = search_unsafe(connection, "Drone")
        unsafe_attack, attack_sql = search_unsafe(connection, "' OR '1'='1")
        safe_attack = search_safe(connection, "' OR '1'='1")
        safe_drone = search_safe(connection, "Drone")

        assert len(unsafe_drone) == 1
        assert len(unsafe_attack) == 7
        assert len(safe_attack) == 0
        assert len(safe_drone) == 1
        assert attack_sql == (
            "SELECT sku, name FROM items WHERE name LIKE '%' OR '1'='1%' "
            "ORDER BY name"
        )
    finally:
        connection.close()


def sql_call_nodes(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in {"execute", "executemany", "executescript"}:
                if node.args:
                    yield node.args[0]


def uses_formatting(node):
    if isinstance(node, ast.JoinedStr):
        return True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        return node.func.attr == "format"
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        return True
    return False


def test_program_sql_is_parameterized_or_not_formatted():
    paths = list((ROOT / "storage").glob("*.py"))
    paths.append(ROOT / "gearshare.py")
    for path in paths:
        for argument in sql_call_nodes(path):
            assert not uses_formatting(argument), f"formatted SQL in {path}"
