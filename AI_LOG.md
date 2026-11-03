Read SPEC.md fully. Set up the project foundation only, no game logic yet:
1. Create the folder structure: items.py, customers.py, rentals.py,
   errors.py, gearshare.py, main.py, tests/, data/
2. Create the four starter CSVs in data/ (gear.csv, customers.csv,
   rentals.csv, fines.csv) exactly as given in SPEC.md.
3. Create a venv setup, requirements.txt (pytest), .gitignore
   (venv, __pycache__, .env), and an empty DECISIONS.md and AI_LOG.md.
4. Add a README skeleton with a "How to run with TODAY=2026-11-03" section.
5. Add one sanity test that checks the CSVs have 7 items, 5 customers,
   10 rentals and 4 fines.
Run pytest, then commit as "Project scaffold and starter data".

Read SPEC.md, Phase 1, task 1.1 and the Rental Rulebook. Design only, no code.

Create docs/design.md containing:
1. A Mermaid class diagram: GearItem (abstract) with Equipment, Accessory,
   DisplayItem; Customer (abstract) with BasicCustomer, PlusCustomer,
   ProCustomer; Rental; GearShare (service class).
2. One sentence per relationship saying whether it is inheritance (is-a)
   or composition (has-a), and why.
3. What each abstract class forces its subclasses to implement. Customer
   must have polymorphic methods for item limit, rental period and daily
   late fee. GearItem must answer whether it is rentable and its rental
   period. No `if tier ==` anywhere.
4. CRC cards (class, responsibilities, collaborators) for every class.
5. Short answers to the 4 "Think about this" questions for Phase 1.

Add 3 entries to DECISIONS.md (problem, options, choice, why).
Add this prompt to AI_LOG.md.

Read SPEC.md Phase 1 task 1.2 and docs/design.md. Implement the classes only.
The service class and menu come later.

1. errors.py: GearShareError (parent) with these children:
   InvalidSKUError, ItemNotFoundError, CustomerNotFoundError,
   ItemNotRentableError (R1), UnpaidFinesError (R4),
   RentalLimitExceededError (R3), DuplicateRentalError (R8),
   ItemNotAvailableError (R7), ExtensionNotAllowedError (R2, R6).
2. items.py: abstract GearItem with Equipment, Accessory, DisplayItem.
   Use @property with setters so invalid objects can never exist:
   SKU exactly 10 digits (InvalidSKUError), units not negative,
   name not blank. Polymorphic methods: is_rentable() and
   rental_period(customer). Accessory is always 2 days (R2).
3. customers.py: abstract Customer with BasicCustomer, PlusCustomer,
   ProCustomer. Polymorphic methods: max_items(), rental_period(),
   late_fee_per_day() using the Rulebook table. Email must contain @,
   name not blank. NO `if tier ==` anywhere.
4. rentals.py: Rental class with a class attribute for the next rental
   number (RN011 is next after the starter data) and instance attributes
   for the rest. Comment why each belongs where it is.
5. Add __str__ and __repr__ to every class.
6. Tests in tests/: every validation rule, every polymorphic method for
   all three tiers, and pytest.raises for each exception used here.
   Use parametrize for the tier table.
Add 2 entries to DECISIONS.md and this prompt to AI_LOG.md.
Run pytest, fix failures, then commit as "1.2 Core classes and validation".

Read SPEC.md Phase 1 task 1.3, the Rental Rulebook, the order of checks,
and the existing classes. Build the service class only. No menu yet.

Create gearshare.py with class GearShare and these methods:
load_data(), list_items(), rent(), return_item(), extend(),
join_waiting_list(), customer_rentals(), overdue_report().

Rules:
1. Pass `today` into every date-dependent method. Never call
   date.today() inside the class.
2. rent() checks in this exact order, and reports only the first failure:
   customer exists -> SKU is 10 digits -> item exists -> R1 -> R4 (fines
   above 500) -> R3 -> R8 -> availability (raise ItemNotAvailableError so
   the caller can offer the waiting list, R7).
3. Late fee (R5, R10): days late x tier daily rate, capped at the item's
   price. Returning on the due date is not late.
4. extend(): max 2 extensions (R6), each adds the tier's rental period to
   the current due date. Accessories cannot be extended (R2). No extension
   if someone is waiting.
5. Waiting list: a collections.deque per SKU, first come first served (R7).
   return_item() reports who is next.
6. Collections: dict by SKU, dict by customer ID, list of rentals, set of
   SKUs. Explain why in DECISIONS.md.
7. Rebuild availability from rentals that have no return date.
8. Messages must match the SPEC.md samples character for character:
   "ERROR [R3]: ..." for rule errors, "ERROR [ClassName]: ..." for others.
   Put messages in the exception classes, not scattered in the service.
9. Make sure there is no `if tier ==` anywhere.

Tests (fresh state per test, never rely on an earlier test):
- Every rule R1 to R10 at least once.
- The two worked-example tables (due dates and late fees) with
  @pytest.mark.parametrize.
- pytest.raises for every exception.
- Session A from the spec, step by step: the Vikram fee is exactly 500,
  Rohan is blocked with 600, RN003 extensions 1 and 2, then the error.
Add 2 entries to DECISIONS.md and this prompt to AI_LOG.md.
Run pytest, fix failures, then commit as "1.3 GearShare service and exceptions".

Read SPEC.md Phase 1 task 1.4 and the existing gearshare.py.
Add the Pythonic layer. Do not break any existing test.

1. Decorator @audit (put it in audit.py): each time rent, return_item or
   extend succeeds, append a record (time, action, customer, item) to an
   audit list on GearShare. Failed calls must NOT be logged. Use
   functools.wraps. Time must come from the `today` parameter, not
   date.today(). Time values must use ISO YYYY-MM-DD format.
2. Generator iter_overdue(today): yields overdue rentals one at a time
   (due date before today and no return date). overdue_report() must
   consume this generator.
3. Three reports, using comprehensions and sorted(key=lambda ...):
   a. Overdue report, most days late first. Format must match the
      SPEC.md Option 8 sample exactly.
   b. Items by category.
   c. Customers with unpaid fines.
4. Use map() or filter() at least once where it reads better than a loop.
5. "Fine so far" is calculated, not saved.

Add 2 entries to DECISIONS.md and this prompt to AI_LOG.md.
Run pytest, fix failures, then commit as "1.4 Audit decorator, overdue generator and reports".

Read SPEC.md Phase 1 task 1.5 and the existing code. Build the menu,
file loading and finish the Phase 1 deliverables. Do not break any
existing test.

1. main.py: read TODAY from the environment (fallback: the real date)
   and pass it into every date-dependent call. Load the three CSVs
   (gear, customers, rentals) plus fines.csv. Rebuild availability from
   rentals with no return date.
2. Start-up output must match SPEC.md exactly:
   "Loaded 7 items, 5 customers, 10 rentals, 4 fines."
   "Today is 2026-11-03." then the menu with options 0 to 8.
3. Menu loop for options 1 to 8 and 0 (exit): list catalogue, search
   (case-insensitive, name or tag, "No items match 'zzz'." when empty),
   rent (offer the waiting list with "(y/n)" when no unit is free),
   return, extend, join waiting list, customer rentals, overdue report.
   Output format, column spacing and the ₹ symbol must match the samples.
4. Bad input (letters, empty text, unknown IDs) must never crash the
   program. Print "Please enter a number from 0 to 8." for bad menu
   choices. Use try/except/finally. Catch GearShareError and print
   "ERROR [R3]: ..." for rule errors and "ERROR [ClassName]: ..." for
   others, using the messages defined in the exception classes.
5. Tests...
6. README deliverables and requirements.
Add 2 entries to DECISIONS.md and this prompt to AI_LOG.md.

Read SPEC.md, Phase 1, task 1.1 and the Rental Rulebook. Design only, no code.

Create or overwrite docs/design.md with these sections:

1. Class diagram: one Mermaid `classDiagram` in a ```mermaid block.
2. Relationships: inheritance and composition.
3. Abstract contracts: GearItem and Customer methods.
4. CRC cards: Class, Responsibilities, Collaborators.
5. Short answers to the 4 Phase 1 questions.

Also save Mermaid code in docs/class-diagram.mmd, add 3 DECISIONS.md entries,
log this prompt in AI_LOG.md, and commit as
"1.1 Design: class diagram and CRC cards".

Read SPEC.md Phase 2 task 2.1 and the existing Phase 1 code.
Create dsa/__init__.py and benchmarks/generate_items.py, benchmark script,
report, tests, decisions, and log this prompt.

Read SPEC.md Phase 2 task 2.2 and the existing code.
Create dsa/search.py and dsa/sorting.py:
linear_search_by_name(items, name), binary_search(skus, target) with comparison counts,
bubble_sort, insertion_sort, and selection_sort with exact pass output, and catalogue_sort.
Create benchmarks/sort_compare.py and docs/sort_report.md using median timings of five runs
for 1k, 5k, and 10k names with hand-sort printing suppressed during timing.
Add search, sorting, edge-case, catalogue-order, and starter-data tests; add two DECISIONS.md
entries and log this prompt. Run pytest without committing.

Read SPEC.md Phase 2 task 2.3 and the existing code.
Create dsa/hashing.py and import_gear.py. Implement duplicate SKU detection,
tag grouping, most-rented frequency ranking, one-pass packing two-sum, and
word-to-SKU multi-word search. Add gear_with_duplicate.csv, hashing tests,
and two DECISIONS.md entries. Run pytest without git commands.

Read SPEC.md Phase 2 task 2.4 and the existing code.
Add GearShare undo stack entries and undo support for rent and return, update
the menu with option 9 and zero-to-nine input validation, and expose FIFO
waiting-list display. Add the linked rental history structure, stretch delete,
reverse and second-from-end operations, and list-versus-deque benchmark/report.
Add undo, waiting-list, and history tests plus two DECISIONS.md entries.
Run pytest without git commands.

Read SPEC.md Phase 2 task 2.5 and the existing code.
Create dsa/recursion.py with recursive factorial, Fibonacci, and digit sum
functions and required base-case comments. Create dsa/categories.py with a
real-data category Node tree, recursive print/count/path functions, and an
iterative stack count. Add docs/recursion_notes.md placeholders plus recursion
and category edge-case tests, and two DECISIONS.md entries. Run pytest without
git commands.

Read SPEC.md Phase 3 task 3.1 and the four starter CSVs in data/.
Do not break any earlier test. Do not run any git commands.

1. Create sql/build_flat.py that combines gear.csv, customers.csv,
   rentals.csv and fines.csv into data/gearshare_flat.csv, with one row
   per rental (10 rows) and exactly these columns in this order:
   rental_id, customer_name, email, tier, item_name, tags (as one
   ; separated cell), sku, category, parent_category, weight_g, price,
   issue_date, due_date, return_date, fine, fine_paid
   - parent_category is Photography for Cameras and Lenses, empty for
     the rest.
   - fine and fine_paid are empty when the rental has no fine.
   - Use the csv module, no hard-coded rows.
2. Create docs/normalisation.md with the heading "3.1 Anomalies" and
   three sections: Update anomaly, Insert anomaly, Delete anomaly. For
   each, use REAL rows from the flat file:
   - Update: Rohan's email changes, so how many rows must change?
   - Insert: where does Pooja Menon go when she has never rented, and
     where does the Vintage Leica go?
   - Delete: what happens to the only record of the SD card if RN005
     is deleted?
   Keep each section to 3 or 4 sentences.
3. Leave empty headings for 1NF, 2NF and 3NF in the same file (I will
   fill them in task 3.2). Do not write content under them.
4. Tests: the flat file has 10 rows and 16 columns, RN001 has an empty
   return_date, RN005 has fine 600 and fine_paid yes, RN009 has fine
   450 and fine_paid no.
5. Add 2 entries to DECISIONS.md and this prompt to AI_LOG.md.
Run pytest and fix failures.
