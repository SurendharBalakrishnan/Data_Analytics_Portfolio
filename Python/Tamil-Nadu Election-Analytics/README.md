# Tamil Nadu Assembly Election 2026 — Data Analytics

An end-to-end Python analytics project analysing **234 constituency results** across Tamil Nadu's 2021 and 2026 Assembly Elections — from raw ECI data through Jupyter EDA, Plotly visualisations, and an auto-generated 10-slide editorial deck built with `python-pptx`.

> **Codebasics Resume Project Challenge** — Completed

---

## Project Objective

To analyse how 234 Tamil Nadu Assembly seats moved between 2021 and 2026 and answer:

- Which party won the most seats in 2026 — and where did they come from?
- How did statewide vote shares shift across parties?
- Did win margins get larger or smaller compared to 2021?
- Which regions of Tamil Nadu saw the biggest swings?
- What does a data-only, non-partisan editorial story look like?

---

## Key Findings

| Metric | 2021 | 2026 |
|--------|------|------|
| TVK seats | 0 | **108** |
| Seats that changed party | — | **163 / 234 (69.7%)** |
| TVK statewide vote share | 0% | **34.9%** |
| DMK vote share drop | — | −13.5 pp |
| AIADMK vote share drop | — | −12.1 pp |
| Decisive wins (>50% share) | 70 | **13** |
| Minority wins (<35% share) | 2 | **64** |
| Median win margin | 9.5% | **5.7%** |

TVK won **108 of 234 seats** — a party that did not exist in 2021. Of those 108 wins: **65 from DMK · 26 from AIADMK · 11 from INC · 6 from others**.

---

## Dashboard / Charts

| # | Chart | View |
|---|-------|------|
| 1 | Sankey — Seat Flows (2021 → 2026) | [PNG](./tn-election-2026-decoded/charts/01_sankey.png) |
| 2 | Vote Share Shift by Party | [PNG](./tn-election-2026-decoded/charts/02_vote_share.png) |
| 3 | Win Margin Buckets | [PNG](./tn-election-2026-decoded/charts/03_margin.png) |
| 4 | Regional Seat Counts | [PNG](./tn-election-2026-decoded/charts/04_regional.png) |

---

## Data Architecture

Four-step pipeline:

| Step | Layer | Tool | Description |
|------|-------|------|-------------|
| 1 | Raw Data | ECI / Trivedi Centre | 3 CSVs — 8,489 candidate rows across 234 ACs |
| 2 | EDA & Cleaning | Python, Pandas, Jupyter | Deduplication, party normalisation, winners table |
| 3 | Visualisation | Plotly, Matplotlib | 4 charts — Sankey, vote share, margins, regional |
| 4 | Deck Generation | python-pptx | `build_deck.py` → 10-slide PPTX for AtliQ Media |

---

## Data Model

| Table | Rows | Description |
|-------|------|-------------|
| `tn_2021_results.csv` | 4,232 | Candidate-level results — 2021 TN election (Trivedi Centre / ECI) |
| `tn_2026_results.csv` | 4,257 | Candidate-level results — 2026 TN election (ECI live results portal) |
| `constituency_master.csv` | 234 | Reference table — AC number, district, editorial region, reservation status |

**Total: ~8,500 rows** | Key columns: `constituency`, `ac_number`, `candidate`, `party`, `votes`, `turnout`, `reserved`, `region`

---

## Technology Stack

| Tool | Role |
|------|------|
| Python 3.11 | Core language |
| Pandas / NumPy | Data cleaning, aggregation, joins |
| Plotly | Sankey diagram, interactive charts |
| Matplotlib / Seaborn | Supplementary static charts |
| python-pptx | Programmatic 10-slide deck generation |
| Jupyter Notebook | Exploratory data analysis |
| conda | Environment management |

---

## File Structure

```
Tamil-Nadu Election-Analytics/
│
├── README.md                              ← Project documentation
├── .gitignore
├── metadata.txt                           ← Column descriptions for all CSVs
│
└── tn-election-2026-decoded/              ← Main project code
    ├── README.md                          ← Technical README (reproduce steps)
    ├── build_deck.py                      ← Generates 10-slide PPTX
    ├── environment.yml                    ← conda environment
    ├── requirements.txt                   ← pip dependencies
    │
    ├── notebooks/
    │   └── 01_data_discovery.ipynb        ← EDA, cleaning, winners table
    │
    ├── charts/                            ← All chart outputs (PNG + HTML)
    │   ├── 01_sankey.png / .html
    │   ├── 02_vote_share.png / .html
    │   ├── 03_margin.png / .html
    │   └── 04_regional.png / .html
    │
    └── data/
        ├── raw/                           ← Original ECI + Trivedi Centre CSVs
        │   ├── tn_2021_results.csv        (4,232 rows)
        │   ├── tn_2026_results.csv        (4,257 rows)
        │   └── constituency_master.csv    (234 rows)
        └── processed/                     ← Cleaned / derived datasets
            ├── winners_2021.csv
            ├── winners_2026.csv
            └── winners_combined.csv
```

---

## Privacy Note

All election data is sourced from publicly available ECI results and the Trivedi Centre for Political Data (Ashoka University). This is a non-partisan analysis — no party, leader, community, region, or religion is endorsed or criticised.
