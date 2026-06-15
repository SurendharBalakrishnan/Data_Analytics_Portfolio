# Decoding the 2026 Tamil Nadu Assembly Election

An end-to-end data analytics project built for the Codebasics Resume Project Challenge — turning 234 constituencies of raw Election Commission of India data into a 10-slide editorial data story for fictional client **AtliQ Media**.

> **Note:** Raw datasets (`.csv`) are included as they are public ECI data. The generated `.pptx` deck is excluded via `.gitignore`.

---

## What This Project Does

Analyses seat-level results across **Tamil Nadu's 234 Assembly Constituencies** comparing 2021 and 2026 elections — identifying where seats flipped, how vote shares shifted, and how win margins changed across parties and regions.

---

## Key Findings

| Metric | 2021 | 2026 |
|--------|------|------|
| DMK seats | 133 | — |
| TVK seats | 0 | **108** |
| Seats changed party | — | **163 / 234 (69.7%)** |
| Decisive wins (>50% share) | 70 | 13 |
| Minority wins (<35% share) | 2 | 64 |
| Median win margin | 9.5% | 5.7% |

TVK — a party that did not exist in 2021 — won 108 seats. Of those: **65 from DMK · 26 from AIADMK · 11 from INC · 6 from others**.

---

## Pipeline

| Step | Tool | Output |
|------|------|--------|
| 1. Raw data | ECI results portal + Trivedi Centre (Ashoka University) | 3 CSVs (~8,500 rows) |
| 2. EDA & cleaning | Python (Pandas, Jupyter) | Cleaned datasets, data quality notes |
| 3. Visualisation | Plotly, Matplotlib | 4 charts (Sankey, vote share, margins, regional) |
| 4. Deck generation | python-pptx (`build_deck.py`) | 10-slide PPTX for AtliQ Media |

---

## Data Model

| File | Rows | Description |
|------|------|-------------|
| `tn_2021_results.csv` | 4,232 | Candidate-level results, 234 ACs — source: Trivedi Centre / ECI |
| `tn_2026_results.csv` | 4,257 | Candidate-level results, 234 ACs — source: ECI live results portal |
| `constituency_master.csv` | 234 | AC reference table — district, editorial region, reservation status |

**Columns:** constituency, ac_number, candidate, party, votes, turnout, reserved, region

---

## Charts

| # | Chart | Description |
|---|-------|-------------|
| 1 | [Sankey — Seat Flows](./charts/01_sankey.png) | Where each party's 2021 seats moved in 2026 |
| 2 | [Vote Share Shift](./charts/02_vote_share.png) | Statewide party vote share: 2021 vs 2026 |
| 3 | [Margin Buckets](./charts/03_margin.png) | Win margin distribution shift across elections |
| 4 | [Regional View](./charts/04_regional.png) | Seat counts by 6 editorial regions |

---

## Technology Stack

| Tool | Role |
|------|------|
| Python 3.11 | Core analysis and scripting |
| Pandas / NumPy | Data cleaning, aggregation, joins |
| Plotly | Interactive and static chart generation |
| Matplotlib / Seaborn | Supplementary visualisations |
| python-pptx | Programmatic 10-slide deck generation |
| Jupyter Notebook | Exploratory data analysis |
| conda | Environment management (`environment.yml`) |

---

## Reproduce

```bash
conda env create -f environment.yml
conda activate tn-election
jupyter notebook
# then run: python build_deck.py
```

---

## File Structure

```
tn-election-2026-decoded/
│
├── README.md
├── .gitignore
├── build_deck.py              ← Generates 10-slide PPTX deck
├── environment.yml            ← conda environment
├── requirements.txt           ← pip dependencies
│
├── notebooks/
│   └── 01_data_discovery.ipynb  ← EDA, cleaning, winners table
│
├── charts/                    ← All 4 chart outputs
│   ├── 01_sankey.png / .html
│   ├── 02_vote_share.png / .html
│   ├── 03_margin.png / .html
│   └── 04_regional.png / .html
│
└── data/
    ├── raw/                   ← Original ECI + Trivedi Centre CSVs
    │   ├── tn_2021_results.csv
    │   ├── tn_2026_results.csv
    │   └── constituency_master.csv
    └── processed/             ← Cleaned / derived datasets
        ├── winners_2021.csv
        ├── winners_2026.csv
        └── winners_combined.csv
```

---

## Disclaimer

This is a non-partisan data analysis exercise. No party, leader, community, region, or religion is endorsed or criticised. All conclusions are sourced from publicly available ECI data only.
