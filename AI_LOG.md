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
