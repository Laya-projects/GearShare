-- Q1: Items tagged 'photo', with all their tags
-- Join type: INNER
-- INNER joins every item-tag link to its item and tag, while EXISTS supplies only photo items. An outer join would introduce non-photo items or unmatched tags and is therefore inappropriate.
SELECT DISTINCT i.name, all_tags.name AS tag
FROM items AS i
JOIN item_tags AS photo_link ON photo_link.sku = i.sku
JOIN tags AS photo_tag ON photo_tag.tag_id = photo_link.tag_id
JOIN item_tags AS all_link ON all_link.sku = i.sku
JOIN tags AS all_tags ON all_tags.tag_id = all_link.tag_id
WHERE photo_tag.name = 'photo'
ORDER BY i.name, all_tags.name;

-- Q2: Items currently on rental, and who has them
-- Join type: INNER
-- INNER joins are required because both an active customer and an item must exist for each reported rental; unmatched rows should not appear.
SELECT r.rental_id,
       c.name AS customer,
       i.name AS item
FROM rentals AS r
JOIN customers AS c ON c.customer_id = r.customer_id
JOIN items AS i ON i.sku = r.sku
WHERE r.return_date IS NULL
ORDER BY r.rental_id;

-- Q3: Overdue rentals with days overdue
-- Join type: INNER
-- INNER joins provide each overdue rental with its customer and item. Rentals without both linked records cannot be valid rental-history rows and must not be reported.
SELECT c.name AS customer,
       i.name AS item,
       r.due_date,
       CAST(julianday('2026-11-03') - julianday(r.due_date) AS INTEGER) AS days_overdue
FROM rentals AS r
JOIN customers AS c ON c.customer_id = r.customer_id
JOIN items AS i ON i.sku = r.sku
WHERE r.return_date IS NULL
  AND r.due_date < '2026-11-03'
ORDER BY days_overdue DESC, c.name;

-- Q4: Top 3 items by number of rentals
-- Join type: INNER
-- An INNER join counts only items that actually occur in rental rows, which is exactly the population being ranked; a LEFT join would add a constant rental count for unrelated items.
SELECT i.name AS item,
       COUNT(*) AS rentals
FROM rentals AS r
JOIN items AS i ON i.sku = r.sku
GROUP BY i.sku, i.name
ORDER BY rentals DESC, i.name ASC
LIMIT 3;

-- Q5: Items that have never been rented
-- Join type: LEFT
-- A LEFT join preserves every item and identifies rental matches that are absent; an INNER join cannot return items with zero rentals.
SELECT i.name
FROM items AS i
LEFT JOIN rentals AS r ON r.sku = i.sku
WHERE r.rental_id IS NULL
ORDER BY i.name;

-- Q6: Customers with no rental since 2026-08-05
-- Join type: LEFT
-- A LEFT join preserves customers even when no recent rental matches, and the NULL match test selects exactly those customers. A NOT EXISTS alternative could express the same rule.
SELECT c.name
FROM customers AS c
LEFT JOIN rentals AS r
  ON r.customer_id = c.customer_id
 AND r.issue_date >= '2026-08-05'
WHERE r.rental_id IS NULL
ORDER BY c.name;

-- Q7: Total fines per tier per month
-- Join type: INNER
-- INNER joins are necessary to obtain a fine, its rental, its customer tier, and the item's return month as one complete fact row.
SELECT mt.tier,
       substr(r.return_date, 1, 7) AS month,
       SUM(f.amount) AS total_fines
FROM fines AS f
JOIN rentals AS r ON r.rental_id = f.rental_id
JOIN customers AS c ON c.customer_id = r.customer_id
JOIN membership_tiers AS mt ON mt.tier = c.tier
WHERE r.return_date IS NOT NULL
GROUP BY mt.tier, substr(r.return_date, 1, 7)
ORDER BY mt.tier, month;

-- Q8: Fines paid vs pending
-- Join type: none
-- No join is needed because the status and total can be aggregated directly from fines.
SELECT CASE WHEN paid = 1 THEN 'Paid' ELSE 'Pending' END AS status,
       SUM(amount) AS total
FROM fines
GROUP BY paid
ORDER BY CASE WHEN paid = 1 THEN 0 ELSE 1 END;

-- Q9: Customers who rented from at least 3 different categories
-- Join type: INNER
-- INNER joins through rentals, items, and categories restrict the result to real category-rental facts and exclude customers with no such history.
SELECT c.name,
       COUNT(DISTINCT i.category_id) AS categories
FROM rentals AS r
JOIN customers AS c ON c.customer_id = r.customer_id
JOIN items AS i ON i.sku = r.sku
GROUP BY c.customer_id, c.name
HAVING COUNT(DISTINCT i.category_id) >= 3
ORDER BY c.name;

-- Q10: Categories where the average completed rental lasts more than 4 days
-- Join type: INNER
-- INNER joins are needed so each completed rental contributes item-category and duration data; rentals without both linked records are excluded.
SELECT cat.name AS category,
       ROUND(AVG(julianday(r.return_date) - julianday(r.issue_date)), 1) AS avg_days
FROM rentals AS r
JOIN items AS i ON i.sku = r.sku
JOIN categories AS cat ON cat.category_id = i.category_id
WHERE r.return_date IS NOT NULL
GROUP BY cat.category_id, cat.name
HAVING AVG(julianday(r.return_date) - julianday(r.issue_date)) > 4
ORDER BY cat.name;

-- Q11: Units available right now, per item
-- Join type: LEFT
-- A LEFT join preserves every item, including items with no open rental; COUNT/rental multiplication then gives the availability against total_units.
SELECT i.name,
       CASE
           WHEN i.item_type = 'Display' THEN i.total_units
           ELSE i.total_units - COUNT(CASE WHEN r.return_date IS NULL THEN 1 END)
       END AS available
FROM items AS i
LEFT JOIN rentals AS r ON r.sku = i.sku
GROUP BY i.sku, i.name, i.item_type, i.total_units
ORDER BY i.sku;

-- Q12: The pair of items most often rented by the same customer
-- Join type: self-join
-- This is a self-join on rentals to connect two different rental rows belonging to the same customer. Items are ordered by name and joined in only once.
SELECT a.name AS item_a,
       b.name AS item_b,
       COUNT(DISTINCT r1.customer_id) AS customers
FROM rentals AS r1
JOIN rentals AS r2
  ON r2.customer_id = r1.customer_id
 AND r1.sku < r2.sku
JOIN items AS a ON a.sku = r1.sku
JOIN items AS b ON b.sku = r2.sku
GROUP BY r1.sku, r2.sku, a.name, b.name
HAVING a.name < b.name
ORDER BY customers DESC, a.name, b.name
LIMIT 1;
