import re
import numpy as np
import pandas as pd
from src import config

def annualize_salary(row, col):
    """Converts a salary value to annual rate based on the pay period."""
    val = row[col]
    if pd.isnull(val):
        return np.nan
        
    period = str(row.get('pay_period', '')).upper()
    if period == 'HOURLY':
        return val * 2080 # 40 hours * 52 weeks
    elif period == 'MONTHLY':
        return val * 12
    elif period == 'WEEKLY':
        return val * 52
    elif period == 'DAILY':
        return val * 260 # 5 days * 52 weeks
    return val # Default is YEARLY/ONCE

def process_salaries(df):
    """Computes standardized annual salaries."""
    print("Standardizing salaries to annual scales...")
    df_out = df.copy()
    
    df_out['salary_min_annual'] = df_out.apply(lambda r: annualize_salary(r, 'salary_min'), axis=1)
    df_out['salary_max_annual'] = df_out.apply(lambda r: annualize_salary(r, 'salary_max'), axis=1)
    
    # Midpoint annual salary calculation
    df_out['salary_midpoint_annual'] = (df_out['salary_min_annual'] + df_out['salary_max_annual']) / 2
    
    # If midpoint is missing but salary_median is present (rare)
    if 'salary_median' in df_out.columns:
        df_out['salary_median_annual'] = df_out.apply(lambda r: annualize_salary(r, 'salary_median'), axis=1)
        # Fill midpoint with median if both bounds are missing
        df_out['salary_midpoint_annual'] = df_out['salary_midpoint_annual'].fillna(df_out['salary_median_annual'])
        
    df_out['salary_available'] = df_out['salary_midpoint_annual'].notnull().astype(int)
    return df_out

def parse_location(loc_str):
    """Parses location strings like 'San Francisco, CA' or 'London, UK' into City, State, Country."""
    if pd.isnull(loc_str):
        return "Unknown", "Unknown", "Unknown"
        
    parts = [p.strip() for p in str(loc_str).split(',')]
    if len(parts) >= 3:
        return parts[0], parts[1], parts[2]
    elif len(parts) == 2:
        # Check if the second part is a US state code (2 letters) or a country
        state = parts[1]
        if len(state) == 2 and state.isupper():
            return parts[0], state, "United States"
        return parts[0], "Unknown", state
    return parts[0], "Unknown", "Unknown"

def process_locations(df):
    """Parses locations and appends city, state, country columns."""
    print("Parsing job locations into City, State, and Country...")
    df_out = df.copy()
    
    locs = df_out['location'].apply(parse_location)
    df_out['city'] = [l[0] for l in locs]
    df_out['state'] = [l[1] for l in locs]
    df_out['country'] = [l[2] for l in locs]
    return df_out

def process_tech_skills(df):
    """Extracts technical skill flags from job descriptions using regex matching."""
    print("Extracting technical skill keywords from job descriptions...")
    df_out = df.copy()
    
    descriptions = df_out['job_description'].fillna('').astype(str)
    
    skill_cols = []
    for skill in config.TECH_SKILLS_LIST:
        # Use word boundaries (\b) to avoid matching parts of other words (e.g. 'Java' in 'Javascript')
        # C++ needs special escaping to handle the plus symbols
        escaped_skill = re.escape(skill).replace(r'\+\+', r'\+\+')
        pattern = r'\b' + escaped_skill + r'\b'
        
        col_name = f"req_{skill.lower().replace('+', 'p')}"
        df_out[col_name] = descriptions.str.contains(pattern, case=False, na=False).astype(int)
        skill_cols.append(col_name)
        
    df_out['tech_skills_count'] = df_out[skill_cols].sum(axis=1)
    return df_out

def run_feature_engineering(df):
    """Executes all feature engineering modules."""
    df_enriched = process_salaries(df)
    df_enriched = process_locations(df_enriched)
    df_enriched = process_tech_skills(df_enriched)
    return df_enriched
