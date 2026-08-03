import os
import pandas as pd
from src import config

def load_job_postings():
    """Loads the main job postings table."""
    path = os.path.join(config.RAW_DATA_DIR, "job_postings.csv")
    print(f"Loading postings from {path}...")
    df = pd.read_csv(path)
    # Enforce correct types
    df['job_id'] = df['job_id'].astype('int64')
    if 'company_id' in df.columns:
        df['company_id'] = df['company_id'].astype('float64')
    return df

def load_benefits():
    """Loads job benefits details."""
    path = os.path.join(config.RAW_DATA_DIR, "job_details", "benefits.csv")
    print(f"Loading benefits from {path}...")
    return pd.read_csv(path)

def load_job_skills():
    """Loads job skills details."""
    path = os.path.join(config.RAW_DATA_DIR, "job_details", "job_skills.csv")
    print(f"Loading job skills from {path}...")
    return pd.read_csv(path)

def load_job_industries():
    """Loads job industries mapping."""
    path = os.path.join(config.RAW_DATA_DIR, "job_details", "job_industries.csv")
    print(f"Loading job industries from {path}...")
    return pd.read_csv(path)

def load_salaries():
    """Loads job salary details."""
    path = os.path.join(config.RAW_DATA_DIR, "job_details", "salaries.csv")
    print(f"Loading salaries from {path}...")
    return pd.read_csv(path)

def load_companies():
    """Loads company details."""
    path = os.path.join(config.RAW_DATA_DIR, "company_details", "companies.csv")
    print(f"Loading companies from {path}...")
    df = pd.read_csv(path)
    df['company_id'] = df['company_id'].astype('int64')
    return df

def load_company_industries():
    """Loads company industries mapping."""
    path = os.path.join(config.RAW_DATA_DIR, "company_details", "company_industries.csv")
    print(f"Loading company industries from {path}...")
    return pd.read_csv(path)

def load_company_specialities():
    """Loads company specialities mapping."""
    path = os.path.join(config.RAW_DATA_DIR, "company_details", "company_specialities.csv")
    print(f"Loading company specialities from {path}...")
    return pd.read_csv(path)

def load_employee_counts():
    """Loads employee count histories."""
    path = os.path.join(config.RAW_DATA_DIR, "company_details", "employee_counts.csv")
    print(f"Loading employee counts from {path}...")
    return pd.read_csv(path)

def load_industry_mappings():
    """Loads industry name mappings."""
    path = os.path.join(config.RAW_DATA_DIR, "mappings", "industries.csv")
    print(f"Loading industry mappings from {path}...")
    return pd.read_csv(path)

def load_skill_mappings():
    """Loads skill name mappings."""
    path = os.path.join(config.RAW_DATA_DIR, "mappings", "skills.csv")
    print(f"Loading skill mappings from {path}...")
    return pd.read_csv(path)
