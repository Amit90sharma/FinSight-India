
---

# `data_dictionary.md`

```markdown
# Data Dictionary — FinSight India

This document describes the fields contained in the FinSight India banking transaction dataset.

The dataset contains **550,000 transactions** and **20 original columns**.

---

# Dataset Overview

| Attribute | Description |
|---|---|
| Dataset | Indian Banking Transactions |
| Records | 550,000 |
| Columns | 20 |
| Unique Transactions | 550,000 |
| Unique Customers | 79,916 |
| Primary Time Period | 2019–2023 |
| Additional Partial Period | January 1, 2024 |

---

# Transaction Identification

## transaction_id

**Type:** VARCHAR / String

Unique identifier for each banking transaction.

### Example

```text
TXN100001