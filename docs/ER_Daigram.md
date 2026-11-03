erDiagram
    MEMBERSHIP_TIERS ||--o{ CUSTOMERS : has
    CATEGORIES ||--o{ ITEMS : contains
    CATEGORIES ||--o{ CATEGORIES : parent_of
    CUSTOMERS ||--o{ RENTALS : makes
    ITEMS ||--o{ RENTALS : rented_as
    RENTALS ||--o| FINES : incurs
    ITEMS ||--o{ ITEM_TAGS : has
    TAGS ||--o{ ITEM_TAGS : labels
    ITEMS ||--o{ WAITING_LIST : queues
    CUSTOMERS ||--o{ WAITING_LIST : joins
    CUSTOMERS ||--o{ AUDIT_LOG : performs
    ITEMS ||--o{ AUDIT_LOG : records
    RENTALS ||--o{ AUDIT_LOG : references

    MEMBERSHIP_TIERS {
        string tier PK
        integer max_items
        integer rental_period_days
        integer late_fee_per_day
    }
    CATEGORIES {
        integer category_id PK
        string name
        integer parent_id FK
    }
    CUSTOMERS {
        string customer_id PK
        string name
        string email
        string tier FK
    }
    ITEMS {
        string sku PK
        string name
        string item_type
        integer weight_g
        integer price
        integer total_units
        integer category_id FK
    }
    TAGS {
        integer tag_id PK
        string name
    }
    ITEM_TAGS {
        string sku PK,FK
        integer tag_id PK,FK
    }
    RENTALS {
        string rental_id PK
        string customer_id FK
        string sku FK
        string issue_date
        string due_date
        string return_date
        integer extensions
    }
    FINES {
        integer fine_id PK
        string rental_id FK
        integer amount
        integer paid
    }
    WAITING_LIST {
        integer waiting_id PK
        string sku FK
        string customer_id FK
        string joined_at
        integer notified
    }
    AUDIT_LOG {
        integer audit_id PK
        string action
        string customer_id FK
        string sku FK
        string created_on
        string rental_id FK
    }