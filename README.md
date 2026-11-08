# Online Retail II: End-to-End Data Pipeline & BI Analytics

An end-to-end business intelligence and data engineering pipeline built in VS Code using Python, SQL, and Power BI. The project ingests raw transactional data from the UCI Online Retail II dataset, cleans and transforms it via modular Python scripts, and exports structured datasets for relational modeling and interactive Power BI dashboards.

---

## 📌 Business Overview

The goal of this project is to analyze customer purchasing behavior, sales performance, and product dynamics for an UK-based online retail retailer operating between December 2009 and December 2011.

Key Analytical Focus Areas:
- **Revenue & Growth:** Monthly recurring trends, Average Order Value (AOV), and top revenue-generating markets.
- **Customer Intelligence:** Customer Lifetime Value (CLV), Repeat Purchase Rates, and Recency-Frequency-Monetary (RFM) Segmentation.
- **Product & Inventory Insights:** Identification of top-selling stock items and inventory returns/cancellations.

---

## 🛠️ Tech Stack & Architecture

- **IDE:** Visual Studio Code
- **Language:** Python 3.10+
- **Data Wrangling:** `pandas`, `openpyxl`, `pyarrow`
- **Database / SQL:** PostgreSQL / SQLite, `SQLAlchemy`
- **Data Visualization & BI:** Power BI Desktop (Import Mode / Parquet connection)
- **Configuration & Secrets:** `pyyaml`, `python-dotenv`

---

## 📁 Repository Structure

```text
retail-business-analysis/
├── config/
│   └── settings.yaml          # Externalized business rules & schema mapping
├── data/
│   ├── 01_raw/                # Raw Online Retail II dataset (Excel)
│   ├── 02_interim/            # Staged concatenated Parquet layer
│   └── 03_processed/          # Clean, analytics-ready Parquet dataset
├── src/
│   ├── extract.py             # Reads sheets, standardizes types, outputs interim Parquet
│   ├── transform.py           # Business filtering, rule enforcement, feature engineering
│   └── load.py                # Dataset validation and loading pipeline
├── powerbi/
│   ├── retail_dashboard.pbix  # Interactive Power BI report
│   └── custom_theme.json      # Custom executive UI theme
└── README.md