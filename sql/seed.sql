INSERT INTO membership_tiers (tier, max_items, rental_period_days, late_fee_per_day) VALUES
    ('Basic', 2, 3, 50),
    ('Plus', 4, 5, 100),
    ('Pro', 8, 7, 150);

INSERT INTO categories (category_id, name, parent_id) VALUES
    (8, 'Photography', NULL),
    (1, 'Cameras', 8),
    (2, 'Lenses', 8),
    (3, 'Drones', NULL),
    (4, 'Tripods', NULL),
    (5, 'Audio', NULL),
    (6, 'Showcase', NULL),
    (7, 'Accessories', NULL);

INSERT INTO items (sku, name, item_type, weight_g, price, total_units, category_id) VALUES
    ('1000000001', 'Canon EOS 200D', 'Equipment', 450, 45000, 2, 1),
    ('1000000002', 'Sony 50mm Lens', 'Equipment', 280, 18000, 1, 2),
    ('1000000003', 'DJI Mini Drone', 'Equipment', 249, 38000, 1, 3),
    ('1000000004', 'Manfrotto Tripod', 'Equipment', 1200, 6000, 2, 4),
    ('1000000005', 'Rode Wireless Mic', 'Equipment', 120, 22000, 1, 5),
    ('1000000006', 'Vintage Leica (Showcase)', 'Display', 600, 150000, 1, 6),
    ('1000000007', 'SD Card 128GB', 'Accessory', 2, 600, 3, 7);

INSERT INTO tags (tag_id, name) VALUES
    (1, 'photo'),
    (2, 'dslr'),
    (3, 'lens'),
    (4, 'video'),
    (5, 'aerial'),
    (6, 'support'),
    (7, 'audio'),
    (8, 'interview'),
    (9, 'display'),
    (10, 'storage');

INSERT INTO item_tags (sku, tag_id) VALUES
    ('1000000001', 1),
    ('1000000001', 2),
    ('1000000002', 1),
    ('1000000002', 3),
    ('1000000003', 4),
    ('1000000003', 5),
    ('1000000004', 6),
    ('1000000005', 7),
    ('1000000005', 8),
    ('1000000006', 9),
    ('1000000007', 10);

INSERT INTO customers (customer_id, name, email, tier) VALUES
    ('C001', 'Ananya Nair', 'ananya@example.com', 'Basic'),
    ('C002', 'Vikram Shah', 'vikram@example.com', 'Plus'),
    ('C003', 'Meera Joshi', 'meera@example.com', 'Pro'),
    ('C004', 'Rohan Das', 'rohan@example.com', 'Basic'),
    ('C005', 'Pooja Menon', 'pooja@example.com', 'Plus');

INSERT INTO rentals (rental_id, customer_id, sku, issue_date, due_date, return_date, extensions) VALUES
    ('RN001', 'C002', '1000000003', '2026-10-24', '2026-10-29', NULL, 0),
    ('RN002', 'C004', '1000000001', '2026-10-28', '2026-10-31', NULL, 0),
    ('RN003', 'C003', '1000000004', '2026-10-30', '2026-11-06', NULL, 0),
    ('RN004', 'C001', '1000000002', '2026-09-10', '2026-09-13', '2026-09-13', 0),
    ('RN005', 'C001', '1000000007', '2026-08-01', '2026-08-03', '2026-08-23', 0),
    ('RN006', 'C003', '1000000003', '2026-08-05', '2026-08-12', '2026-08-10', 0),
    ('RN007', 'C002', '1000000001', '2026-07-10', '2026-07-15', '2026-07-15', 0),
    ('RN008', 'C002', '1000000005', '2026-06-01', '2026-06-06', '2026-06-09', 0),
    ('RN009', 'C004', '1000000005', '2026-07-01', '2026-07-04', '2026-07-13', 0),
    ('RN010', 'C004', '1000000001', '2026-07-20', '2026-07-23', '2026-07-26', 0);

INSERT INTO fines (fine_id, rental_id, amount, paid) VALUES
    (1, 'RN005', 600, 1),
    (2, 'RN008', 300, 1),
    (3, 'RN009', 450, 0),
    (4, 'RN010', 150, 0);
