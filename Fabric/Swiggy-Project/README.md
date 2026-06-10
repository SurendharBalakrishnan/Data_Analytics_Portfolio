# Swiggy Food Analytics — End-to-End Microsoft Fabric Pipeline

An **end-to-end data analytics project** built on Swiggy's food delivery data — covering the full pipeline from raw data ingestion in a **Fabric Lakehouse** through SQL cleaning, **Data Warehouse** star schema modelling, a **Power BI Semantic Model**, and an interactive **Power BI dashboard** analysing ₹53M in sales across 197K orders.

> **Note:** The `.pbix` dashboard file and all raw CSV datasets are excluded from this repository via `.gitignore`. Dashboard PDF export and design images are committed.

---

## Project Objective

To build a complete modern analytics solution on Swiggy's delivery data and answer:

- What is the total sales revenue, average order value, and order volume?
- How do sales trend across months, days of the week, and quarters?
- Which restaurants drive the most revenue?
- How are sales split between Veg and Non-Veg food types?
- Which states and cities generate the highest revenue?
- What is the average customer rating across the platform?

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Sales | ₹53.01M |
| Average Order Value | ₹268.51 |
| Total Orders | 197,430 |
| Average Rating | 4.34 |
| Total Rating Count | 6M |
| Non-Veg Sales Share | 62.26% (₹33.00M) |
| Veg Sales Share | 37.74% (₹20.01M) |

---

## Dashboard Insights

### Top 5 Restaurants by Sales

| Restaurant | Sales |
|------------|-------|
| KFC | ₹4.2M |
| McDonald's | ₹3.3M |
| Pizza Hut | ₹2.1M |
| Burger King | ₹1.9M |
| Domino's Pizza | ₹1.8M |

### Top States by Sales

| State | Sales |
|-------|-------|
| Karnataka | ₹5.5M |
| Uttar Pradesh | ₹3.1M |
| Telangana | ₹3.0M |
| Maharashtra | ₹3.0M |
| Delhi | ₹2.8M |
| Gujarat | ₹2.8M |
| Punjab | ₹2.8M |
| West Bengal | ₹2.7M |
| Tamil Nadu | ₹2.6M |
| Rajasthan | ₹2.5M |

---

## Data Architecture

Six-step end-to-end pipeline built inside a **Microsoft Fabric Workspace**:

| Step | Layer | Technology | Description |
|------|-------|------------|-------------|
| 1 | Workspace | Microsoft Fabric | Created `Swiggy Analytics Project` workspace |
| 2 | Ingestion | Lakehouse | Uploaded raw CSVs into `Files/Raw_Data/` in the Lakehouse |
| 3 | Cleaning | SQL | Removed duplicates, handled nulls, validated referential integrity, standardised formats |
| 4 | Modelling | Data Warehouse | Built star schema — 1 fact table + 4 dimension tables |
| 5 | Semantic Layer | Power BI Semantic Model | Defined table relationships, measures, and KPIs |
| 6 | Reporting | Power BI Report | Built interactive dashboard published inside Fabric workspace |

---

## Data Model

Star schema — 1 fact table + 4 dimension tables.

| Table | Rows | Key Columns |
|-------|------|-------------|
| `fact_orders` | 197,430 | order_id, date_id, location_id, restaurant_id, food_id, price, rating, rating_count |
| `dim_restaurant` | 993 | restaurant_id, restaurant_name |
| `dim_dish` | 82,891 | dish_id, category, dish_name |
| `dim_location` | 995 | location_id, state, city, location |
| `dim_date` | 243 | date_id, order_date |

**Total records: 282,552 rows across all tables**

---

## Technology Stack

| Tool | Role |
|------|------|
| Microsoft Fabric | Unified analytics platform (workspace, Lakehouse, Warehouse) |
| Lakehouse | Raw data storage layer — CSV ingestion |
| SQL | Data cleaning, validation, and transformation queries |
| Data Warehouse | Star schema storage and modelling |
| Dataflow / Data Pipelines | Orchestrated data movement between layers |
| Power BI Semantic Model | Relationships, DAX measures, KPI definitions |
| Power BI Report | Interactive multi-visual dashboard |

---

## File Structure

```
Swiggy-Project/
│
├── Swiggy_Report.pbix              ← Power BI dashboard (excluded)
├── Swiggy_Report.pdf               ← Dashboard PDF export (committed)
├── README.md                       ← Project documentation
├── .gitignore                      ← Excludes .pbix, CSVs, docx
│
├── data/                           ← Raw datasets (excluded)
│   ├── fact_orders.csv             (197,430 rows)
│   ├── dim_restaurant.csv          (993 rows)
│   ├── dim_dish.csv                (82,891 rows)
│   ├── dim_location.csv            (995 rows)
│   └── dim_date.csv                (243 rows)
│
├── documents/                      ← Project documents (excluded)
│   └── Business Requirement.docx   ← BRD — architecture, pipeline steps, KPI definitions
│
└── Images/                         ← Dashboard design assets (committed)
    ├── analytics.png
    ├── checkout.png
    ├── data-governance.png
    ├── database (2).png
    ├── economics.png
    ├── laptop.png
    ├── rating (3).png
    ├── revenue.png
    └── star (1).png
```

---

## Privacy Note

All order, restaurant, and location data is synthetic and used for portfolio and learning purposes. Raw CSV datasets and the Power BI workbook are excluded from version control.
