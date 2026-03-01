# QuickBite Express — Crisis Recovery Analytics

A full end-to-end **data analytics project** for a food delivery startup that suffered a viral food safety incident followed by a platform outage — covering a complete Python data pipeline (cleaning → EDA → deep analysis) and a 6-page **Power BI dashboard** built on 837,000+ order records spanning 9 months.

> **Note:** The `.pbix` dashboard, all CSV datasets, and generated output files are excluded from this repository via `.gitignore`. Jupyter notebooks and design assets are committed.

---

## Project Objective

To analyse the full business impact of QuickBite Express's crisis period (June–September 2025) and answer:

- How severely did monthly orders and revenue decline after the crisis?
- Which cities were hit hardest and by how much?
- How did cancellation rates and SLA breach rates change during the crisis?
- What happened to customer ratings and review sentiment?
- How many loyal and high-value customers churned?
- What is the total estimated financial loss over the 4-month crisis period?
- What recovery strategies does the data recommend?

---

## Crisis Context

| Event | Date | Impact |
|-------|------|--------|
| Viral food quality incident | May 2025 | Negative social media coverage, customer trust erosion |
| Platform outage | June 2025 | Service disruption across all cities |
| Crisis period | Jun–Sep 2025 | 4-month sustained decline in orders, revenue, and ratings |

---

## Key Findings

| Metric | Pre-Crisis (Jan–May) | Crisis (Jun–Sep) | Change |
|--------|----------------------|------------------|--------|
| Monthly Orders | 22,761 | 8,840 | **-61.2%** |
| Monthly Revenue | ₹7.52M | ₹2.74M | **-63.7%** |
| Cancellation Rate | 6.1% | 11.9% | **+95%** |
| Avg Delivery Time | 39.5 min | 60.1 min | **+52%** |
| SLA Breach Rate | 56% | 88% | **+32 pp** |
| Avg Rating | 4.5 ★ | 2.5 ★ | **-2 stars** |
| Sentiment Score | +0.75 | -0.25 | **-1.0** |
| Loyal Customer Churn | — | 84.5% churned | **49 of 58 lost** |
| High-Value Customer Churn | — | 84% churned | **3,648 of 4,342 lost** |
| **Estimated 4-Month Revenue Loss** | | | **₹19.16 Crore** |

---

## Data Pipeline

### Step 1 — Data Quality Report (`01_data_quality_report.ipynb`)
Validates all 8 source tables against schema expectations:
- Null analysis, duplicate detection, data type checks, foreign key validation
- **Initial quality score: 93.3%** (3.78% null delivery partners, 21,355 orphan keys, 16 duplicate ratings)

### Step 2 — Data Cleaning (`02_data_cleaning.ipynb`)
Resolves all identified issues:
- Null `delivery_partner_id` → filled with `UNKNOWN` placeholder
- Orphan keys → resolved via placeholder dimension records
- Duplicate ratings → deduplicated (16 records)
- Added `phase` column: `Pre-Crisis` (Jan–May) / `Crisis` (Jun–Sep)
- **Final quality score: 99.94%**
- Output: 8 cleaned CSVs in `output/02_cleaned_data/`

### Step 3 — Primary EDA (`03_eda_primary_analysis.ipynb`)
Answers Q1–3 and Q8:

| Question | Finding |
|----------|---------|
| Q1 — Monthly order trend | Orders peaked Jan–May, collapsed from June |
| Q2 — City-level decline | Chennai -62%, Kolkata -61%, Bengaluru -61%, Hyderabad -61% |
| Q3 — Restaurant impact | All top 10 restaurants hit 100% order loss during crisis |
| Q8 — Revenue trend | Revenue mirrored order decline; AOV (avg order value) also fell |

### Step 4 — Deep Analysis (`04_deep_analysis.ipynb`)
Answers Q4–10:

| Question | Finding |
|----------|---------|
| Q4 — Cancellations | Rate doubled from 6.1% → 11.9%; spike in all cities |
| Q5 — SLA compliance | Delivery time +52%; SLA breaches jumped from 56% → 88% |
| Q6 — Ratings | Avg rating fell 4.5 → 2.5; sentiment reversed to negative |
| Q7 — Review keywords | Top terms: food quality, packaging, safety, stale, late |
| Q9 — Loyalty churn | 84.5% of loyal customers churned |
| Q10 — High-value churn | 84% of top 5% customers (by spend) churned; rating drop 4.51 → 2.51 |

---

## Data Model

Star schema — 4 fact tables + 4 dimension tables.

### Fact Tables

| Table | Rows | Key Columns |
|-------|------|-------------|
| `fact_orders` | 149,166 | order_id, customer_id, restaurant_id, delivery_partner_id, order_timestamp, subtotal_amount, discount_amount, delivery_fee, total_amount, is_cancelled |
| `fact_order_items` | 342,994 | order_id, item_id, menu_item_id, quantity, unit_price, line_total |
| `fact_delivery_performance` | 149,166 | order_id, actual_delivery_time_mins, expected_delivery_time_mins, distance_km |
| `fact_ratings` | 68,842 | order_id, customer_id, rating (1–5), review_text, sentiment_score |

### Dimension Tables

| Table | Rows | Key Columns |
|-------|------|-------------|
| `dim_customer` | 107,776 | customer_id, signup_date, city, acquisition_channel |
| `dim_restaurant` | 19,995 | restaurant_id, name, city, cuisine_type, partner_type, avg_prep_time_min, is_active |
| `dim_delivery_partner` | 15,000 | delivery_partner_id, name, city, vehicle_type, employment_type, avg_rating |
| `dim_menu_item` | 342,671 | menu_item_id, restaurant_id, item_name, category, is_veg, price |

**Total records analysed: 1,379,410 rows**
**Period: January 1 – September 30, 2025 (9 months)**

---

## Power BI Dashboard

**File:** `powerbi/Dashboard.pbix` (35 MB)
**Canvas:** 1920 × 1080 px | **Theme:** Navy `#1A2744`, Teal `#0D8A8A`, Orange `#E8743B`

| Page | Content |
|------|---------|
| 1 — Home / Executive Summary | KPI headline cards: total orders, revenue, churn, rating |
| 2 — Orders & Revenue Analytics | Monthly trend, MoM % change, AOV (avg order value) |
| 3 — Delivery & Operations | SLA compliance trend, delivery time distribution, breach rate by city |
| 4 — Ratings & Sentiment | Rating trend, sentiment score line, review word cloud |
| 5 — Customer Loyalty & LTV | Loyal customer churn, high-value segment analysis |
| 6 — Recovery Recommendations | Data-driven recovery plan with strategic actions |

---

## Technology Stack

| Tool | Role |
|------|------|
| Python 3.10+ | Full data pipeline (cleaning, EDA, deep analysis) |
| pandas, numpy | Data manipulation and aggregation |
| duckdb | In-process SQL queries over CSV files |
| matplotlib, seaborn, plotly | Analysis visualizations |
| nltk, textblob, wordcloud | Sentiment analysis and NLP on review text |
| Power BI Desktop | Interactive 6-page dashboard |
| DAX | KPI measures, phase comparisons, rolling calculations |
| Power Query | CSV loading, star schema relationships |

---

## File Structure

```
Food_Delivery_Startup/
│
├── 01_data_quality_report.ipynb      ← Data validation notebook
├── 02_data_cleaning.ipynb            ← Data cleaning pipeline
├── 03_eda_primary_analysis.ipynb     ← Primary EDA (Q1–3, Q8)
├── 04_deep_analysis.ipynb            ← Deep analysis (Q4–10)
├── 01_data_quality_report.py         ← Standalone Python script
├── metadata.txt                      ← Full data dictionary (8 tables)
├── requirements.txt                  ← Python dependencies
├── README.md                         ← Project documentation
├── .gitignore                        ← Excludes .pbix, CSVs, .venv, output/
│
├── Datasets/                         ← Raw source CSVs — 8 files, 69 MB (excluded)
│   ├── fact_orders.csv
│   ├── fact_order_items.csv
│   ├── fact_delivery_performance.csv
│   ├── fact_ratings.csv
│   ├── dim_customer.csv
│   ├── dim_restaurant.csv
│   ├── dim_delivery_partner_.csv
│   └── dim_menu_item.csv
│
├── output/                           ← Generated artifacts (excluded)
│   ├── 01_data_quality_report/       ← Quality check CSVs + DATA_QUALITY_REPORT.md
│   ├── 02_cleaned_data/              ← 8 cleaned CSVs + CLEANING_LOG.md
│   ├── 03_eda_primary/               ← Charts + ANSWERS_Q1_Q2_Q3_Q8.md
│   └── 04_deep_analysis/             ← Charts + ANSWERS_Q4_Q10.md
│
├── powerbi/
│   └── Dashboard.pbix                ← 6-page Power BI dashboard (excluded)
│
├── powerbi_assets/                   ← Design assets (committed)
│   ├── BrandTheme.json               ← Color/typography theme
│   ├── background_1920x1080.png      ← Canvas background
│   ├── logo_large.png
│   ├── logo_sidebar.png
│   ├── card_page2.png – card_page6.png
│   ├── recovery_plan.png
│   └── PowerBI_Dashboard_Guide.md    ← Full build guide (51 KB)
│
└── .venv/                            ← Python virtual environment (excluded)
```

---

## Privacy Note

All customer, restaurant, and delivery partner data is synthetic/anonymized and used for portfolio and learning purposes. All raw data files (`.csv`) and the Power BI workbook (`.pbix`) are excluded from version control.
