# GearShare Mini

A rental system for FrameWorks Gear Rental, built in four phases: a Python/OOP
console engine, data structures and benchmarks, a SQL database, and a React
website with an API. The full specification is in [SPEC.md](SPEC.md).


## Requirements

- Python 3.11 or newer
- Node.js (LTS) and npm, for the website
- Git

## Setup

### Windows (PowerShell)

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS / Linux

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run
`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once.

## Run the console app (Phases 1 to 3)

All sample outputs assume today is 2026-11-03.

```powershell
# Windows PowerShell
$env:TODAY = "2026-11-03"
python main.py
```

```sh
# macOS / Linux
TODAY=2026-11-03 python main.py
```

The first run creates `gearshare.db` from `sql/schema.sql` and `sql/seed.sql`.
Delete `gearshare.db` to reset to the starter data.

## Run the API and website (Phase 4)

Use two terminals, both from the project root.

**Terminal 1: API** (http://127.0.0.1:8000, test page at `/docs`)

```sh
python -m uvicorn api.main:app --reload
```

**Terminal 2: website** (http://localhost:5173)

```sh
cd web
npm install
npm run dev
```

The website reads the API address from `web/.env`:

```
VITE_API_URL=http://127.0.0.1:8000
```

Restart `npm run dev` after changing it. Details: [api/README.md](api/README.md)
and [web/README.md](web/README.md).

## Run the tests

```sh
python -m pytest -v      # Python: Phases 1 to 4 (API)
cd web && npm test       # React: basket reducer tests
```

Every Python test uses a fresh temporary database.

## Project structure

```
items.py, customers.py, rentals.py,    Phase 1: classes, errors, service, menu
errors.py, gearshare.py, audit.py, main.py
dsa/                                   Phase 2: search, sorting, hashing, history,
                                       categories, recursion
benchmarks/                            Phase 2: audit, sort and queue comparisons
sql/                                   Phase 3: schema, seed, queries, tx demo,
                                       indexes, index report scripts
storage/                               Phase 3: repository classes (sqlite3)
experiments/                           Phase 3: SQL injection demo (intentionally unsafe)
api/                                   Phase 4: FastAPI endpoints
web/                                   Phase 4: React + Vite + Tailwind
data/                                  Starter CSVs and the flat file
docs/                                  Design, reports, diagrams, checklists
tests/                                 pytest suite
DECISIONS.md, AI_LOG.md                Design decisions and AI prompt log
```

## Phase 1: rule coverage

| Rule | Method | Test |
|---|---|---|
| R1 | `GearShare.rent()` | `test_display_item` |
| R2 | `Accessory.rental_period()`, `GearShare.extend()` | `test_accessory_is_always_rentable_for_two_days`, `test_accessory_cannot_be_extended` |
| R3 | `GearShare.rent()` | `test_rental_limit` |
| R4 | `GearShare.rent()` | `test_unpaid_fines_above_500`, `test_rohan_is_blocked_with_unpaid_fines` |
| R5 | `GearShare.late_fee()` | `test_late_fee_examples` |
| R6 | `GearShare.extend()` | `test_extensions_two_steps_and_then_error` |
| R7 | `GearShare.join_waiting_list()`, `GearShare.return_item()` | `test_vikram_return_fee_and_waiting_list` |
| R8 | `GearShare.rent()` | `test_duplicate_rental` |
| R9 | `GearItem.sku` setter | `test_invalid_sku`, `test_sku_property_rejects_invalid_values` |
| R10 | `GearShare.late_fee()` | `test_late_fee_examples`, `test_return_on_due_date_not_late` |

## Phase 2: data structures

| Topic | Where |
|---|---|
| Linear and binary search | `dsa/search.py` |
| Bubble, insertion, selection sort; catalogue sort | `dsa/sorting.py` |
| Duplicates, grouping, frequency, two-sum | `dsa/hashing.py`, `import_gear.py` |
| Undo stack, waiting-list queue | `gearshare.py` (menu option 9) |
| Rental history (linked list) | `dsa/history.py` |
| Recursion and category tree | `dsa/recursion.py`, `dsa/categories.py` |

Reports: [benchmark](docs/benchmark_report.md), [sorting](docs/sort_report.md),
[queue](docs/queue_report.md). Run a benchmark with
`python -m benchmarks.audit`.

## Phase 3: database

- Schema, seed and queries: `sql/schema.sql`, `sql/seed.sql`, `sql/queries.sql` (Q1 to Q12)
- Transaction and rollback demo: `sql/tx_demo.sql`, `python -m sql.run_tx_demo`
- Index report: [docs/index_report.md](docs/index_report.md)
- Normalisation and ER diagram: [docs/normalisation.md](docs/normalisation.md), `docs/er_diagram.png`
- Injection experiment: [docs/injection_evidence.md](docs/injection_evidence.md)

`GearShare` contains no SQL. All database access goes through `storage/`
with parameterised queries.

## Phase 4: API and website

| Endpoint | Purpose |
|---|---|
| `GET /gear`, `GET /gear/{sku}` | Search and view items |
| `POST /gear` | Staff: add an item |
| `POST /rentals` | Rent an item |
| `POST /rentals/{id}/return`, `/extend` | Return or extend |
| `POST /waiting-list` | Join the waiting list |
| `GET /customers`, `GET /customers/{id}/rentals` | Customers and their rentals |
| `GET /overdue` | Staff overdue rental report |
| `GET /gear/{sku}/waiting-list` | Customer queue for an item |
| `POST /customers` | Staff: add a customer |
| `GET /categories` | List rentable item categories |

Errors use `{"error": "R3", "message": "..."}` with the same text as the console.
Statuses: 404 not found, 409 rule conflict, 422 invalid input.

Website routes: `/` catalogue, `/gear/:sku`, `/me`, `/basket`, `/admin/add`,
and a 404 page. Component tree and state locations: [docs/component_tree.md](docs/component_tree.md).
Behaviour checklist: [docs/behaviour_checklist.md](docs/behaviour_checklist.md).

## How AI was used

- Tool: GitHub Copilot in VS Code (Agent mode), one prompt per numbered task.
- Every prompt and what I changed is recorded in [AI_LOG.md](AI_LOG.md).
- Design decisions and rejected alternatives are in [DECISIONS.md](DECISIONS.md).
- Activity tracking: WakaTime in VS Code.

## Branches and tags

One branch per phase: `feature/python`, `feature/dsa`, `feature/sql`,
`feature/react`. Each is merged into `main` and tagged `phase-1` to `phase-4`.