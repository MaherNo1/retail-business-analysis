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
online_retail_ii_project/
├── .env.example                 # Template for database connection variables
├── .gitignore                   # Excludes raw data, local venvs, and secrets
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
│
├── config/
│   └── settings.yaml            # Pipeline thresholds, file paths, and cleaning configs
│
├── data/                        # Ignored by Git (stores local binary files)
│   ├── 01_raw/                  # Raw UCI dataset (online_retail_II.xlsx)
│   ├── 02_interim/              # Combined staging files (.parquet)
│   └── 03_processed/            # Cleaned, analytics-ready datasets (.parquet)
│
├── notebooks/                   # Exploratory Data Analysis & Prototyping
│   ├── 01_raw_data_exploration.ipynb
│   ├── 02_anomaly_detection.ipynb
│   └── 03_rfm_prototyping.ipynb
│
├── src/                         # Production Python ETL Modules
│   ├── __init__.py
│   ├── extract.py               # Ingests multi-sheet Excel files
│   ├── transform.py             # Business logic: handles cancellations, non-inventory items
│   ├── load.py                  # Parquet export & DB streaming
│   └── main.py                  # Master execution script
│
├── sql/                         # Relational Data Modeling & Analytics Views
│   ├── 01_schema.sql            # Star Schema (Dimensions & Fact tables)
│   ├── 02_rfm_segmentation.sql  # SQL queries for RFM customer scoring
│   └── 03_powerbi_views.sql     # Database views optimized for Power BI
│
└── powerbi/                     # Business Intelligence Workspace
    ├── online_retail_analytics.pbix  # Interactive Dashboard Report
    └── dax_measures.md               # DAX Formula Catalog & Documentation