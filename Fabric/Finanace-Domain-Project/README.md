# Finance Analytics — Microsoft Fabric + Dataflow Gen2 + Warehouse + SQL

An **end-to-end finance analytics project** built using Microsoft Fabric — covering data ingestion, cleaning via Dataflow Gen2, Data Warehouse modelling, and SQL-based KPI reporting across 50,000 financial transactions to analyse fraud, revenue, customer behaviour, and business performance.

> **Note:** Raw datasets (`.csv`) and source documents (`.docx`, `.pptx`) are excluded from this repository via `.gitignore`. Warehouse DDL scripts, semantic model definition, and SQL queries are committed.

---

## Business Context

A financial services company faces challenges in analysing customer transactions, detecting fraud, monitoring success rates, and understanding customer behaviour across regions and demographics. Data arrives from multiple sources with inconsistencies, missing values, and duplicate records.

The goal is to build a modern end-to-end analytics solution using Microsoft Fabric to streamline ingestion, transformation, warehousing, and reporting.

---

## Project Objective

To design and implement a scalable Finance Analytics Solution that answers:

- What is the total transaction volume, revenue, fees, and tax collected?
- What percentage of transactions are successful vs. fraudulent?
- How does transaction amount vary by month, type, and channel?
- Which states, cities, and customer segments generate the most revenue?
- How are customers distributed by occupation, age group, and segment?
- Which customers and transactions have the highest values?

---

## Data Architecture

Five-step pipeline built inside a **Microsoft Fabric Workspace**:

| Step | Layer | Technology | Description |
|------|-------|------------|-------------|
| 1 | Workspace | Microsoft Fabric | Created Finance Analytics workspace |
| 2 | Ingestion | Lakehouse | Uploaded raw CSVs (`customers.csv`, `finance_transactions.csv`) |
| 3 | Cleaning | Dataflow Gen2 | Removed duplicates, handled nulls, corrected date formats, validated amounts |
| 4 | Modelling | Data Warehouse | Created `customers` and `finance_transactions` tables via SQL DDL |
| 5 | Reporting | SQL + Power BI | 27 KPI queries executed; Semantic Model built in DirectLake mode |

---

## Data Model

| Table | Rows | Key Columns |
|-------|------|-------------|
| `customers` | 5,000 | customer_id, customer_name, gender, date_of_birth, city, state, occupation, customer_segment, annual_income, join_date, age |
| `finance_transactions` | 50,069 | transaction_id, transaction_date, account_id, customer_id, transaction_type, channel, merchant_category, amount, fee_amount, tax_amount, currency, transaction_status, is_fraud, risk_score, reference_no |

**Total records: 55,069 rows**

---

## SQL KPI Queries (27 Queries)

### KPI Summary (Queries 1–12)

| # | KPI | Description |
|---|-----|-------------|
| 1 | Total Transactions | Count of all transactions processed |
| 2 | Total Customers | Count of all customers |
| 3 | Avg Customer Age | Average age across all customers |
| 4 | Total Transaction Amount | Sum of all transaction amounts |
| 5 | Total Fees Collected | Sum of all fee amounts |
| 6 | Total Tax Amount | Sum of all tax amounts |
| 7 | Avg Transaction Amount | Average value per transaction |
| 8 | Avg Annual Income | Average annual income of customers |
| 9 | Successful Transactions | Count of `transaction_status = 'Success'` |
| 10 | Fraud Amount | Count of `is_fraud = 'Yes'` transactions |
| 11 | Success Rate % | Successful / Total × 100 |
| 12 | Fraud Rate % | Fraudulent / Total × 100 |

### Granular Insights (Queries 13–27)

| # | KPI | Description |
|---|-----|-------------|
| 13 | Monthly Transaction Amount | Total amount, fees, tax grouped by year and month |
| 14 | Transaction Type Analysis | Count and amount by transaction type |
| 15 | Transaction Status Distribution | Count and amount by status (Success / Failed / Pending) |
| 16 | Customers by State | Customer count per state |
| 17 | Customers by Occupation | Customer count per occupation |
| 18 | Customer Segment Distribution | Customer count per segment |
| 19 | Age Group Analysis | Customers grouped: Below 25 / 25–40 / 41–60 / 60+ |
| 20 | Top 10 Highest Transactions | Top 10 by amount |
| 21 | Top 10 Customers by Transaction Amount | Customer name + state + amount (JOIN) |
| 22 | Monthly Revenue by Segment | Amount + fees + tax by month and customer segment |
| 23 | Transaction Amount by Gender | Total amount split by gender |
| 24 | Revenue by Customer Segment | Revenue (amount + fees + tax) per segment |
| 25 | Top States by Transaction Amount | Top 10 states by total transaction amount |
| 26 | Top 10 Cities by Revenue | Top 10 cities by total revenue |
| 27 | Age Group Wise Revenue | Revenue contribution by age group |

---

## Technology Stack

| Tool | Role |
|------|------|
| Microsoft Fabric | Unified analytics platform — workspace, Lakehouse, Warehouse |
| Dataflow Gen2 | ETL/ELT — data cleaning and transformation |
| Fabric Data Warehouse | SQL-based storage and modelling (T-SQL) |
| SQL (T-SQL) | DDL schema creation + 27 KPI analytical queries |
| Power BI Semantic Model | DirectLake connection to Warehouse — relationships and measures |
| Power BI Report | Interactive dashboard for business stakeholders |

---

## File Structure

```
Finanace-Domain-Project/
│
├── README.md                          ← Project documentation
├── .gitignore                         ← Excludes Source CSVs, docx, pptx
├── finance_queries.docx               ← All 27 SQL KPI queries
│
├── finance_wh/                        ← Fabric Data Warehouse SQL project
│   ├── finance_wh.sqlproj             ← SQL project file (Microsoft.Build.Sql)
│   ├── xmla.json                      ← Power BI Semantic Model (DirectLake)
│   └── dbo/
│       └── Tables/
│           ├── customers.sql          ← CREATE TABLE DDL for customers
│           └── finance_transactions.sql ← CREATE TABLE DDL for transactions
│
└── Source/                            ← Raw data and source documents (excluded)
    ├── customers (1).csv              (5,000 rows)
    ├── finance_transactions.csv       (50,069 rows)
    ├── Finance Analytics Project - Problem Statement.docx
    ├── Project Doc.docx
    └── Project Flow.pptx
```

---

## Privacy Note

All customer and transaction data is synthetic and used for portfolio and learning purposes. Raw CSV datasets are excluded from version control via `.gitignore`.
