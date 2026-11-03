-- before: demonstrate that neither the rental nor audit history exists yet
SELECT COUNT(*) FROM rentals WHERE rental_id = 'RN011';
SELECT COUNT(*) FROM audit_log;

-- attempt 1: prove that an invalid audit row rolls back both inserts
BEGIN;
INSERT INTO rentals (rental_id, customer_id, sku, issue_date, due_date, return_date, extensions)
VALUES ('RN011', 'C001', '1000000002', '2026-11-03', '2026-11-06', NULL, 0);
INSERT INTO audit_log (action, customer_id, sku, created_on, rental_id)
VALUES (NULL, 'C001', '1000000002', '2026-11-03', 'RN011');
ROLLBACK;

SELECT COUNT(*) FROM rentals WHERE rental_id = 'RN011';
SELECT COUNT(*) FROM audit_log;

-- attempt 2: prove that a valid audit row commits the rental and audit atomically
BEGIN;
INSERT INTO rentals (rental_id, customer_id, sku, issue_date, due_date, return_date, extensions)
VALUES ('RN011', 'C001', '1000000002', '2026-11-03', '2026-11-06', NULL, 0);
INSERT INTO audit_log (action, customer_id, sku, created_on, rental_id)
VALUES ('RENT', 'C001', '1000000002', '2026-11-03', 'RN011');
COMMIT;

SELECT COUNT(*) FROM rentals WHERE rental_id = 'RN011';
SELECT COUNT(*) FROM audit_log;
