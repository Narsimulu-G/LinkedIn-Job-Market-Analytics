import pandas as pd
import numpy as np
from src.feature_engineering import annualize_salary, parse_location, process_tech_skills

def test_annualize_salary():
    # Mock row 1: Hourly
    row_hourly = {'salary_min': 50.0, 'pay_period': 'HOURLY'}
    assert annualize_salary(row_hourly, 'salary_min') == 50.0 * 2080
    
    # Mock row 2: Monthly
    row_monthly = {'salary_min': 5000.0, 'pay_period': 'MONTHLY'}
    assert annualize_salary(row_monthly, 'salary_min') == 5000.0 * 12
    
    # Mock row 3: Yearly
    row_yearly = {'salary_min': 90000.0, 'pay_period': 'YEARLY'}
    assert annualize_salary(row_yearly, 'salary_min') == 90000.0

def test_parse_location():
    # Standard format: City, State, Country
    assert parse_location("Los Angeles, CA, United States") == ("Los Angeles", "CA", "United States")
    
    # Compact format: City, State (Default US)
    assert parse_location("Dallas, TX") == ("Dallas", "TX", "United States")
    
    # International format
    assert parse_location("Toronto, ON, Canada") == ("Toronto", "ON", "Canada")
    
    # Single name
    assert parse_location("Remote") == ("Remote", "Unknown", "Unknown")

def test_process_tech_skills():
    # Mock dataframe with descriptions
    data = {
        'job_description': [
            "We are looking for a Python developer with SQL skills.",
            "Must have experience in Java and AWS architecture.",
            "Excel modeling experience is required."
        ]
    }
    df = pd.DataFrame(data)
    
    # Run skills extraction
    df_skills = process_tech_skills(df)
    
    # Assert flags are correct
    assert df_skills['req_python'].tolist() == [1, 0, 0]
    assert df_skills['req_sql'].tolist() == [1, 0, 0]
    assert df_skills['req_java'].tolist() == [0, 1, 0]
    assert df_skills['req_aws'].tolist() == [0, 1, 0]
    assert df_skills['req_excel'].tolist() == [0, 0, 1]
    
    # Assert count is correct
    assert df_skills['tech_skills_count'].tolist() == [2, 2, 1]
