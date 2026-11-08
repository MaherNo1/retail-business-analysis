# End-to-End Retail ETL & Analytics Pipeline

An end-to-end data analysis and pipeline project built on the **Online Retail II** dataset from the UCI Machine Learning Repository. This project processes raw e-commerce transaction logs (2009–2011) through a custom Python ETL pipeline, stores interim and clean states in Parquet format, and delivers interactive executive insights through Power BI using custom DAX measures.

---

## Executive Summary & Key Insights

* **Revenue Overview:** Total revenue reached **~$17.09M** across **~37K total orders**, yielding an overall **Average Order Value (AOV)** of **~$466.25**.
* **Geographic Distribution:** The **United Kingdom** represents the vast majority of overall sales volume (~$14M+), followed by primary international European markets including **EIRE (Ireland)**, the **Netherlands**, **Germany**, and **France**.
* **Customer Base:** The store successfully served over **6,000 unique customers**, driven primarily by high repeat purchasing patterns in core territories.

---

## Technical Architecture

```text
retail-business-analysis/
├── config/
│   └── settings.yaml          # Pipeline rules, column mappings, and excluded stock codes
├── data/
│   ├── 01_raw/                # Raw Excel dataset (online_retail_II.xlsx)
│   ├── 02_interim/            # Staging raw Parquet dataset
│   └── 03_processed/          # Final analytics-ready Parquet file
├── src/
│   ├── extract.py             # Reads sheets, standardizes types, outputs staging Parquet
│   ├── transform.py           # Applied business cleaning rules & feature engineering
│   └── load.py                # Pipeline validation layer
├── powerbi/
│   └── retail_dashboard.pbix  # Interactive Power BI Report
└── README.md
```

---

## Data Pipeline (ETL Details)

1. **Extraction (`src/extract.py`):**
   - Concatenates historical worksheets covering 2009–2010 and 2010–2011.
   - Enforces explicit string dtypes on key fields (`Invoice`, `StockCode`, `Description`, `Customer ID`) to prevent conversion errors.
   - Outputs raw concatenated data to `data/02_interim/raw_combined.parquet`.

2. **Transformation (`src/transform.py`):**
   - Drops records lacking a `customer_id`.
   - Filters out cancellation invoices (prefixed with `"C"`) and records where `quantity < 1`.
   - Strips non-inventory administrative fees (e.g., `POST`, `D`, `M`, `BANK CHARGES`).
   - Standardizes dates to datetime format and removes duplicate transactions.
   - **Feature Engineering:** Computes total transaction value (`total_sales = quantity * unit_price`).

3. **Loading (`src/load.py`):**
   - Verifies record integrity and saves the cleaned dataset to `data/03_processed/clean_online_retail.parquet`.

---

## Data Model & DAX Measures

All metrics are isolated within a dedicated `_Measures` table inside Power BI:

* **Total Revenue:**
  ```dax
  Total Revenue = SUM('clean_online_retail'[total_sales])
  ```
* **Total Orders:**
  ```dax
  Total Orders = DISTINCTCOUNT('clean_online_retail'[invoice_no])
  ```
* **Total Customers:**
  ```dax
  Total Customers = DISTINCTCOUNT('clean_online_retail'[customer_id])
  ```
* **Average Order Value (AOV):**
  ```dax
  Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
  ```

---

## Business Recommendations

1. **International Expansion:** Target marketing campaigns specifically toward EIRE and the Netherlands, which stand out as the strongest secondary revenue streams outside the primary UK market.
2. **Order Value Optimization:** Implement bundled product promotions to help increase Average Order Value beyond the current $466 baseline.