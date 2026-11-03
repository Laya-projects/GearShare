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
