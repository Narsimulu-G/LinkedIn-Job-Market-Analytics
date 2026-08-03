# LinkedIn Job Market Analytics Platform 📊

An interactive, production-quality Data Analytics and ETL pipeline designed to ingest, clean, transform, and analyze LinkedIn job postings from 2023.

---

## 🏗️ Project Architecture
The platform is designed around a modular data pipeline that feeds an interactive Streamlit dashboard:

```text
  [Raw CSV Files]
         │
         ▼ (Data Loader: Ingestion & Validation)
  [Data Quality Checks]
         │
         ▼ (Data Cleaner: Deduplication & Normalization)
  [Aggregation & Transformation]
         │  - Join 1-to-many benefits and skills
         │  - Resolve company employee count idxmax bug
         ▼
  [Data Integration & Merging]
         │
         ▼ (Feature Engineering)
         │  - Parse Location (City, State, Country)
         │  - Annualize Salaries (Hourly to Annual conversion)
         │  - Extract Tech Skill flags from description (Python, SQL, etc.)
         ▼
  [Master Analytical Dataset] (data/processed/linkedin_jobs_clean.csv)
         │
         ├───► [Jupyter Notebooks] (Interactive Learning)
         │
         └───► [Streamlit Dashboard] (Production App)
```

---

## 🛠️ Technology Stack
*   **Core**: Python 3.11+
*   **Data Processing**: Pandas, NumPy
*   **Interactive Visualizations**: Plotly, Seaborn, Matplotlib
*   **Dashboard Framework**: Streamlit
*   **Unit Testing**: Pytest

---

## 🚀 Setup & Execution Guide

### Step 1: Clone the Repository & Configure Directory
```bash
git clone https://github.com/Narsimulu-G/LinkedIn-Job-Market-Analytics.git
cd LinkedIn-Job-Market-Analytics
```

### Step 2: Set Up Virtual Environment & Dependencies
```bash
# Create environment
python -m venv .venv

# Activate environment (Windows)
.venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 3: Setup Datasets
Ensure your LinkedIn datasets are unzipped and placed in `C:\Users\naras\Downloads\archive`. Then run the structure initializer script:
```bash
python -m src.setup_data
```
*This copies and organizes all files into `data/raw/` automatically.*

### Step 4: Run the ETL Data Pipeline
Executes data loader, cleaning, transformations, merging, and feature engineering:
```bash
python -m src.pipeline
```
*The clean master dataset is generated and saved as `data/processed/linkedin_jobs_clean.csv`.*

### Step 5: Start the Dashboard
```bash
streamlit run dashboard/app.py
```

### Step 6: Run Tests
To verify all pipeline transformations and cleaners pass:
```bash
python -m pytest -W ignore tests/
```

---

## 📖 Educational Mode
The dashboard includes an active **📘 Learn Analytics Mode** designed for beginners. Toggle it in the sidebar to see:
*   **What** is being calculated.
*   **Why** this metric is relevant.
*   **How** to write the Pandas code to execute it.
*   **Result** interpretations from actual metrics.

---

## 📊 Key Findings
*   **Hiring Volumes**: Job postings are highly dominated by **Full-time positions** (~80%).
*   **Employer Scales**: Large enterprises (Size Category 7) represent the single largest block of recruitment activity.
*   **Tech Demands**: SQL and Python lead technical skill demands across data and engineering vacancies.
