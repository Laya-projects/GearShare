# 3.1 Anomalies

## Update anomaly

In RN002, RN009, and RN010, Rohan Das has the email rohan@example.com. Changing it to a new email would require changing all three real flat-file rows, so three rows must change. Without separate customer data, the same email update is repeated for every rental.

## Insert anomaly

Pooja Menon has no rental row in the flat file, so there is nowhere to add her as a customer because inserting her requires inventing a rental. The Vintage Leica (Showcase), SKU 1000000006, also has no real rental row, so inserting its item record would likewise require a fictional rental.

## Delete anomaly

RN005 is the only flat-file record for the SD Card 128GB, SKU 1000000007. Deleting RN005 would remove the only representation of that item and the real fine of 600 from the flat file, even though the card can exist independently. That deletion would also lose the rental facts for Ananya Nair.

## 1NF

RN002 stores two tags in one cell: `photo;dslr`. The semicolon-separated value repeats tag values, so it is not atomic.

**BEFORE:** `RN002 | Canon EOS 200D | photo;dslr`

**AFTER:** `RN002 | Canon EOS 200D | photo`; `RN002 | Canon EOS 200D | dslr`. The `tags(tag_id, name)` table stores `photo` and `dslr` once, and `item_tags(item_id, tag_id)` links the Canon to each tag.

RN005 also separates through this rule as `storage`, while RN009 has the two separate tags `audio` and `interview`.

## 2NF

The flat-table key is `rental_id`, so values can be identified by a complete key such as RN002 or RN005. Customer columns (`customer_name`, `email`, `tier`) depend only on the customer, while item columns (`item_name`, `tags`, `sku`, `category`, `parent_category`, `weight_g`, `price`) depend only on the SKU.

Split them into `customers(customer_id, name, email, tier)`, keyed by `customer_id`; `items(sku, item_name, category, weight_g, price)`, keyed by SKU; and `rentals(rental_id, customer_id, sku, issue_date, due_date, return_date)`, keyed by rental ID. For example, RN009's Rohan and microphone details are stored once in the customer and item tables.

## 3NF

In `membership_tiers`, tier is the key and determines `max_items`, `rental_period_days`, and `late_fee_per_day`: `Basic` does not need those policy values repeated for RN002, RN009, and RN010. In `categories`, category determines `parent_category`; `Cameras` and `Lenses` point to the self-referencing `Photography` parent, while RN005's `Accessories` category has no parent.

Fines depend on a rental rather than on every rental detail, so store them separately as one row for RN005 (`600`, `yes`) and RN009 (`450`, `no`). A rental without a fine, such as RN001, has no `fines` row.

## Final tables

- `customers(customer_id, name, email, tier)` - PK: `customer_id`; FK: `tier -> membership_tiers(tier)`.
- `membership_tiers(tier, max_items, rental_period_days, late_fee_per_day)` - PK: `tier`; no foreign keys.
- `items(sku, item_name, category_id, weight_g, price, total_units, item_type)` - PK: `sku`; FK: `category_id -> categories(category_id)`.
- `tags(tag_id, name)` - PK: `tag_id`; UNIQUE: `name`; no foreign keys.
- `item_tags(sku, tag_id)` - PK: `(sku, tag_id)`; FKs: `sku -> items(sku)`, `tag_id -> tags(tag_id)`.
- `categories(category_id, name, parent_category_id)` - PK: `category_id`; FK: `parent_category_id -> categories(category_id)`.
- `rentals(rental_id, customer_id, sku, issue_date, due_date, return_date, extensions)` - PK: `rental_id`; FKs: `customer_id -> customers(customer_id)`, `sku -> items(sku)`.
- `fines(fine_id, rental_id, amount, paid)` - PK: `fine_id`; FK: `rental_id -> rentals(rental_id)`; UNIQUE: `rental_id`.
- `waiting_list(waiting_id, sku, customer_id, joined_at, notified)` - PK: `waiting_id`; FKs: `sku -> items(sku)`, `customer_id -> customers(customer_id)`.
- `audit_log(audit_id, action_time, action, customer_id, sku, rental_id)` - PK: `audit_id`; FKs: `customer_id -> customers(customer_id)`, `sku -> items(sku)`, `rental_id -> rentals(rental_id)`.
