import io
from contextlib import redirect_stdout

import main
from gearshare import GearShare


def run_script(inputs):
    values = iter(inputs)

    def fake_input(prompt=""):
        print(prompt, end="")
        value = next(values)
        print(value)
        return value

    service = GearShare()
    service.load_data()
    output = io.StringIO()
    with redirect_stdout(output):
        main.run_menu(service, "2026-11-03", fake_input)
    return output.getvalue()


def test_bad_menu_input_does_not_crash():
    output = run_script(["abc", "", "0"])
    assert output.count("Please enter a number from 0 to 9.") == 2


def test_catalogue_sample():
    output = run_script(["1", "0"])
    assert "1000000001  Canon EOS 200D             Equipment  1 of 2" in output
    assert "1000000003  DJI Mini Drone             Equipment  0 of 1" in output
    assert "Vintage Leica (Showcase)" in output
    assert "Display    not rentable" in output


def test_search_samples():
    output = run_script(["2", "VIDEO", "2", "zzz", "0"])
    assert "1 result:" in output
    assert "DJI Mini Drone (video, aerial)" in output
    assert "No items match 'zzz'." in output


def test_session_a_transcript():
    output = run_script([
        "3", "C001", "1000000002",
        "3", "C001", "1000000002",
        "3", "C003", "1000000006",
        "3", "C004", "1000000004",
        "3", "C003", "1000000003", "y",
        "4", "RN001",
        "0",
    ])
    assert "Ananya Nair rented 'Sony 50mm Lens'. Due 2026-11-06." in output
    assert "ERROR [R8]: Ananya Nair already has a unit of 'Sony 50mm Lens'." in output
    assert "ERROR [R1]: 'Vintage Leica (Showcase)' is a display item and cannot be rented." in output
    assert "ERROR [R4]: Rohan Das has unpaid fines of ₹600 (limit ₹500)." in output
    assert "No units of 'DJI Mini Drone' are available." in output
    assert "OK: Meera Joshi is #1 on the waiting list for 'DJI Mini Drone'." in output
    assert "Vikram Shah returned 'DJI Mini Drone'. Late by 5 days. Fee: ₹500." in output
    assert "Next on waiting list: Meera Joshi." in output
