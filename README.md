# ☁️ Automated Data Ingestion Pipeline on AWS

> A cloud-native, serverless data ingestion pipeline simulating AWS architecture (S3, Lambda, Glue, Athena) using Python, Boto3, and Moto — processing 50,000 pharma sales records with automated validation, file routing, and business intelligence reporting.

---

## 📌 Business Problem

Pharmaceutical companies receive large volumes of sales data daily from multiple sources. Manually uploading, validating, and processing this data is error-prone, slow, and unscalable. This project automates the entire pipeline:

- **Automatically ingests** raw CSV data into cloud storage (S3)
- **Validates** data quality before processing
- **Routes** files intelligently — valid files to processing, invalid to logs
- **Runs business queries** simulating AWS Athena on processed data
- **Generates 5 BI reports** saved back to cloud storage

---

## 🏗️ Architecture

```
Raw CSV Upload
      │
      ▼
┌─────────────────────┐
│   AWS S3 (Moto)     │  Bucket: pharma-sales-pipeline
│                     │  Folders: raw/ processed/ output/ logs/
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Lambda Function    │  Triggered on file arrival in raw/
│  (Simulated)        │  Validates data quality (5 checks)
└────────┬────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
processed/   logs/
(valid)    (invalid + error report)
    │
    ▼
┌─────────────────────┐
│  Athena Query       │  5 Business SQL queries
│  Engine             │  Results saved to output/
│  (Simulated)        │
└─────────────────────┘
         │
         ▼
  output/ (5 CSV reports)
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Cloud Platform | AWS S3, Lambda, Glue, Athena (via Moto) |
| AWS SDK | Boto3 |
| AWS Mocking | Moto (industry-standard AWS testing library) |
| Data Processing | Pandas, NumPy |
| Language | Python 3.14 |
| Testing | PyTest |
| Version Control | Git, GitHub |

---

## 💡 Why Moto?

> Moto is the **industry-standard library** for testing AWS code locally. It integrates directly into PyTest via decorators, making unit tests cleaner and faster than spinning up real AWS infrastructure. This is a real-world best practice used in CI/CD pipelines at production companies — the Boto3 code is identical to real AWS, only the endpoint is mocked.

---

## 📁 Project Structure

```
Automated-Data-Ingestion-Pipeline/
│
├── data/
│   ├── pharma_sales_raw.csv          ← raw input (50,100 records)
│   └── pharma_sales_clean.csv        ← cleaned input (50,000 records)
│
├── scripts/
│   ├── 01_setup_s3.py                ← create bucket + upload to raw/
│   ├── 02_validate_and_route.py      ← validate + route to processed/
│   ├── 03_query_engine.py            ← run 5 Athena-style queries
│   └── 04_pipeline_runner.py         ← master pipeline (runs all steps)
│
├── tests/
│   └── test_pipeline.py              ← PyTest unit tests (mock_aws)
│
├── output/
│   ├── q1_revenue_by_region.csv
│   ├── q2_monthly_trend.csv
│   ├── q3_top_products.csv
│   ├── q4_category_revenue.csv
│   └── q5_data_quality_summary.csv
│
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- Git

### Step 1 — Clone the Repository
```bash
git clone https://github.com/navanee7h/automated-data-ingestion-pipeline.git
cd automated-data-ingestion-pipeline
```

### Step 2 — Install Dependencies
```bash
pip install boto3 moto[s3] pandas numpy pytest
```

### Step 3 — Run Full Pipeline
```bash
python scripts/04_pipeline_runner.py
```

### Step 4 — Run Unit Tests
```bash
python -m pytest tests/test_pipeline.py -v
```

---

## 📊 Dataset Overview

| Property | Value |
|---|---|
| Raw Records | 50,100 |
| Cleaned Records | 50,000 |
| Duplicates Removed | 100 |
| Nulls Handled | 251 |
| Products | 42 unique |
| Categories | 8 unique |
| Regions | 11 unique |
| Customers | 36 unique |
| Date Range | 2021-01-01 to 2024-12-31 |

---

## 🔍 Pipeline Results

### ✅ Step 1 — S3 Setup & Upload
```
Bucket Created    : pharma-sales-pipeline
Folders Created   : raw/ processed/ output/ logs/
File Uploaded     : pharma_sales_clean.csv → raw/
Records Uploaded  : 50,000
```

### ✅ Step 2 — Validation & Routing (5/5 Checks Passed)
```
[PASS] Column structure check
[PASS] Null check on critical columns
[PASS] Row count check (50,000 > 40,000)
[PASS] Positive values check
[PASS] Date range check (2021–2024)

Quality Score  : 5/5 checks passed
Routing        : pharma_sales_clean.csv → processed/
```

### ✅ Step 3 — Business Query Engine (5 Queries)

**Query 1 — Total Revenue by Region**
- Revenue breakdown across all 11 pharma sales regions
- Identifies top and bottom performing territories

**Query 2 — Monthly Sales Trend**
- Month-over-month revenue across 4 years (2021–2024)
- 48 data points for trend analysis

**Query 3 — Top Products by Units Sold**
- Ranks all 42 products by quantity sold
- Includes total revenue per product

**Query 4 — Revenue Share by Category**
- Revenue percentage breakdown across 8 categories
- Identifies highest-value product categories

**Query 5 — Data Quality Summary**
- Total rows, revenue, avg order value
- Complete data health report

---

## ⏱️ Pipeline Execution Summary

| Step | Status | Description |
|---|---|---|
| 1 — S3 Setup | ✅ SUCCESS | Bucket + folders created, file uploaded |
| 2 — Validation | ✅ SUCCESS | 5/5 quality checks passed |
| 3 — Query Engine | ✅ SUCCESS | 5 business queries executed |
| **Pipeline Status** | **COMPLETE** ✓ | All steps successful |

```
Total Records Processed  : 50,000
Output Files Generated   : 5
Pipeline Status          : COMPLETE ✓
```

---

## 🧪 Unit Tests

```bash
python -m pytest tests/test_pipeline.py -v
```

**Tests cover:**

| Category | Tests |
|---|---|
| S3 Operations | Bucket created, folders exist, file uploaded, file routed correctly |
| Validation Logic | Columns present, no nulls, row count, positive values, date range |
| Query Engine | Output files exist, correct columns, correct row counts, percentages sum to 100% |

---

## 💡 Key Business Insights

1. **Automated routing** eliminates manual file management — valid files instantly move to processing
2. **5/5 quality checks** ensure only clean, validated data reaches the query engine
3. **Zero infrastructure cost** — entire pipeline runs locally using Moto mock
4. **Production-ready code** — identical Boto3 code works on real AWS by removing mock decorators
5. **48 months of trend data** available for sales forecasting

---

## 🔄 Running on Real AWS

To run on real AWS instead of Moto:

1. Configure AWS credentials:
```bash
aws configure
```

2. Remove `@mock_aws` decorators from all scripts

3. Update region if needed:
```python
region_name="ap-south-1"  # Mumbai
```

4. Run the pipeline — same code, real AWS!

---

## 🎯 Agile Delivery

**Sprint 1 — Infrastructure & Ingestion**
- S3 bucket setup and folder structure
- File upload automation using Boto3
- Raw data landing zone design

**Sprint 2 — Validation, Routing & Reporting**
- Data quality validation engine
- Intelligent file routing logic
- Athena-style query engine
- Unit testing and documentation

---

## 👤 Author

**Navaneeth Krishna C**
- 📧 navaneeth364@gmail.com
- 📱 8589902439
- 🎓 Integrated MCA — SCMS School of Technology and Management (7.92 CGPA)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
