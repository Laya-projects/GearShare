PRAGMA foreign_keys = ON;

CREATE TABLE membership_tiers (
    tier TEXT PRIMARY KEY,
    max_items INTEGER NOT NULL CHECK (max_items >= 0),
    rental_period_days INTEGER NOT NULL CHECK (rental_period_days > 0),
    late_fee_per_day INTEGER NOT NULL CHECK (late_fee_per_day >= 0)
);

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    -- A child category may temporarily have no parent.
    parent_id INTEGER REFERENCES categories(category_id) ON DELETE SET NULL
);

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    -- Deleting a tier must not leave customers without a membership policy.
    tier TEXT NOT NULL REFERENCES membership_tiers(tier) ON DELETE RESTRICT
);

CREATE TABLE items (
    sku TEXT PRIMARY KEY CHECK (length(sku) = 10 AND sku NOT GLOB '*[^0-9]*'),
    name TEXT NOT NULL,
    item_type TEXT NOT NULL,
    weight_g INTEGER NOT NULL CHECK (weight_g >= 0),
    price INTEGER NOT NULL CHECK (price >= 0),
    total_units INTEGER NOT NULL CHECK (total_units >= 0),
    -- Keep the category until all items in it are reassigned.
    category_id INTEGER NOT NULL REFERENCES categories(category_id) ON DELETE RESTRICT
);

CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE item_tags (
    sku TEXT NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (sku, tag_id),
    -- Removing a tag link when its item is deleted keeps no orphaned links.
    FOREIGN KEY (sku) REFERENCES items(sku) ON DELETE CASCADE,
    -- Removing an item-tag link when a tag is deleted does not delete the item.
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
);

CREATE TABLE rentals (
    rental_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    sku TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    extensions INTEGER NOT NULL DEFAULT 0 CHECK (extensions >= 0),
    CHECK (due_date >= issue_date),
    -- Rental history must survive; remove customers only after rentals are handled.
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    -- Rental history must survive; item removal is blocked while rentals exist.
    FOREIGN KEY (sku) REFERENCES items(sku) ON DELETE RESTRICT
);

CREATE TABLE fines (
    fine_id INTEGER PRIMARY KEY,
    rental_id TEXT NOT NULL UNIQUE,
    amount INTEGER NOT NULL CHECK (amount >= 0),
    paid INTEGER NOT NULL CHECK (paid IN (0, 1)),
    -- Keep a fine's rental identity rather than losing financial history.
    FOREIGN KEY (rental_id) REFERENCES rentals(rental_id) ON DELETE RESTRICT
);

CREATE TABLE waiting_list (
    waiting_id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    joined_at TEXT NOT NULL,
    notified INTEGER NOT NULL DEFAULT 0 CHECK (notified IN (0, 1)),
    -- Waiting requests are transient and should disappear with their item.
    FOREIGN KEY (sku) REFERENCES items(sku) ON DELETE CASCADE,
    -- Waiting requests are transient and should disappear with their customer.
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE audit_log (
    audit_id INTEGER PRIMARY KEY,
    action TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    sku TEXT NOT NULL,
    created_on TEXT NOT NULL,
    rental_id TEXT,
    -- Audit history is retained; deleting customers is blocked while audited.
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    -- Audit history is retained; deleting items is blocked while audited.
    FOREIGN KEY (sku) REFERENCES items(sku) ON DELETE RESTRICT,
    -- Audit history is retained; deleting rentals is blocked while audited.
    FOREIGN KEY (rental_id) REFERENCES rentals(rental_id) ON DELETE RESTRICT
);
