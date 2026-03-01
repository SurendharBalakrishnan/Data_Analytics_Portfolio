# OTT Platform Merger Analysis — LioCinema × Jotstar

A **Power BI dashboard** and SQL-based analytics project built for a CodeBasics Resume Project Challenge — comparing two Indian OTT streaming platforms (LioCinema and Jotstar) to support a strategic merger decision by Lio, India's leading telecom provider.

> **Note:** The `.pbix` dashboard, all SQL database dumps, and PDF documents are excluded from this repository via `.gitignore`. SQL analysis scripts and design assets are committed.

---

## Business Context

Lio (telecom) is planning to merge with **Jotstar** (premium streaming) to create a unified OTT platform. The goal of this project is to analyse 11 months of subscriber and content consumption data (Jan–Nov 2024) from both platforms and deliver comparative insights to C-suite stakeholders.

| Platform | Subscription Plans | Focus |
|----------|--------------------|-------|
| LioCinema | Free, Basic (₹69/mo), Premium (₹129/mo) | Mass-market, Tier 2 & 3 cities |
| Jotstar | Free, VIP (₹159/mo), Premium (₹359/mo) | Premium content, higher ARPU |

---

## Project Objective

To compare both platforms and answer:

- How do LioCinema and Jotstar compare on total users, growth, and active rate?
- Which platform has a larger and more diverse content library?
- How do subscriber demographics (age group, city tier) differ between platforms?
- What are the watch time and device usage patterns on each platform?
- Which platform has better upgrade and downgrade rates?
- How does revenue and ARPU compare given the different pricing models?
- What strategies should the merged platform adopt?

---

## Dashboard

**File:** `Power Bi Output.pbix` (33 MB, excluded from repo)

| Page | Content |
|------|---------|
| 1 — Executive Overview | KPI cards: total users, active rate, paid users %, total content |
| 2 — Overview | Side-by-side platform comparison — content library, users, growth |
| 3 — Users & Growth | Monthly new user acquisition, cumulative growth rate (%) |
| 4 — Engagement & Consumption | Total & avg watch time by platform, device type, city tier |
| 5 — Demographics | Age group distribution, city tier breakdown, subscription plan mix |
| 6 — Revenue Analysis | Revenue by plan, by platform, by month; pricing tier comparison |

**Dashboard screenshots** → `Screenshots/` folder *(to be added)*

---

## Data Sources

Two MySQL databases — full subscriber, content, and consumption data for Jan–Nov 2024.

### LioCinema Database (`liocinema_db`)
**SQL Dump:** `datasets/LioCinema_db.sql` (28 MB, excluded)

| Table | Key Columns |
|-------|-------------|
| `subscribers` | user_id, age_group (18-24 / 25-34 / 35-44 / 45+), city_tier (Tier 1/2/3), subscription_date, subscription_plan (Free / Basic / Premium), last_active_date, plan_change_date, new_subscription_plan |
| `contents` | content_id, content_type (Movie / Series), language, genre, run_time |
| `content_consumption` | user_id, device_type (Mobile / TV / Tablet), total_watch_time (mins) |

### Jotstar Database (`jotstar_db`)
**SQL Dump:** `datasets/Jotstar_db.sql` (7.7 MB, excluded)

| Table | Key Columns |
|-------|-------------|
| `subscribers` | user_id, age_group, city_tier, subscription_date, subscription_plan (Free / VIP / Premium), last_active_date, plan_change_date, new_subscription_plan |
| `contents` | content_id, content_type, language, genre, run_time |
| `content_consumption` | user_id, device_type (Mobile / TV / Laptop), total_watch_time (mins) |

**Analysis period:** January – November 2024 (11 months)

---

## SQL Scripts

| Script | Purpose |
|--------|---------|
| `liocinema_db data_cleaning.sql` | Creates 3 clean views: `subscribers_clean`, `content_consumption_clean`, `contents_clean` — normalises text, filters invalid records, computes `activity_status` |
| `jotstar_db data_cleaning.sql` | Same cleaning approach for Jotstar database |
| `Cleaning Process continues Pre-aggregate_watch_time_per_user_both_db.sql` | Creates `user_watch_time` pre-aggregated views per platform to optimise Power BI query performance |
| `BenchMark - Consolidated KPI Query – Users & Activity (Platform-wise).sql` | 418-line consolidated query covering all 6 KPI areas: users & activity, growth, content library, engagement, subscription plan movements, revenue |
| `Bench mark validation.sql` | 6-step validation queries to cross-check all KPI calculations for accuracy |

---

## Key Metrics Framework (16 Metrics)

| # | Metric | Description |
|---|--------|-------------|
| 1 | Total Users | All registered subscribers |
| 2 | Active Users | Users with no `last_active_date` (NULL = active) |
| 3 | Inactive Users | Users with a recorded `last_active_date` |
| 4 | Active Rate % | Active / Total × 100 |
| 5 | Inactive Rate % | Inactive / Total × 100 |
| 6 | Paid Users | Subscribers on Basic / VIP / Premium plans |
| 7 | Paid Users % | Paid / Total × 100 |
| 8 | Monthly Growth Rate % | New users month-over-month change |
| 9 | Total Content Items | Count of movies + series in library |
| 10 | Total Watch Time (hrs) | Sum of all `total_watch_time` / 60 |
| 11 | Avg Watch Time (hrs) | Per-user average watch time |
| 12 | Upgraded Users | Count of plan upgrades (e.g. Free → Premium) |
| 13 | Upgrade Rate % | Upgraded / Total × 100 |
| 14 | Downgraded Users | Count of plan downgrades |
| 15 | Downgrade Rate % | Downgraded / Total × 100 |
| 16 | Total Revenue | Paid users × plan price per month, summed |

---

## Strategic Recommendations

Six areas identified for the merged platform:

1. **Inactive user re-engagement** — targeted campaigns for churned subscribers
2. **Unified brand campaign** — communicate merger value to existing user bases
3. **Pricing strategy** — bridge LioCinema's mass-market pricing with Jotstar's premium tiers
4. **Telecom bundle opportunity** — leverage Lio's network to drive OTT bundle adoption
5. **AI/ML personalisation** — combine content libraries for cross-platform recommendations
6. **Brand ambassador selection** — data-driven choice based on demographics

---

## Technology Stack

| Tool | Role |
|------|------|
| MySQL 8.0 | Database hosting for both platform dumps |
| SQL (DDL + DML) | Data cleaning views, KPI queries, validation scripts |
| Power BI Desktop | 6-page interactive dashboard |
| DAX | Calculated measures, platform comparisons, revenue calculations |
| Power Query | MySQL connection, data transformation |

---

## File Structure

```
OTT_Domain/
│
├── Power Bi Output.pbix                        ← Main dashboard (excluded)
├── meta_data.txt                               ← Data dictionary for both DBs
├── README.md                                   ← Project documentation
├── .gitignore                                  ← Excludes .pbix, .sql, .pdf, .claude/
│
├── SQL Scripts (committed)
│   ├── liocinema_db data_cleaning.sql
│   ├── jotstar_db data_cleaning.sql
│   ├── Cleaning Process continues Pre-aggregate_watch_time_per_user_both_db.sql
│   ├── BenchMark - Consolidated KPI Query – Users & Activity (Platform-wise).sql
│   └── Bench mark validation.sql
│
├── datasets/                                   ← MySQL dumps (excluded — 35.7 MB total)
│   ├── LioCinema_db.sql                        (28 MB)
│   └── Jotstar_db.sql                          (7.7 MB)
│
├── Screenshots/                                ← Dashboard screenshots (to be added)
│   └── insightsand startergic recomendations.png
│
├── page6_background.png                        ← Dashboard page 6 background asset
│
└── .claude/                                    ← Claude IDE config (excluded)
```

---

## Privacy Note

All subscriber data in the SQL dumps is synthetic/anonymized and provided as part of the CodeBasics Resume Project Challenge. No real user data is committed to this repository. All database dumps and the Power BI workbook are excluded from version control.
