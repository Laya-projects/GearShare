# GearShare Mini

A rental system for FrameWorks Gear Rental, built in four phases: object-oriented
Python, data structures, a SQL database, and a website on top of an HTTP API.
A customer can search the gear, rent it, join a waiting list and see their
rentals, from a console menu or from the browser, using the same engine and
database.

| Phase | Topic | Branch |
|---|---|---|
| 1 | Python and OOP | `feature/python` |
| 2 | Data structures | `feature/dsa` |
| 3 | SQL | `feature/sql` |
| 4 | API and website (React + Tailwind) | `feature/react` |

## Contents

1. [Quick start](#quick-start)
2. [Preview](#preview)
3. [AI Metrics](#ai-metrics)
4. [The console menu](#the-console-menu)
5. [Project layout](#project-layout)
6. [Business rules](#business-rules)
7. [What each phase added](#what-each-phase-added)
8. [Tests](#tests)
9. [Documentation index](#documentation-index)
10. [Troubleshooting](#troubleshooting)

---

## Quick start

**You need:** Python 3.11+, Node.js with npm, and git.

### 1. Get the code and set up Python

```
git clone https://github.com/<your-username>/<your-repo>.git
cd "Project code - Zoho"
python -m venv venv
```

Windows (PowerShell): `venv\Scripts\activate`
macOS / Linux: `source venv/bin/activate`

```
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run
`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once.

### 2. Run the console app

The sample data is built around **2026-11-03**, so set `TODAY`.

Windows (PowerShell): `$env:TODAY="2026-11-03"; python main.py`
macOS / Linux: `TODAY=2026-11-03 python main.py`

The first run creates `gearshare.db` from the schema and starter data.
Delete `gearshare.db` to start again from the starter data.

### 3. Run the website (two terminals, from the project root)

```
python -m uvicorn api.main:app --reload      # terminal 1: API on port 8000
cd web && npm install && npm run dev         # terminal 2: site on port 5173
```

Open <http://localhost:5173>. API test page: <http://127.0.0.1:8000/docs>.
The site reads the API address from `web/.env` (`VITE_API_URL=http://127.0.0.1:8000`).

---

## Preview

<img width="1137" height="885" alt="image" src="https://github.com/user-attachments/assets/55d49ec6-a31c-4ee4-8517-6624b311c0cf" />

<img width="1893" height="869" alt="image" src="https://github.com/user-attachments/assets/262615a3-edf3-427d-a8ac-a46a5118adaa" />

<img width="1899" height="877" alt="image" src="https://github.com/user-attachments/assets/3d04380e-97b8-47ab-987f-68e77138d825" />

<img width="1232" height="879" alt="image" src="https://github.com/user-attachments/assets/60b13491-4476-4726-be06-73d32d2cc6d0" />

<img width="1150" height="307" alt="image" src="https://github.com/user-attachments/assets/0170750c-9cd1-4fe0-9824-29c4d410eea0" />


---

## AI Metrics

This project was built with AI at every step, as the assignment requires.

| Item | Detail |
|---|---|
| AI tool | GitHub Copilot in VS Code (Agent mode), approved by the coordinator |
| Activity tracking | WakaTime extension in VS Code |
| Working style | One agent prompt per numbered task, reviewed before accepting |
| Prompts used | total (one entry per prompt in [AI_LOG.md](AI_LOG.md)) |
| Coding time |  hours, from the WakaTime dashboard |
| Languages tracked | e.g. Python, JavaScript, SQL, Markdown |

**How AI was used, by phase**

| Phase | AI did | I did |
|---|---|---|
| 1. Python and OOP | Wrote classes, service, menu and tests from SPEC.md | Reviewed the diff, replayed Session A by hand, checked for `if tier ==` |
| 2. Data structures | Wrote search, sorts, hashing, history and benchmarks | Ran the benchmarks, wrote the Surprises in my own words |
| 3. SQL | Wrote schema, seed, 12 queries, repositories | Checked every query result against the spec, ran the rollback demo |
| 4. API and website | Wrote the endpoints, React pages and theme | Tested all behaviour-table rows, the race condition and the 360 px layout |


**Evidence:** WakaTime dashboard screenshot:

<img width="1915" height="946" alt="image" src="https://github.com/user-attachments/assets/523bdd7f-4823-46b5-8fcb-54031db21b8c" />

and the prompt log in [AI_LOG.md](AI_LOG.md).

---

## The console menu

Type a number and press Enter. `0` exits.

| Choice | What it does | Example result |
|---|---|---|
| 1 | List the catalogue | Table with `1 of 2`, `0 of 1` or `not rentable` |
| 2 | Search by name or tag | `1 result:` or `No items match 'zzz'.` |
| 3 | Rent | `OK: Ananya Nair rented 'Sony 50mm Lens'. Due 2026-11-06.` |
| 4 | Return | `OK: Vikram Shah returned 'DJI Mini Drone'. Late by 5 days. Fee: ₹500.` |
| 5 | Extend | `OK: Extended 'Manfrotto Tripod' (extension 1 of 2). New due date ...` |
| 6 | Join waiting list | `OK: Meera Joshi is #1 on the waiting list for 'DJI Mini Drone'.` |
| 7 | Customer rentals | Active rentals, `OVERDUE (5 days)`, items held of limit, unpaid fines |
| 8 | Overdue report | Late rentals, most late first, with the fine so far |
| 9 | Undo | Reverses the latest rent or return, or `Nothing to undo.` |

Money is whole rupees (`₹100`) and dates are `YYYY-MM-DD`. Errors look like
`ERROR [R3]: ...` for a rule and `ERROR [ClassName]: ...` otherwise.

**Try this:** `3`, `C003`, `1000000003` (no units free, answer `y` to join the
waiting list), then `4`, `RN001`. The output ends with
`Next on waiting list: Meera Joshi.`

**Persistence check:** rent `1000000002` as `C001`, exit with `0`, start again and
choose `7` for `C001`. Rental `RN011` is still there.

---

## Project layout

```
Project code - Zoho/
├─ data/                 Starter CSVs and the flat file
├─ items.py, customers.py, rentals.py, errors.py, audit.py, gearshare.py, main.py
├─ dsa/                  Search, sorting, hashing, history, categories, recursion
├─ benchmarks/           Audit, sort and queue comparisons
├─ sql/                  schema, seed, queries, tx demo, indexes, report scripts
├─ storage/              Database helper and one repository per table group
├─ experiments/          Injection demo (deliberately unsafe)
├─ api/                  FastAPI app
├─ web/                  React + Vite + Tailwind site
├─ tests/                pytest suite
├─ docs/                 Design, reports, diagrams, checklists
├─ DECISIONS.md          Design decisions and why
├─ AI_LOG.md             Every AI prompt and what I changed
└─ SPEC.md               The project specification
```

The layers: domain classes at the bottom, then the `GearShare` service where the
rules are applied, then three front doors: the console menu, the HTTP API and
(through the API) the website. None of them applies a rule itself.

---

## Business rules

| Rule | What it says | Enforced in | Test |
|---|---|---|---|
| R1 | Display items are never rented | `GearShare.rent` | `test_display_item` |
| R2 | Accessories: 2 days, no extension | `Accessory.rental_period`, `GearShare.extend` | `test_accessory_cannot_be_extended` |
| R3 | Item limit by tier (2, 4, 8) | `GearShare.rent` | `test_rental_limit` |
| R4 | Rent blocked when unpaid fines are above ₹500 | `GearShare.rent` | `test_unpaid_fines_above_500` |
| R5 | Late fee capped at the item price | `GearShare.late_fee` | `test_late_fee_examples` |
| R6 | Max 2 extensions, none if someone waits | `GearShare.extend` | `test_extensions_two_steps_and_then_error` |
| R7 | Waiting list, first come first served | `GearShare.join_waiting_list` | `test_vikram_return_fee_and_waiting_list` |
| R8 | No two units of the same item | `GearShare.rent` | `test_duplicate_rental` |
| R9 | SKU is exactly 10 digits | `GearItem.sku` setter | `test_invalid_sku` |
| R10 | Returning on the due date is not late | `GearShare.late_fee` | `test_return_on_due_date_not_late` |

**[Verify]** the test names against your `tests/` folder.

---

## What each phase added

| Phase | What it added | Additional enhancements |
|---|---|---|
| 1. Python and OOP | Item and customer classes, rule exceptions, `GearShare` service, `@audit`, overdue generator, console menu | None |
| 2. Data structures | Linear and binary search, hand-written sorts, hashing (duplicates, grouping, two-sum), undo stack, waiting-list queue, linked-list history, category tree, recursion, benchmarks | Growth-ratio columns in the benchmark report |
| 3. SQL | Normalised SQLite database, 12 queries, transaction rollback demo, indexes, `storage/` repositories, injection experiment | Repository layer keeps `GearShare` free of SQL |
| 4. API and website | FastAPI endpoints, React catalogue, item details, basket, my rentals, add item, routing, context, `useReducer` | See below |

**Phase 4 enhancements beyond the brief:**

| Enhancement | What it does |
|---|---|
| Pink and black theme | Cursive italic headings, dark cards, cards pop out on hover and keyboard focus, respects reduced-motion |
| Add customer page | Staff add a customer with a generated ID (C006, C007), duplicate email check, picker updates at once |
| Category dropdown | Add item uses a list of valid categories from the API instead of free text |
| Staff overdue page | Overdue table with pink highlight and a text label, shares the console report logic |
| Waiting list visibility | Shows "You are #2 on the waiting list" and "Next on waiting list: ..." after a return |
| Return button | Return from My rentals, with a confirm step and the server's fee message |

---

## Tests

```
python -m pytest -v        # Python: all phases and the API
cd web && npm test         # React: basket reducer and validation
```

Every Python test uses a fresh temporary database. A test fails if any SQL in
`storage/` or `gearshare.py` is built from text.

Manual checks for the site: 360 px wide, keyboard only, and "Slow 3G" in the
browser tools to confirm that an old response never replaces a newer one.

---

## Documentation index

| File | What is in it |
|---|---|
| [DECISIONS.md](DECISIONS.md) | Design decisions and the alternatives rejected |
| [AI_LOG.md](AI_LOG.md) | AI prompts used, and what I changed |
| [docs/design.md](docs/design.md) | Class diagram and CRC cards |
| [docs/benchmark_report.md](docs/benchmark_report.md) | Predicted against measured Big-O |
| [docs/normalisation.md](docs/normalisation.md) | Flat file to 3NF, with the three anomalies |
| [docs/index_report.md](docs/index_report.md) | Indexes, before and after |
| [docs/injection_evidence.md](docs/injection_evidence.md) | SQL injection experiment output |
| [docs/component_tree.md](docs/component_tree.md) | React components and where state lives |
| [docs/behaviour_checklist.md](docs/behaviour_checklist.md) | Phase 4 behaviour table, ticked off |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| The site shows "Can't reach the rental server." | Start the API and check `VITE_API_URL` in `web/.env`. Restart `npm run dev` after changing it. |
| Browser console mentions CORS | Open the site as `http://localhost:5173` |
| Overdue rentals or fines look different | Set `TODAY=2026-11-03` before starting |
| I want the starter data back | Delete `gearshare.db` |
| `pytest` or `uvicorn` not found | Activate the venv, or use `python -m pytest` and `python -m uvicorn` |
| `ModuleNotFoundError: api` | Run `uvicorn` from the project root, not from inside `api/` |
| `ModuleNotFoundError` in tests | Check `pytest.ini` has `pythonpath = .` |
