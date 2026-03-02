# Email Marketing Customer Analysis Dashboard

A **Power BI dashboard** built on a 10,000-record Indian customer database to support targeted email marketing campaigns — segmenting customers by demographics, geography, family composition, and account status.

> **Live Dashboard:** [View on Power BI](https://app.powerbi.com/view?r=eyJrIjoiOTJkYWI0OGYtNzRmYS00OTQ2LTkxNjAtOTgwOGM2OGIyYWRiIiwidCI6ImFiZWU3YjhjLTQ1MWQtNDNlMy05MmI0LTMwNjE0OWI1YjVkYyJ9)

> **Note:** The `.pbix` dashboard file and all data files (`.xlsx`, `.csv`) are excluded from this repository via `.gitignore` to protect customer data privacy.

---

## Project Objective

To analyse a customer email list and answer:

- What is the active vs. inactive distribution of the customer base?
- How are customers distributed across states and cities in India?
- What is the gender and marital status breakdown of the mailing list?
- How do family living arrangements (couple with children, single, etc.) vary across the segment?
- Which customer types (Individual vs. Business) dominate the list?
- How can customers be segmented for more targeted email campaigns?

---

## Dataset Overview

**Source File:** `output/Email Marketing Analysis.xlsx`
**Sheet:** `TBL_CustomerProfileData`
**Total Records:** 10,000 customer profiles

| Column | Description |
|--------|-------------|
| Customer ID | Unique UUID identifier per customer |
| Type | Customer type — `Individual` or `Business` |
| Status | Account status — `Active` / `InActive` |
| City | City of residence |
| State | State / Province |
| PostalCode | Postal / PIN code |
| GenderCode | Gender — `MALE`, `FEMALE`, `OTHER`, `U` (Unspecified) |
| BirthDate | Date of birth (Excel serial format) |
| MaritalStatus | Marital status — `M` (Married), `U` (Unmarried), or text values |
| Enrolled on | Enrollment / registration date (Excel serial format) |
| Living status | Household composition — `couple with children`, `couple without children`, `single/living alone` |

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Customer Records | 10,000 |
| Active Customers | 9,900 (99%) |
| Inactive Customers | 100 (1%) |
| Individual Customers | 9,736 (97.4%) |
| Business Customers | 264 (2.6%) |
| Male | 6,814 (68.1%) |
| Female | 2,907 (29.1%) |
| Married Customers | 9,676 (96.8%) |
| Couple with Children | 4,785 (47.9%) |
| Couple without Children | 3,497 (35.0%) |
| Single / Living Alone | 1,645 (16.5%) |
| Geographic Coverage | 37 States, 452 Cities, 1,361 Postal Codes |

---

## Geographic Distribution

### Top States by Customer Count

| State | Customers |
|-------|-----------|
| Telangana | 4,304 (43.0%) |
| Maharashtra | 2,236 (22.4%) |
| Andhra Pradesh | 2,123 (21.2%) |
| Karnataka | 391 (3.9%) |
| Delhi | 150 (1.5%) |
| Tamil Nadu | 124 (1.2%) |

### Top Cities by Customer Count

| City | Customers |
|------|-----------|
| Hyderabad | 2,639 |
| Secunderabad | 2,093 |
| Mumbai | 1,498 |
| Hyderabad City | 976 |
| Thane | 227 |
| Bengaluru | 200 |

> The customer base is heavily concentrated in South India — Telangana, Maharashtra, and Andhra Pradesh together account for ~86% of all customers.

---

## Dashboard

**Tool:** Power BI Desktop (November 2025 release)
**File:** `output/Email Marketing Analysis.pbix`

**Dashboard Page:**

| Visual | Description |
|--------|-------------|
| Gender Distribution | Donut chart showing Male / Female / Other / Unspecified breakdown |
| Customer Type | Individual vs. Business split |
| Account Status | Active vs. Inactive customer count |
| Geographic Map | Customer density by state and city |
| Living Status | Household composition breakdown |
| Marital Status | Married vs. unmarried segmentation |

---

## Data Quality Notes

- **73 records** have data entry issues — `MALE` appears in the State field (likely import error)
- **Marital status** uses mixed coding: `M`/`U` codes alongside full text values (`couple with children`, etc.)
- **73 records** have empty Living status values
- **Dates** stored as Excel serial numbers — converted in Power Query during model load
- **City naming inconsistencies:** `Hyderabad` and `Hyderabad City` treated as separate entries

---

## Technology Stack

| Tool | Role |
|------|------|
| Power BI Desktop | Dashboard development and visualizations |
| Power Query (M) | Data type conversion, date parsing, null handling |
| DAX | Calculated measures for KPI cards and segment counts |
| Excel | Source data storage (`TBL_CustomerProfileData`) |

---

## File Structure

```
Email_Marketing/
│
├── README.md                                  ← Project documentation
├── .gitignore                                 ← Excludes .pbix, .xlsx, .csv
│
└── output/
    ├── Email Marketing Analysis.pbix          ← Power BI dashboard (excluded)
    └── Email Marketing Analysis.xlsx          ← Customer dataset — 10,000 records (excluded)
```

---

## Privacy Note

This dataset contains customer-level personal information including UUID identifiers, geographic data, date of birth, gender, and marital status. All data files are excluded from version control via `.gitignore`. No raw customer data is committed to this repository.
