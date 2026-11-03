# ER Relationship Notes

One membership tier has many customers, while each customer belongs to one tier.
A category has many items, while each item belongs to one category.
A category may have one parent category and many child categories.
One customer has many rentals, while each rental belongs to one customer.
One item has many rentals, while each rental concerns one item.
One rental can have zero or one fine, while each fine belongs to one rental.
One item has many item-tag links and one tag has many item-tag links, so items and tags have a many-to-many relationship.
One item has many waiting-list entries and one customer can join many waiting lists.
One customer has many audit-log entries and each audit-log entry belongs to one customer.
One item has many audit-log entries and each audit-log entry belongs to one item.
One rental can have many audit-log entries and each audit-log entry belongs to zero or one rental.
