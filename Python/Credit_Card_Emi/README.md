# Credit Card Statement Analyzer

An end-to-end data pipeline that automates fetching, parsing, and visualizing credit card statements from HDFC Bank and IDFC FIRST Bank — built with Python and Power BI.

---

## Overview

Managing credit card statements manually across multiple banks is tedious. This project automates the entire workflow:

1. **Fetch** — Connects to Gmail via IMAP and downloads PDF statements automatically
2. **Extract** — Opens password-protected PDFs and extracts key financial fields
3. **Transform** — Standardizes data into a clean, structured format
4. **Visualize** — Loads data into a Power BI dashboard for interactive analysis

Covers statement history (2021–2025) across two banks, processing **187 PDF files** (99 HDFC + 88 IDFC).

> **Note on data privacy:** The Power BI dashboard and sample data in this repository use **modified amounts** — exact credit card figures have been altered and 2026 data has been excluded intentionally to avoid exposing real personal financial information. The pipeline logic and structure are fully representative of the actual implementation.

---

## Demo

> Power BI dashboard (`PowerBi/CreditCardProject.pbix`) provides:
> - Monthly and yearly spending trends
> - Bank-wise statement comparisons
> - Amount distribution (min / max / avg)
> - Due date tracking and payment calendar

---

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.x |
| Email Fetching | `imap-tools`, `email-validator` |
| PDF Processing | `pikepdf`, `pdfplumber`, `PyPDF2` |
| Data Wrangling | `pandas`, `numpy`, `openpyxl` |
| Visualization | Power BI Desktop |
| Notebook Environment | Jupyter (`.ipynb`) |

---

## Project Structure

```
Credit Card Emi - github/
├── PowerBi/
│   ├── CreditCardProject.pbix          # Main Power BI dashboard
│   ├── credit_card_statement.xlsx      # Fact table (extracted statement data)
│   ├── credit_card_dimension_tables.xlsx
│   ├── bank_dimension.csv              # HDFC & IDFC metadata
│   ├── date_dimension.csv              # Date hierarchy (2021–2026)
│   └── product_dimension.csv          # Product types (CC, Jumbo Loan, etc.)
├── src/
│   └── email_fetcher/                  # Email fetcher source module
├── notebooks/
│   └── email_fetcher.ipynb            # Phase 1 notebook
├── data/
│   └── raw_emails/                     # Raw downloaded email/PDF storage
├── logs/
│   └── email_fetcher.log              # Processing logs
├── backup/
│   └── hdfc/                          # Backup copies of HDFC statements
├── config/
│   └── email_config.json              # Non-sensitive settings only (credentials in .env)
├── .env.example                       # Credential template — copy to .env and fill in
├── .gitignore                         # Excludes .env, data/, backup/, logs/, *.pbix
├── phase1-notebook.md                 # Phase 1 implementation guide
├── phase2-notebook.ipynb              # Phase 2: PDF extraction
├── email-fetcher.py                   # Standalone email fetcher script
└── requirements.txt                   # Python dependencies
```

---

## Pipeline Phases

### Phase 1 — Email Fetching

Connects to Gmail over IMAP (SSL), searches for statements from known bank senders, and downloads PDF attachments.

**Supported senders:**
- HDFC: `**********@hdfcbank.net`, `**********@hdfcbank.com`
- IDFC: `********@idfcfirstbank.com`

**Output:** PDF files saved locally with safe filenames (`HDFC_YYYYMMDD_statement.pdf`)

---

### Phase 2 — PDF Data Extraction

Opens each password-protected PDF and extracts structured data using a multi-method fallback chain:

```
pikepdf (primary) → PyPDF2 (fallback) → pdfplumber (fallback)
```

**Fields extracted per statement:**

| Field | Description |
|---|---|
| `DATE` | Standardized statement date (`DD/MM/YYYY`) |
| `MONTH` | Month name |
| `YEAR` | 4-digit year |
| `BANK` | `HDFC` or `IDFC` |
| `AMOUNT` | Total amount due (₹) |
| `DUE_DATE` | Payment due date |
| `FILE_NAME` | Source PDF filename |
| `PROCESSED_TIME` | Processing timestamp |

**Validation rules:**
- File size: 1 KB – 10 MB
- Amount range: ₹50 – ₹10,00,000
- Batch processing (20 files at a time) to manage memory

---

### Phase 3 — Power BI Dashboard

Data is loaded into a star-schema model in Power BI:

- **Fact table:** `credit_card_statement.xlsx`
- **Dimensions:** Bank, Date, Product

---

## Setup & Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure credentials

Copy `.env.example` to `.env` and fill in your real values:

```bash
cp .env.example .env
```

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

IMAP_SERVER=imap.gmail.com
IMAP_PORT=993

HDFC_PDF_PASSWORD=your_hdfc_pdf_password
IDFC_PDF_PASSWORD=your_idfc_pdf_password
```

> **Gmail:** Use a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your main account password.
> **Never commit `.env` to version control** — it is already listed in `.gitignore`.

### 3. Run Phase 1 — Fetch emails

```bash
python email-fetcher.py
```

Or open and run `notebooks/email_fetcher.ipynb` in Jupyter.

### 4. Run Phase 2 — Extract PDF data

Open and run `phase2-notebook.ipynb` in Jupyter.

### 5. Visualize in Power BI

Open `PowerBi/CreditCardProject.pbix` in Power BI Desktop and refresh the data source.

---

## Data Model

```
                  ┌─────────────────┐
                  │  bank_dimension  │
                  │  HDFC / IDFC    │
                  └────────┬────────┘
                           │
┌──────────────┐    ┌──────┴──────────────┐    ┌────────────────────┐
│date_dimension│────│ credit_card_statement│────│ product_dimension  │
│ 2021 – 2026  │    │   (Fact Table)       │    │ CC / Jumbo Loan    │
└──────────────┘    └─────────────────────┘    └────────────────────┘
```

---

## Key Results

- **187 PDFs processed** successfully (99 HDFC + 88 IDFC)
- **6 years** of historical statement data (2021–2026)
- Automated pipeline reduces manual effort from hours to minutes
- Error logging captures and reports any failed extractions

---

## Banks Supported

| Bank | Type | Established | Segment |
|---|---|---|---|
| HDFC Bank | Private Sector | 1994 | Premium Banking |
| IDFC FIRST Bank | Private Sector | 2015 | Digital Banking |

---

## Skills Demonstrated

- Email automation with IMAP protocol
- PDF parsing and password-protected document handling
- ETL pipeline design (Extract → Transform → Load)
- Star-schema data modeling for analytics
- Power BI dashboard development
- Python data engineering (pandas, error handling, batch processing)

---

## Security

This project handles sensitive financial data. The following measures are in place:

| What | How |
|---|---|
| Email & PDF credentials | Stored in `.env` only — never in code |
| `.env` file | Listed in `.gitignore`, never committed |
| `config/email_config.json` | Contains non-sensitive settings only |
| Downloaded PDFs (`data/`, `backup/`) | Excluded from git via `.gitignore` |
| Processing logs (`logs/`) | Excluded — may contain account metadata |
| Power BI files (`*.pbix`, `*.xlsx`) | Excluded — contain real financial data |
| Notebook outputs | `.ipynb_checkpoints/` excluded; outputs cleared before committing |
| Sample data amounts | Modified/anonymized — do not reflect real credit card usage |
| 2026 data | Excluded entirely from the repository |

**Before pushing to GitHub:**
- Run `git status` to confirm no `.env`, PDF files, or data folders are staged
- Passwords print as `[SET]` / `[NOT SET]` in notebook output — never the actual value

---

## License

This project is for personal portfolio and educational purposes. Credentials and personal financial data are not included in this repository.
