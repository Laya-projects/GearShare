# 3.1 Anomalies

## Update anomaly

In RN002, RN009, and RN010, Rohan Das has the email rohan@example.com. Changing it to a new email would require changing all three real flat-file rows, so three rows must change. Without separate customer data, the same email update is repeated for every rental.

## Insert anomaly

Pooja Menon has no rental row in the flat file, so there is nowhere to add her as a customer because inserting her requires inventing a rental. The Vintage Leica (Showcase), SKU 1000000006, also has no real rental row, so inserting its item record would likewise require a fictional rental.

## Delete anomaly

RN005 is the only flat-file record for the SD Card 128GB, SKU 1000000007. Deleting RN005 would remove the only representation of that item and the real fine of 600 from the flat file, even though the card can exist independently. That deletion would also lose the rental facts for Ananya Nair.

## 1NF

## 2NF

## 3NF
