# Personal Finance & Debt Tracker Dashboard

An interactive Microsoft Excel dashboard that consolidates multiple personal loan and credit obligations into a single unified view — tracking EMI schedules, outstanding balances, repayment progress, and monthly liabilities across lenders.

> **Note:** The `.xlsx` workbook and all CSV source files are excluded from this repository via `.gitignore` to protect sensitive financial data. Only the dashboard PDF export is shared publicly.

---

## Dashboard Preview

📄 [`Personal_Finance_Dashboard.pdf`](./Personal_Finance_Dashboard.pdf)

---

## Project Objective

To build a personal debt management tracker that answers:
- How much total debt is outstanding across all lenders?
- What is the upcoming monthly EMI liability?
- Which loan type contributes the most to total debt?
- What is the paid vs. remaining balance ratio per loan?
- What does the month-by-month repayment schedule look like through 2027?

---

## Workflow

### Step 1 — Data Collection (CSV Uploads)
Individual repayment schedule CSVs were sourced for each loan account:

| Source Sheet | Lender | Loan Category |
|---|---|---|
| `hdfc credit card` | HDFC Bank | Insta Loan (EMI) |
| `idfc credit claude` | IDFC Bank | Credit / Subscription |
| `Saison_Loan_5120` | Ind Money | Insta Cash (App Loan) |
| `Saison_Loan_4096` | Ind Money | Insta Cash (App Loan) |
| `Saisom_Loan_10241` | Ind Money | Insta Cash (App Loan) |
| `Saison_Loan_12290` | Ind Money | Insta Cash (App Loan) |
| `Saison_Loan_6145` | Ind Money | Insta Cash (App Loan) |
| `Bank_Loan` | IOB Bank | Agri Easy Jewel Loan |
| `Bank_Loan (2)` | Kamalam Bankers | Jewel Loan |

Each CSV contained: `Statement Date`, `EMI Amount`, `Principal`, `Interest`, `Balance`, `Due Date`.

---

### Step 2 — Loan Summary Table (`Loan` sheet)
A master loan register was created manually capturing high-level details for all 13 loan accounts:

| Column | Description |
|---|---|
| S No | Serial number |
| Date | Loan start date |
| Company | Lender name |
| Loan Type | Type of loan product |
| Amount Borrowed | Original principal |
| Monthly Instalment | Whether EMI is fixed (Yes/No) |
| Months | Total tenure in months |
| EMI Amount | Fixed monthly instalment |
| Paid Months | Number of months already paid |
| Paid Amount | Total amount repaid so far |
| Balance Months | Remaining months |
| Balance Amount | Outstanding principal balance |
| Interest | Annual interest rate |
| Status | Active / Closed |

---

### Step 3 — Master EMI Schedule (`Master Emi Schedule` sheet)
All individual loan schedules were consolidated into a single flat table with additional classification columns:

| Column | Description |
|---|---|
| Statement Date | Date of statement generation |
| EMI Amount | Monthly instalment amount |
| Principal | Principal component of EMI |
| Interest | Interest component of EMI |
| Balance | Remaining balance after payment |
| Loan Type | Loan product name |
| Due Date | Payment due date |
| Loan Category | `EMI Loan` / `Jewel Loan` / `App Loan` |
| Year | Extracted year of due date |
| Month | Extracted month of due date |

This table spans **76 rows** covering the full repayment timeline from **December 2025 to December 2027**.

---

### Step 4 — Master Data Table (`Master Data` sheet)
An extended version of the Master EMI Schedule, enriched with lender-level details for deeper analysis:

| Additional Columns | Description |
|---|---|
| Company | Lender name (HDFC Bank, IDFC Bank, Ind Money, IOB Bank, Kamalam Bankers) |
| Bank Loan | Loan amount from bank/formal lender category |

This table powers the KPI calculations and pivot aggregations on the dashboard.

---

### Step 5 — Pivot Tables (`Pivot` / `pivot tables` sheets)
Ten pivot tables were built to feed the dashboard visuals:

| Pivot | Purpose |
|---|---|
| Total Outstanding Debt | Sum of balance by loan type |
| Upcoming Monthly Liability | Total EMI due in the current month |
| Debt Concentration | EMI distribution by lender (company-wise) |
| Paid vs. Balance Ratio | Comparison of paid amount vs. outstanding |
| Active Loans Count | Count of active loan accounts |
| Monthly Payment Calendar | Month-by-month EMI breakdown (2025–2027) |
| Total Repayment — Credit Card & App | Repayment summary for HDFC & IDFC |
| Total Repayment — Banks & Jewel Loan | Repayment summary for bank and jewel loans |
| Year-wise EMI Trend | Annual EMI aggregation (2025 / 2026 / 2027) |
| Lender-wise Liability | EMI breakdown by company |

Slicers applied: **Year**, **Month**, **Loan Type**, **Due Date**

---

### Step 6 — Dashboard (`Dashboard` sheet)
The final single-page interactive dashboard consolidates all KPIs and charts with slicers for filtering.

#### KPI Cards
| KPI | Description |
|---|---|
| Total Outstanding Debt | Total remaining balance across all loans |
| Upcoming Monthly Liability | Total EMI due in the upcoming month |
| Debt Concentration | Highest contributing loan category |
| Paid vs. Balance Ratio | Proportion of total loan already repaid |
| Active Loans Count | Number of currently active loan accounts |

#### Visualizations
- **Monthly Payment Calendar** — Bar/column chart showing monthly EMI outflow from Dec 2025 to Dec 2027
- **Debt Concentration** — Chart showing EMI split across loan types (Jewel Loan, Insta Cash, Insta Loan, IDFC Subscriptions)
- **Paid vs. Balance Ratio** — Stacked or pie chart comparing total paid amount vs. outstanding balance
- **Lender-wise Liability** — Breakdown of EMI obligation by lender (IOB Bank, Kamalam Bankers, Ind Money, HDFC Bank, IDFC Bank)
- **Year-wise EMI Trend** — Trend line across 2025, 2026, 2027

---

## Tools & Techniques Used

| Tool / Feature | Usage |
|---|---|
| Microsoft Excel | Primary tool |
| Power Query | CSV import and data loading |
| Excel Tables | Structured references for each loan sheet |
| Pivot Tables | 10 pivot tables for aggregation and KPIs |
| Pivot Charts | 6 interactive charts linked to pivot data |
| Slicers | Year, Month, Loan Type, Due Date filters |
| Conditional Formatting | Status indicators (Active / Closed) |
| Data Validation | Dropdown lists for loan categories |
| Named Ranges | Used in KPI formula references |

---

## File Structure

```
personal_finance_excel_dashbaord/
│
├── Personal_Finance_Dashboard.pdf   ← Dashboard export (publicly shared)
├── README.md                        ← Project documentation
└── .gitignore                       ← Excludes .xlsx and .csv files
```

## Key Insights from the Dashboard

- **Multiple loan types tracked:** Jewel loans (interest-only), App-based Insta Cash loans (short-tenure), and EMI-based bank loans
- **Repayment timeline:** Full debt clearance projected by **December 2027**
- **Highest EMI contributor:** Sim Soft Info Systems (IDFC Bank) — 24-month EMI loan
- **Short-tenure high-interest loans:** Ind Money Insta Cash loans carry ~22% annual interest over 6-month tenures
- **Jewel loans:** IOB Bank and Kamalam Bankers jewel loans are interest-servicing only (no fixed EMI schedule)
- **Dashboard is slicer-enabled:** Can filter by year, month, and loan type for focused analysis

---

## Privacy Note

All account numbers, exact loan amounts, and personal identifiers have been removed from this documentation. The `.xlsx` workbook is not uploaded to this repository. Only the PDF export of the dashboard visuals is shared publicly.
