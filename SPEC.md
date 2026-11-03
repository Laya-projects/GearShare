# GearShare Mini: Python, DSA, SQL and React Project

One small rental business, built four times better: first as a Python program, then with proper data structures, then on a database, and finally as a website. **Total: 100 marks.**

This is a mini project covering Python + OOP, DSA, SQL and React JS. Every phase extends the work of the phase before it, and every phase has exact sample inputs and outputs so trainees can check their own work.

## The project question

FrameWorks Gear Rental lends cameras, lenses, drones, tripods and microphones to college media students, freelance creators and small studios. Everything is written in a paper register, and the staff keep making mistakes: renting expensive gear to customers who still owe fines, forgetting extensions, and losing track of who is waiting for a popular item.

**Your task:** build **GearShare Mini**. It must enforce the Rental Rulebook below, remember everything in a database, stay fast when the catalogue grows to 10,000 items, and give customers a website to search, rent and see their rentals.

You are not given code. You are given the rules, the data, the exact behaviour to reproduce, and questions that make you decide. Finding the *how* is the point.

## How the four phases connect

```
Phase 1: Python + OOP  ->  Phase 2: DSA  ->  Phase 3: SQL  ->  Phase 4: React
   Console engine          Fast and smart     Durable data      Website + API
```

```
Customer / Staff -> React website (P4) -> HTTP API (P4) -> Python engine: OOP + data structures (P1-2) -> SQL database (P3)
```

## Ground rules

- **Build on the previous phase.** Phase 2 extends Phase 1, Phase 3 sits underneath it, Phase 4 sits on top. When you add something, all earlier tests must still pass.
- **Match the samples exactly.** Messages, spacing and numbers in the sample blocks are the specification. Today's date for every sample is **2026-11-03**: run with `TODAY=2026-11-03`.
- **Money** is written like `₹100` with no decimals. **Dates** are `YYYY-MM-DD`.
- **Keep a decision log.** `DECISIONS.md` gets at least 3 entries per phase: the problem, the options, what you chose and why.
- **Commit often.** At least one commit per numbered task, with a message that says what changed.
- **The 20-minute rule.** Hints are given in each task. Try for 20 minutes first. If you read a hint, write one line about what you were missing.
- **Use AI tools to learn, not to skip learning.** Ask them to explain errors and concepts. You may not submit code you cannot explain; after each phase you will be asked to explain parts of your code.

---

## The Rental Rulebook

These rules are the client's requirements and apply in every phase. Refer to them by number (R1, R2, ...) in tests, commit messages and documents.

| Membership tier | Max items on rental | Rental period | Late fee per day |
|---|---|---|---|
| Basic | 2 | 3 days | ₹50 |
| Plus | 4 | 5 days | ₹100 |
| Pro | 8 | 7 days | ₹150 |

| Rule | Statement |
|---|---|
| R1 | Display items (showcase pieces) can be viewed in the shop but are never rented. |
| R2 | Accessories (memory cards, batteries) are rented for 2 days whatever the tier, and cannot be extended. |
| R3 | A customer cannot have more items on rental than their tier allows. |
| R4 | A customer whose unpaid fines are above ₹500 cannot rent until they pay. |
| R5 | Late fee = days late x the tier's daily rate, never more than the item's replacement price. |
| R6 | Equipment can be extended up to 2 times. Each extension adds the tier's rental period to the current due date. No extension if another customer is on the waiting list for that item. |
| R7 | If no unit is free, a customer may join the waiting list. The first person in the list is served first. |
| R8 | A customer cannot hold two units of the same item at once. |
| R9 | A SKU is exactly 10 digits (no checksum) and identifies one item. It is unique. |
| R10 | Returning on the due date is not late. The first late day is the day after. |

### Order of checks when renting

When several rules are broken at once, only the **first one** in this list is reported. This makes every sample deterministic.

1. The customer exists (`CustomerNotFoundError`)
2. The SKU has 10 digits (`InvalidSKUError`) and exists (`ItemNotFoundError`)
3. R1: the item is not a display item
4. R4: unpaid fines are not above ₹500
5. R3: the customer is below their item limit
6. R8: the customer does not already hold a unit of this item
7. Availability: if no unit is free, offer the waiting list (R7)

### Worked examples: use these as your first test cases

**Due dates.** Issue date 2026-11-03.

| Tier | Item | Due date | Why |
|---|---|---|---|
| Basic | Equipment | 2026-11-06 | 3 days |
| Plus | Equipment | 2026-11-08 | 5 days |
| Pro | Equipment | 2026-11-10 | 7 days |
| Pro | Accessory | 2026-11-05 | R2: 2 days whatever the tier |

**Late fees.**

| Tier | Item (price) | Due | Returned | Days late | Fee |
|---|---|---|---|---|---|
| Basic | Equipment (₹45000) | 2026-10-31 | 2026-10-31 | 0 | ₹0 (R10) |
| Basic | Equipment (₹45000) | 2026-10-31 | 2026-11-01 | 1 | ₹50 |
| Plus | Equipment (₹38000) | 2026-10-29 | 2026-11-03 | 5 | ₹500 |
| Pro | Equipment (₹22000) | 2026-09-30 | 2026-10-30 | 30 | ₹4500 |
| Basic | Accessory (₹600) | 2026-08-03 | 2026-08-23 | 20 | ₹600 (1000 capped at the price, R5) |

### Starter data

Copy each block into a file with the name shown. All outputs and expected query results are based on exactly this data. `return_date` is empty when the item has not been returned yet, and `;` separates multiple tags.

**gear.csv**

```csv
sku,name,tags,category,parent_category,item_type,weight_g,price,total_units
1000000001,Canon EOS 200D,photo;dslr,Cameras,Photography,Equipment,450,45000,2
1000000002,Sony 50mm Lens,photo;lens,Lenses,Photography,Equipment,280,18000,1
1000000003,DJI Mini Drone,video;aerial,Drones,,Equipment,249,38000,1
1000000004,Manfrotto Tripod,support,Tripods,,Equipment,1200,6000,2
1000000005,Rode Wireless Mic,audio;interview,Audio,,Equipment,120,22000,1
1000000006,Vintage Leica (Showcase),display,Showcase,,Display,600,150000,1
1000000007,SD Card 128GB,storage,Accessories,,Accessory,2,600,3
```

**customers.csv**

```csv
customer_id,name,email,membership_type
C001,Ananya Nair,ananya@example.com,Basic
C002,Vikram Shah,vikram@example.com,Plus
C003,Meera Joshi,meera@example.com,Pro
C004,Rohan Das,rohan@example.com,Basic
C005,Pooja Menon,pooja@example.com,Plus
```

**rentals.csv**

```csv
rental_id,customer_id,sku,issue_date,due_date,return_date
RN001,C002,1000000003,2026-10-24,2026-10-29,
RN002,C004,1000000001,2026-10-28,2026-10-31,
RN003,C003,1000000004,2026-10-30,2026-11-06,
RN004,C001,1000000002,2026-09-10,2026-09-13,2026-09-13
RN005,C001,1000000007,2026-08-01,2026-08-03,2026-08-23
RN006,C003,1000000003,2026-08-05,2026-08-12,2026-08-10
RN007,C002,1000000001,2026-07-10,2026-07-15,2026-07-15
RN008,C002,1000000005,2026-06-01,2026-06-06,2026-06-09
RN009,C004,1000000005,2026-07-01,2026-07-04,2026-07-13
RN010,C004,1000000001,2026-07-20,2026-07-23,2026-07-26
```

**fines.csv**

```csv
rental_id,amount,paid
RN005,600,yes
RN008,300,yes
RN009,450,no
RN010,150,no
```

Customer IDs are text such as `C001`; rental IDs are text such as `RN001`. A new rental gets the next number (`RN011`). Customer C005 (Pooja Menon) has never rented, and the Vintage Leica has never been rented. Both are there on purpose. Rohan Das owes ₹450 + ₹150 = ₹600 in unpaid fines, which is above the R4 limit.

---

# Phase 1: The Console Engine

**Training phase:** Python + OOP | **Marks:** 25

**The task.** Build a console program that enforces the Rental Rulebook, so nobody has to remember who may rent what. It reads the starter data files, runs a menu, and prints messages exactly as shown in the samples below, so your output can be compared line by line.

**Topics from your sheet that this phase uses:** Python Basics (setup and syntax); Functions, Lists and Strings; OOP: Classes, Objects and `__init__`; OOP: Inheritance and Polymorphism; OOP: Encapsulation/Abstraction and Collections/Exceptions; Pythonic Essentials; Python + OOP Review.

## 1.1 Design on paper first

- Read the Rulebook and the order of checks. Underline every noun (candidate class) and every verb (candidate method).
- Draw a class diagram: `GearItem` (abstract) with `Equipment`, `Accessory`, `DisplayItem`; `Customer` (abstract) with `BasicCustomer`, `PlusCustomer`, `ProCustomer`; `Rental`; `GearShare` (the service class).
- For each relationship decide: inheritance (is-a) or composition (has-a). Write one sentence defending each.
- Decide what each abstract class forces its subclasses to answer. (A display item cannot be rented. A Basic customer has a 3-day period. Where does that knowledge live?)

> **Hint (after 20 minutes):** Every customer type must answer the same three questions with different values: how many items, how many days, how much fee per day. If you wrote `if tier == 'Basic'` anywhere, polymorphism is missing.

## 1.2 Build the classes

- Create the files `items.py`, `customers.py`, `rentals.py`, `errors.py`, `gearshare.py`, `main.py`.
- Use `@property` with setters so invalid objects can never exist: SKU must be exactly 10 digits, units cannot be negative, name cannot be blank, email must contain `@`.
- Make rental period, item limit and daily late fee polymorphic methods. Add `__str__` and `__repr__` to every class.
- Use one class attribute (for example the next rental number) and one instance attribute, and write a comment explaining why each belongs where it is.

## 1.3 The service class and the exceptions

- Create the exception hierarchy. `GearShareError` is the parent. Its children are `InvalidSKUError`, `ItemNotFoundError`, `CustomerNotFoundError`, `ItemNotRentableError` (R1), `UnpaidFinesError` (R4), `RentalLimitExceededError` (R3), `DuplicateRentalError` (R8), `ItemNotAvailableError` (R7), `ExtensionNotAllowedError` (R2, R6).
- Build `GearShare` with `load_data()`, `list_items()`, `rent()`, `return_item()`, `extend()`, `join_waiting_list()`, `customer_rentals()`, `overdue_report()`.
- Pass `today` into every date-dependent method instead of calling `date.today()` inside it. Read it from the `TODAY` environment variable in `main.py` (fallback: the real date).
- Store data in collections that fit: a dict by SKU, a dict by customer ID, a list of rentals, a set of SKUs. Write down why in `DECISIONS.md`.
- Error messages must match the samples character for character: `ERROR [R3]: ...` for rule violations and `ERROR [ClassName]: ...` for the others.

## 1.4 The Pythonic layer

- Write a decorator `@audit` that appends time, action, customer and item to a list each time `rent`, `return_item` or `extend` succeeds.
- Write a generator `iter_overdue(today)` that yields overdue rentals one at a time. The overdue report must consume it.
- Write the three reports with comprehensions and `sorted(key=lambda ...)`: overdue (most days late first), items by category, customers with unpaid fines. Use `map` or `filter` at least once where it reads better than a loop.

## 1.5 Menu, files and tests

- Read the three CSV files (file input/output) and rebuild each item's availability from the rentals that have no return date.
- Build the menu loop. Bad input (letters, empty text, unknown IDs) must never crash the program. Use `try/except/finally`.
- Set up `venv`, `requirements.txt` and `pytest`. Write at least 20 tests: every rule R1 to R10 at least once, plus the two worked-example tables as `@pytest.mark.parametrize` cases.
- Every exception must have a test that expects it (`pytest.raises`).

> **Hint (after 20 minutes):** Because `today` is a parameter, a test can say 'return this rental on 2026-11-03' without waiting for the real date.

## Sample input and output for Phase 1

### Start-up and menu

```
$ TODAY=2026-11-03 python main.py
Loaded 7 items, 5 customers, 10 rentals, 4 fines.
Today is 2026-11-03.

=== GearShare Mini ===
1. List catalogue
2. Search by name or tag
3. Rent
4. Return
5. Extend
6. Join waiting list
7. Customer rentals
8. Overdue report
0. Exit
> abc
Please enter a number from 0 to 8.
>
Please enter a number from 0 to 8.
```

Availability is rebuilt from the rentals file: rentals RN001, RN002 and RN003 have no return date, so those units are out.

### Option 1: list the catalogue

```
> 1
SKU         NAME                       TYPE       AVAILABLE
1000000001  Canon EOS 200D             Equipment  1 of 2
1000000002  Sony 50mm Lens             Equipment  1 of 1
1000000003  DJI Mini Drone             Equipment  0 of 1
1000000004  Manfrotto Tripod           Equipment  1 of 2
1000000005  Rode Wireless Mic          Equipment  1 of 1
1000000006  Vintage Leica (Showcase)   Display    not rentable
1000000007  SD Card 128GB              Accessory  3 of 3
```

### Option 2: search (case-insensitive, name or tag)

```
> 2
Search: VIDEO
1 result:
1000000003  DJI Mini Drone (video, aerial)  0 of 1

> 2
Search: zzz
No items match 'zzz'.
```

### Session A: run these in order from a fresh start

```
> 3
Customer ID: C001
SKU: 1000000002
OK: Ananya Nair rented 'Sony 50mm Lens'. Due 2026-11-06.

> 3
Customer ID: C001
SKU: 1000000002
ERROR [R8]: Ananya Nair already has a unit of 'Sony 50mm Lens'.

> 3
Customer ID: C003
SKU: 1000000006
ERROR [R1]: 'Vintage Leica (Showcase)' is a display item and cannot be rented.

> 3
Customer ID: C004
SKU: 1000000004
ERROR [R4]: Rohan Das has unpaid fines of ₹600 (limit ₹500).

> 3
Customer ID: C003
SKU: 1000000003
No units of 'DJI Mini Drone' are available. Join the waiting list? (y/n): y
OK: Meera Joshi is #1 on the waiting list for 'DJI Mini Drone'.

> 4
Rental ID: RN001
OK: Vikram Shah returned 'DJI Mini Drone'. Late by 5 days. Fee: ₹500.
Next on waiting list: Meera Joshi.
```

Vikram's fee is exactly ₹500, and R4 blocks only fines **above** ₹500. A new rental for Vikram would still be allowed. Is yours?

### Other error paths

```
> 3
Customer ID: C009
ERROR [CustomerNotFoundError]: No customer with ID C009.

> 3
Customer ID: C001
SKU: 123
ERROR [InvalidSKUError]: SKU must be exactly 10 digits.

> 3
Customer ID: C001
SKU: 1000000999
ERROR [ItemNotFoundError]: No item with SKU 1000000999.

(after Ananya has rented the Sony Lens and the SD Card)
> 3
Customer ID: C001
SKU: 1000000004
ERROR [R3]: Ananya Nair already has 2 of 2 items on rental.
```

### Return on time, and extensions

```
> 4
Rental ID: RN003
OK: Meera Joshi returned 'Manfrotto Tripod'. Returned on time. Fee: ₹0.

(with RN003 still open)
> 5
Rental ID: RN003
OK: Extended 'Manfrotto Tripod' (extension 1 of 2). New due date 2026-11-13.

> 5
Rental ID: RN003
OK: Extended 'Manfrotto Tripod' (extension 2 of 2). New due date 2026-11-20.

> 5
Rental ID: RN003
ERROR [R6]: 'Manfrotto Tripod' has already been extended 2 times.

(RN011 is an SD card rental created earlier in the session)
> 5
Rental ID: RN011
ERROR [R2]: Accessories cannot be extended.

(someone is on the waiting list for the item)
> 5
Rental ID: RN003
ERROR [R6]: 'Manfrotto Tripod' cannot be extended because another customer is waiting.
```

Notice that rental RN003 appears in two different situations. In each of your tests, set up the starting state yourself and never rely on an earlier test.

### Option 7: customer rentals

```
> 7
Customer ID: C002
Rentals for Vikram Shah (Plus: 4 items, 5 days, ₹100/day)
RENTAL  ITEM            ISSUED      DUE         STATUS
RN001   DJI Mini Drone  2026-10-24  2026-10-29  OVERDUE (5 days)
Active rentals: 1 of 4
Unpaid fines: ₹0
```

A rental that is not overdue shows the status `On rental`.

### Option 8: overdue report (fresh start)

```
> 8
Overdue rentals as of 2026-11-03
RENTAL  CUSTOMER     ITEM             DUE         DAYS  FINE SO FAR
RN001   Vikram Shah  DJI Mini Drone   2026-10-29  5     ₹500
RN002   Rohan Das    Canon EOS 200D   2026-10-31  3     ₹150
Total overdue: 2   Fines so far: ₹650
```

Sorted by days late, most late first. 'Fine so far' is calculated but not yet saved: it only becomes a real fine when the item is returned.

## Think about this before and while you build

1. Why is it better for `rent()` to raise an exception than to return `False`? What does the caller lose with `False`?
2. The check order is fixed. Swap R4 and R3 in your head. Which sample above would now print a different message?
3. Where should fine calculation live: `Rental`, `Customer` or `GearShare`? Argue for one and against it.
4. A customer is upgraded from Basic to Pro while holding 2 items. Which limit and fee rate apply to the existing rentals? What does your design make easy or hard?

## What to hand in

- Project folder with the files above, `requirements.txt` and a README explaining how to run with `TODAY=2026-11-03`
- Class diagram (image or photo) and CRC cards
- `pytest` output with 20+ passing tests
- A table in the README: rule (R1 to R10), method that enforces it, test that proves it
- `DECISIONS.md` with at least 3 design decisions and the alternatives you rejected

## You are done when

- Every sample transcript above reproduces exactly
- There is no `if tier ==` anywhere in the code
- Bad menu input never crashes the program
- Another trainee can run it from a clean copy using only your README

---

# Phase 2: Make It Fast and Smart

**Training phase:** DSA | **Marks:** 20

**The task.** The shop now has 10,000 items. Searching feels slow, customers want a waiting list that is fair, staff want an undo button, and the owner wants to browse a category tree. You improve the Phase 1 engine with data structures and prove each improvement with measurements, not opinions. All Phase 1 tests must still pass, and the menu gains option 9 (undo).

**Topics from your sheet that this phase uses:** Arrays, Strings, Time Complexity, Searching and Sorting; Hashing; Stacks, Queues and Linked Lists; Recursion, Problem Solving and Assessment.

## 2.1 Complexity audit

- Write a script that generates 10,000 fake items (valid SKUs, names, tags, weights) and loads them into `GearShare`.
- Make a table for `list_items`, `search`, `rent`, `return_item` and `overdue_report`. Write your **predicted** time and space Big-O *before* measuring.
- Measure with `time.perf_counter()` at n = 1,000 / 5,000 / 10,000 / 50,000. Compare predictions with results and write two sentences on every surprise.

> **Hint (after 20 minutes):** Run each measurement several times and use the median. A single run is noise.

## 2.2 Searching and sorting

- Implement linear search by name and binary search by SKU on a sorted list. Handle: empty list, one element, first element, last element, not found.
- Implement bubble, insertion and selection sort by hand to sort names. Each prints the list after every pass, exactly like the sample.
- Compare your three sorts with Python's `sorted(key=...)` on 1k, 5k and 10k items and put the times in a table.
- Add the catalogue sort the website will use later: top-level category ascending, then weight descending, then name ascending.

> **Hint (after 20 minutes):** For mixed directions, sort in two passes (Python's sort is stable) or use a tuple key with a negated number.

## 2.3 Hashing

- **Duplicates:** when importing a gear CSV, detect repeated SKUs with a `set` and report the line number of each duplicate.
- **Grouping:** build a dict from tag to list of item names (split the `;`-separated tags).
- **Frequency counting:** from `rentals.csv`, produce the most-rented items (ties broken alphabetically).
- **Packing challenge (two-sum):** given a target weight in grams, find two different rentable items whose weights add up to it, in one pass using a dict. Display items are excluded.
- **Stretch:** build a word-to-SKU index for instant multi-word search.

> **Hint (after 20 minutes):** For the packing challenge, as you look at each item, what other weight would you need to have already seen?

## 2.4 Stacks, queues and linked lists

- **Undo (stack):** keep the last rent/return operations on a stack. Option 9 reverses the latest one. First decide what each stack entry must store so the action can truly be reversed.
- **Waiting list (queue):** each fully rented SKU has a `collections.deque` of customer IDs. A returned unit notifies the first in the queue (R7).
- Benchmark `list.pop(0)` against `deque.popleft()` on 100,000 entries. Record the difference.
- **Rental history (singly linked list):** write `Node` and `RentalHistory` with insert at head and traversal. Printing shows the newest rental first.
- **Stretch:** delete a node by rental ID, reverse the list, find the 2nd node from the end.

## 2.5 Recursion

- **Warm-up:** write `factorial(n)`, `fibonacci(n)` and `sum_of_digits(n)` recursively. For each, write the base case and how the problem gets smaller *before* the code.
- Model the categories as a tree (Gear Hub, Photography, Cameras). Write recursive functions to print the tree with item counts, count all items under a category, and find the path to a category.
- Write an iterative version of one of them. Which is clearer? Which would you use at depth 10,000? What does `sys.setrecursionlimit` change, and what does it not fix?

## Sample input and output for Phase 2

### 2.1 Benchmark table (illustrative: your numbers will differ)

| n | linear_ms | binary_ms | sorted_key_ms | insertion_ms |
|---|---|---|---|---|
| 1,000 | 0.05 | 0.002 | 0.4 | 38.0 |
| 5,000 | 0.24 | 0.003 | 2.1 | 960.0 |
| 10,000 | 0.47 | 0.003 | 4.5 | 3,900.0 |

What matters is the shape: one column barely moves, one roughly doubles, one roughly quadruples when n doubles. Explain which is which.

### 2.2 Sorting by hand: input `[6, 3, 5, 2]`

```
bubble_sort([6, 3, 5, 2])
after pass 1: [3, 5, 2, 6]
after pass 2: [3, 2, 5, 6]
after pass 3: [2, 3, 5, 6]

insertion_sort([6, 3, 5, 2])
after inserting index 1: [3, 6, 5, 2]
after inserting index 2: [3, 5, 6, 2]
after inserting index 3: [2, 3, 5, 6]

selection_sort([6, 3, 5, 2])
after pass 1 (min=2): [2, 3, 5, 6]
after pass 2 (min=3): [2, 3, 5, 6]
after pass 3 (min=5): [2, 3, 5, 6]
```

### 2.2 Binary search on the sorted starter SKUs

```
skus = ['1000000001', '1000000002', '1000000003', '1000000004',
        '1000000005', '1000000006', '1000000007']

binary_search(skus, '1000000006') -> 5   (2 comparisons)
binary_search(skus, '1000000008') -> -1  (3 comparisons)
binary_search([], '1000000001')   -> -1  (0 comparisons)
```

### 2.2 Catalogue sort: category, then weight (high to low), then name

```
Accessories   SD Card 128GB              2
Audio         Rode Wireless Mic          120
Drones        DJI Mini Drone             249
Photography   Canon EOS 200D             450
Photography   Sony 50mm Lens             280
Showcase      Vintage Leica (Showcase)   600
Tripods       Manfrotto Tripod           1200
```

'Category' here means the **top-level** category: Cameras and Lenses both count as Photography.

### 2.3 Hashing: duplicates, grouping, frequency, two-sum

```
$ python import_gear.py gear_with_duplicate.csv
Line 9: duplicate SKU 1000000004 (already used by 'Manfrotto Tripod'), skipped.
Imported 8 rows: 7 added, 1 duplicate skipped.

group_by_tag():
aerial: DJI Mini Drone
audio: Rode Wireless Mic
display: Vintage Leica (Showcase)
dslr: Canon EOS 200D
interview: Rode Wireless Mic
lens: Sony 50mm Lens
photo: Canon EOS 200D, Sony 50mm Lens
storage: SD Card 128GB
support: Manfrotto Tripod
video: DJI Mini Drone

most_rented(3):
1. Canon EOS 200D     3
2. DJI Mini Drone     2
3. Rode Wireless Mic  2

packing_challenge(730)  -> Canon EOS 200D (450) + Sony 50mm Lens (280) = 730
packing_challenge(1320) -> Manfrotto Tripod (1200) + Rode Wireless Mic (120) = 1320
packing_challenge(1000) -> No pair found.
```

The duplicate file is your starter `gear.csv` plus one extra line that repeats SKU 1000000004. You create it yourself.

### 2.4 Undo, waiting list and rental history

```
> 3
Customer ID: C001
SKU: 1000000002
OK: Ananya Nair rented 'Sony 50mm Lens'. Due 2026-11-06.

> 9
OK: Undid rental of 'Sony 50mm Lens' by Ananya Nair (rental RN011 removed).

> 9
Nothing to undo.

(Meera, then Pooja, joined the waiting list for 'DJI Mini Drone' earlier)
Waiting list for 'DJI Mini Drone': Meera Joshi, Pooja Menon

> 4
Rental ID: RN001
OK: Vikram Shah returned 'DJI Mini Drone'. Late by 5 days. Fee: ₹500.
Next on waiting list: Meera Joshi.
Waiting list for 'DJI Mini Drone': Pooja Menon

Rental history, Vikram Shah (newest first):
RN001 -> RN007 -> RN008 -> None
Rental history, Meera Joshi (newest first):
RN003 -> RN006 -> None
```

### 2.5 Recursion

```
factorial(6)       -> 720
fibonacci(8)       -> 21     # fibonacci(0)=0, fibonacci(1)=1
sum_of_digits(5078) -> 20

print_tree(root):
Gear Hub (7)
  Accessories (1)
  Audio (1)
  Drones (1)
  Photography (2)
    Cameras (1)
    Lenses (1)
  Showcase (1)
  Tripods (1)

count_items('Photography') -> 2
path_to('Lenses')   -> ['Gear Hub', 'Photography', 'Lenses']
path_to('Lighting') -> None
```

## Think about this before and while you build

1. Binary search needs sorted data. If a user searches once, is sorting first worth it? After how many searches does it pay off?
2. Why can't you simply push the `Rental` object onto the undo stack? What if the rental was removed since?
3. Why is `pop(0)` on a list slow, and what does `deque` do differently inside?
4. In which of the five recursion tasks would recursion be the wrong choice, and why?

## What to hand in

- `dsa/` package: `search.py`, `sorting.py`, `hashing.py`, `history.py`, `categories.py`
- Benchmark report (1 to 2 pages): predicted vs measured Big-O table, sort comparison, `pop(0)` vs `popleft` result, conclusions
- New tests for every structure; all Phase 1 tests still green
- `DECISIONS.md` updated: which structure for which feature, and why

## You are done when

- Every sample above reproduces exactly
- The waiting list serves reservations strictly first come, first served
- Undo works for both rent and return
- You can explain each Big-O in your table without looking at it

---

# Phase 3: Durable Data

**Training phase:** Database (SQL) | **Marks:** 25

**The task.** Close the program and the shop forgets who rented what. You design a proper database, load the starter data, answer the owner's business questions in SQL, and then connect your Python engine to the database so everything survives a restart.

**Topics from your sheet that this phase uses:** SQL Fundamentals, Joins and Aggregations; Database Design and Normalization; DML, Transactions and Indexes; Connecting Python to a Database.

## Part A: Design and SQL

### 3.1 Start from a mess

- Combine the four starter CSVs into one flat file `gearshare_flat.csv` with one row per rental: rental ID, customer name, email, tier, item name, tags (as one cell), SKU, category, parent category, weight, price, issue date, due date, return date, fine, fine paid.
- Write three concrete anomalies using real rows: one update, one insert, one delete anomaly. (Examples to think about: Rohan's email changes, where does Pooja Menon go when she has never rented, what happens to the only record of the SD card if RN005 is deleted?)

### 3.2 Normalise step by step

- Take the flat file to **1NF**. What repeats inside a cell? Show before and after.
- Take it to **2NF**: which columns depend on only part of the key? Split them out.
- Take it to **3NF**: which columns depend on other non-key columns? (Think about tier and its limits, and category and its parent.) Split them out.
- List your final tables. You should find roughly: `customers`, `membership_tiers`, `items`, `tags`, `item_tags`, `categories` (self-reference via parent), `rentals`, `fines`, `waiting_list`, `audit_log`.
- Record in `DECISIONS.md`: is *available units* stored in a column or calculated? Argue both sides, pick one, and say when you would choose differently (when to denormalise).

### 3.3 ER diagram and schema

- Draw the ER diagram in dbdiagram.io. Show the cardinality of every relationship.
- Write `schema.sql` with primary keys, foreign keys, `NOT NULL`, `UNIQUE` (SKU, email) and `CHECK` constraints (due date not before issue date, units not negative, fine not negative).
- For every foreign key choose the `ON DELETE` behaviour on purpose. What should happen to a customer's rentals if the customer is deleted?
- Use SQLite (built into Python) or PostgreSQL. Either is fine, but keep the same choice for Part B.

### 3.4 Load the starter data

- Write `seed.sql` (or a loader script) that fills your tables from the starter CSVs. After loading, the counts must be: **7 items, 10 tags, 5 customers, 10 rentals, 4 fines, 8 categories** (the 7 categories used by items, plus Photography as the parent of two of them).
- Check: the count of rentals with no return date must be **3**.

> **Hint (after 20 minutes):** Tags appear as `a;b` in one cell. Splitting that cell is the whole point of the junction table.

### 3.5 The query pack

- Write the 12 queries in `queries.sql` and compare each result with the expected output below. Put the business question as a comment above each query.
- Next to each query write which kind of join you used and why that one and not another.

> **Hint (after 20 minutes):** Q5 and Q6 cannot be answered with an `INNER JOIN` alone. Ask yourself what you need to keep in the result even when there is no match.

### 3.6 Transactions and indexes

- Write *rent* as one transaction: check the item is available, insert the rental, insert a row in `audit_log`. Show it succeeding.
- Break it on purpose at the last statement (for example, violate a constraint in `audit_log`). Show `ROLLBACK` leaves the `rentals` table unchanged. See the sample.
- Generate 100,000 rentals. Pick the 2 slowest queries, run `EXPLAIN` before and after adding an index, and record the difference.
- Name one index you decided **not** to create and say why.

## Part B: Python meets the database

### 3.7 Connect the engine

- Add a `storage/` package. Write a class for each table group (items, customers, rentals) that uses the DB-API (`sqlite3` or `psycopg2`) with **parameterised queries only**.
- Make `GearShare` read and write through these classes instead of lists and CSV files. Keep your exception messages and menu output identical to Phase 1.
- Make each business operation commit or roll back as one unit (use a context manager).
- Run all Phase 1 tests again. They must pass with the database underneath (use a fresh temporary database per test).
- *Optional path:* do the same with SQLAlchemy ORM and write 5 lines on which you prefer.

> **Hint (after 20 minutes):** If `GearShare` contains the text `sqlite3` or `SELECT`, the layers are tangled.

### 3.8 The injection experiment

- In a throwaway file write a deliberately unsafe search that builds SQL with an f-string. Attack it with `' OR '1'='1`.
- Fix it with a parameterised query and show the same input failing. Keep both versions' output as evidence.

## Sample input and output for Phase 3

### Expected results of the 12 queries (today = 2026-11-03)

**Q1** Items tagged 'photo', with all their tags

```
name            | tag
Canon EOS 200D  | dslr
Canon EOS 200D  | photo
Sony 50mm Lens  | lens
Sony 50mm Lens  | photo
```

**Q2** Items currently on rental, and who has them

```
rental_id | customer     | item
RN001     | Vikram Shah  | DJI Mini Drone
RN002     | Rohan Das    | Canon EOS 200D
RN003     | Meera Joshi  | Manfrotto Tripod
```

**Q3** Overdue rentals with days overdue

```
customer     | item            | due_date   | days_overdue
Vikram Shah  | DJI Mini Drone  | 2026-10-29 | 5
Rohan Das    | Canon EOS 200D  | 2026-10-31 | 3
```

**Q4** Top 3 items by number of rentals (ties broken by name)

```
item              | rentals
Canon EOS 200D    | 3
DJI Mini Drone    | 2
Rode Wireless Mic | 2
```

**Q5** Items that have never been rented

```
name
Vintage Leica (Showcase)
```

**Q6** Customers with no rental in the last 90 days (since 2026-08-05)

```
name
Pooja Menon
```

**Q7** Total fines per tier per month (month the item was returned)

```
tier  | month   | total_fines
Basic | 2026-07 | 600
Basic | 2026-08 | 600
Plus  | 2026-06 | 300
```

**Q8** Fines paid vs pending

```
status  | total
Paid    | 900
Pending | 600
```

**Q9** Customers who rented from at least 3 different categories

```
name        | categories
Vikram Shah | 3
```

**Q10** Categories where the average completed rental lasts more than 4 days

```
category    | avg_days
Accessories | 22.0
Audio       | 10.0
Cameras     | 5.5
Drones      | 5.0
```

**Q11** Units available right now, per item

```
name                     | available
Canon EOS 200D           | 1
Sony 50mm Lens           | 1
DJI Mini Drone           | 0
Manfrotto Tripod         | 1
Rode Wireless Mic        | 1
Vintage Leica (Showcase) | 1
SD Card 128GB            | 3
```

**Q12** The pair of items most often rented by the same customer

```
item_a         | item_b            | customers
Canon EOS 200D | Rode Wireless Mic | 2
```

Write each query's question yourself from this expected output. Column names are suggestions: your results must match in values, not necessarily in column names. The display item shows 1 available only because nobody can rent it, so decide how your query should treat it and note it in `DECISIONS.md`.

### 3.6 Transaction demo (expected behaviour)

```sql
-- before
SELECT COUNT(*) FROM rentals WHERE rental_id = 'RN011';  -- 0
SELECT COUNT(*) FROM audit_log;                          -- 0

-- attempt 1: the audit insert violates a constraint on purpose
BEGIN;
INSERT INTO rentals ... 'RN011', 'C001', '1000000002', '2026-11-03', '2026-11-06';
INSERT INTO audit_log ... (violates NOT NULL);  -- ERROR
ROLLBACK;
SELECT COUNT(*) FROM rentals WHERE rental_id = 'RN011';  -- still 0

-- attempt 2: correct statements
BEGIN;
INSERT INTO rentals ...;
INSERT INTO audit_log ...;
COMMIT;
SELECT COUNT(*) FROM rentals WHERE rental_id = 'RN011';  -- 1
SELECT COUNT(*) FROM audit_log;                          -- 1
```

### 3.7 Persistence check

```
$ TODAY=2026-11-03 python main.py
> 3
Customer ID: C001
SKU: 1000000002
OK: Ananya Nair rented 'Sony 50mm Lens'. Due 2026-11-06.
> 0

$ TODAY=2026-11-03 python main.py
> 7
Customer ID: C001
Rentals for Ananya Nair (Basic: 2 items, 3 days, ₹50/day)
RENTAL  ITEM            ISSUED      DUE         STATUS
RN011   Sony 50mm Lens  2026-11-03  2026-11-06  On rental
Active rentals: 1 of 2
Unpaid fines: ₹0
```

The program was closed and reopened. In Phase 1 this rental would have disappeared.

### 3.8 The injection experiment (7 items in the table)

```
search_unsafe("Drone")        -> 1 row
search_unsafe("' OR '1'='1")  -> 7 rows (every item leaked)
search_safe("' OR '1'='1")    -> 0 rows
search_safe("Drone")          -> 1 row
```

## Think about this before and while you build

1. Is availability a fact you *store* or a fact you *calculate*? What breaks in each design when two rent requests arrive together?
2. What does `ON DELETE CASCADE` from customer to rentals do to the shop's history? Who might object?
3. Which of the 12 queries would you worry about at 10 million rentals, and what would you do about it?
4. What exactly did the parameterised query do differently from the f-string version?

## What to hand in

- `schema.sql`, `seed.sql`, `queries.sql` (12 queries with comments), `tx_demo.sql`
- ER diagram and a normalisation write-up (1NF, 2NF, 3NF) using the flat file as the example
- Index report: `EXPLAIN` before and after for 2 queries
- `storage/` package, with all Phase 1 tests passing on the database
- Injection experiment evidence and an updated `DECISIONS.md`

## You are done when

- All 12 query results match the expected output
- Counts after loading: 7 items, 5 customers, 10 rentals, 4 fines, 3 open rentals
- No SQL is built with string formatting anywhere in the program (except your deliberate unsafe demo file)
- You have shown a rolled-back transaction leaving no trace

---

# Phase 4: The Website

**Training phase:** React JS | **Marks:** 30

**The task.** Customers can't use a console program. The owner wants a website where customers search the catalogue, see what is available, fill a rental basket and view their own rentals. This is the small, real-shaped full-stack app from your React mini-project row: a React front end, an HTTP API in front of your Python engine, and your database underneath.

**Topics from your sheet that this phase uses:** Modern JavaScript Refresher and Environment Setup; React Basics (JSX, Components and Props); State, Events and Component Lifecycle (`useState`, `useEffect`); Conditional Rendering, Lists and Forms; React Router Basics; State Management Beyond `useState`; Calling APIs, Styling and Component Libraries; React Mini Project and Review.

## 4.0 Put an HTTP API in front of your engine

A web framework is not part of the training plan, so a short introduction to FastAPI (recommended) or Flask comes before this task. Use the framework's official tutorial alongside it.

- Create the endpoints in the sample below. Each one calls your existing `GearShare` methods. **Do not copy rules into the API.**
- Convert every custom exception into an HTTP status and a JSON body `{"error": "R3", "message": "..."}` using the same message text as the console. Decide for each exception which status fits and write why.
- Allow requests only from the origin of your React development server (CORS). Read `TODAY` from the environment as before.

> **Hint (after 20 minutes):** 404 means the thing doesn't exist. 409 means it exists but its state conflicts with the request. 422 means the input itself doesn't make sense.

## 4.1 Set up and wireframe

- Create a Vite React app in `web/`. Keep the API URL in an environment variable.
- Sketch five screens on paper: Catalogue, Item details, My rentals, Rental basket, Add item (staff).
- Draw the component tree. Next to every component write the **state it owns** and the **props it receives**. If you can't say who owns a piece of state, you aren't ready to code.

## 4.2 Components and props

- Build `Navbar`, `Layout` (using `children`), `GearCard`, `GearList` and `AvailabilityBadge` with hard-coded JSON first.
- Every component receives what it needs by props and knows nothing about where the data came from.

## 4.3 State, events and effects

- Add a controlled search box, a category filter and a sort dropdown that all control the same list.
- Fetch from the API in `useEffect` with a correct dependency array. Debounce typing, and cancel the old request in the cleanup function (`AbortController`).
- Throttle the network to 'Slow 3G' in the browser tools and type quickly. Does an old response ever overwrite a newer one? Fix it if it does.

## 4.4 Conditional rendering, lists and forms

- Render different UI for loading, error, empty and results. Show 'Join waiting list' instead of 'Add to basket' when nothing is available.
- Render lists with a stable `key` (the SKU). Be ready to explain what goes wrong with the array index.
- Build the staff Add item form with controlled inputs and validation: SKU exactly 10 digits, units at least 1, name required. Errors appear next to the field and submit stays disabled until valid.

## 4.5 Routing

- Routes: `/` catalogue, `/gear/:sku` details, `/me` my rentals, `/basket`, `/admin/add`, plus a friendly 404 page.
- A 'Back to results' link must restore the previous search. Where must the search text live for that to work?

## 4.6 State beyond useState

- Create a `CustomerContext` that holds 'who am I' (a customer picker in the navbar is enough; no passwords).
- Create the basket with `useReducer`: actions `ADD`, `REMOVE`, `CLEAR`. It blocks adding more than the customer's limit (2 / 4 / 8) with a message.
- On checkout, call `POST /rentals` for each item. The server has the last word. Show its message to the customer exactly.

## 4.7 Styling, responsiveness, polish

- Pick Tailwind or Material UI and use it consistently.
- Every screen must work at 360 px width. Every input has a label, every image an `alt`, every action is reachable by keyboard.

## Sample input and output for Phase 4

### 4.0 API requests and responses (`TODAY=2026-11-03`)

```
GET /gear?q=drone&sort=name
200 [
  {"sku": "1000000003", "name": "DJI Mini Drone",
   "tags": ["video", "aerial"], "category": "Drones",
   "item_type": "Equipment", "available": 0, "total": 1, "weight_g": 249}
]

GET /gear?q=zzz
200 []

GET /gear/1000000999
404 {"error": "ItemNotFoundError", "message": "No item with SKU 1000000999."}

POST /rentals
{"customer_id": "C001", "sku": "1000000002"}
201 {"rental_id": "RN011", "due_date": "2026-11-06"}

POST /rentals   (same body again)
409 {"error": "R8", "message": "Ananya Nair already has a unit of 'Sony 50mm Lens'."}

POST /rentals
{"customer_id": "C004", "sku": "1000000004"}
409 {"error": "R4", "message": "Rohan Das has unpaid fines of ₹600 (limit ₹500)."}

POST /rentals
{"customer_id": "C003", "sku": "1000000006"}
409 {"error": "R1", "message": "'Vintage Leica (Showcase)' is a display item and cannot be rented."}

POST /rentals
{"customer_id": "C009", "sku": "1000000002"}
404 {"error": "CustomerNotFoundError", "message": "No customer with ID C009."}

POST /rentals
{"customer_id": "C001", "sku": "123"}
422 {"error": "InvalidSKUError", "message": "SKU must be exactly 10 digits."}

POST /rentals/RN001/return
200 {"rental_id": "RN001", "days_late": 5, "fine": 500,
     "next_in_waiting_list": "Meera Joshi"}    (null if nobody is waiting)

GET /customers/C002/rentals
200 {"customer": "Vikram Shah", "membership_type": "Plus",
     "max_items": 4, "unpaid_fines": 0,
     "active": [{"rental_id": "RN001", "item": "DJI Mini Drone",
                 "due_date": "2026-10-29", "days_overdue": 5}]}
```

If the status codes you choose differ from these, explain why in `DECISIONS.md`. The error messages must match.

### 4.1 Catalogue wireframe (draw yours on paper first)

```
+---------------------------------------------------------------------+
| GearShare Mini    Catalogue   My rentals   Basket (2)  [Ananya Nair v] |
+---------------------------------------------------------------------+
| Search [ drone_______ ]   Category [All v]   Sort [Name v]          |
|                                                                     |
| 1 result                                                            |
| +-----------------------------+                                     |
| | DJI Mini Drone              |                                     |
| | video, aerial               |                                     |
| | Drones                      |                                     |
| | 0 of 1 available            |                                     |
| | [Join waiting list]         |                                     |
| +-----------------------------+                                     |
+---------------------------------------------------------------------+
```

### 4.2 Behaviour table: what the screen must do

| Action | Expected result |
|---|---|
| Open `/` | Spinner `Loading catalogue...` then 7 cards |
| Type `drone` | List shows only DJI Mini Drone. Text: `1 result` |
| Type `zzz` | `No items match 'zzz'. Try a different word.` |
| Click the Sony 50mm Lens card | URL becomes `/gear/1000000002`. Shows `1 of 1 available` |
| Open DJI Mini Drone | `0 of 1 available`. Button reads `Join waiting list` |
| Open Vintage Leica (Showcase) | `Display item: view in the shop only`. No rent button |
| Pick Ananya (Basic). Add 2 items, try a 3rd | Message: `Basket full: Basic members can rent 2 items.` 3rd button disabled |
| Click Rent with a valid basket | Button shows `Renting...` then toast: `Rented Sony 50mm Lens. Due 2026-11-06.` |
| Back on the catalogue after renting | Sony 50mm Lens now shows `0 of 1 available` |
| Pick Rohan. Try to rent Manfrotto Tripod | Red message from the server: `Rohan Das has unpaid fines of ₹600 (limit ₹500).` |
| Pick Vikram. Open My rentals | Table row: DJI Mini Drone, due 2026-10-29, `OVERDUE (5 days)` |
| Stop the API server, reload | `Can't reach the rental server.` with a `Retry` button |
| Open `/nothing` | 404 page with a link back to the catalogue |
| Add item: SKU `123` | Under the field: `SKU must be exactly 10 digits.` Submit disabled |
| Add item: all fields valid | Success message, form clears, item appears in the catalogue |
| Resize to 360 px wide | One column of cards, nothing cut off, no sideways scrolling |

Use this table as your own test checklist and tick it off before you hand in.

## Think about this before and while you build

1. The basket limit exists in React *and* in Python. Why is each useful, and which one must never be removed?
2. Two customers rent the last unit at the same moment. What does the second customer see, and is it true?
3. Which component would suffer most from prop drilling if you had no context? What would you change?
4. What does each screen say when the API is down? Would a non-technical customer understand it?

## What to hand in

- `api/` and `web/` folders with a README that explains how to start both
- Component tree diagram and a note on where each piece of state lives
- A 2-minute screen recording or screenshots of all five screens, including loading, empty and error states
- The behaviour table above, ticked off with a note on anything that does not work yet
- `DECISIONS.md`: Tailwind vs MUI, where search state lives, status code choices

## You are done when

- A customer can search, open an item, fill the basket and rent it end to end against the real API and database
- Every screen that fetches data handles loading, empty and error
- An old response never overwrites a newer one
- Everything in the behaviour table works

---

# Submission and Scoring

Submit one repository containing all four phases, with a folder or tag per phase. After the project, expect a short session where you explain parts of your own code and your decisions.

| Phase | Marks | Full marks need |
|---|---|---|
| 1 Python + OOP | 25 | Every sample reproduces; polymorphic design; 20+ meaningful tests; every rule traceable to a test |
| 2 DSA | 20 | Correct structures; measured evidence for every claim; no regressions |
| 3 Database | 25 | Sound normalisation reasoning; all 12 results match; rollback demonstrated; engine works on the database; injection experiment |
| 4 React | 30 | API plus website work end to end; every behaviour-table row passes; states handled; race condition handled; basic accessibility |
| **Total** | **100** | |