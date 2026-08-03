import pandas as pd
from src import config

def clean_job_postings(df_postings):
    """
    Cleans the main job postings table.
    - Detects and logs duplicates
    - Standardizes categories (work type, experience level)
    """
    df = df_postings.copy()
    
    # 1. Duplicate detection
    duplicates = df['job_id'].duplicated()
    num_duplicates = duplicates.sum()
    print(f"Duplicate check: Found {num_duplicates} duplicate job IDs.")
    if num_duplicates > 0:
        # Report duplicates but remove them to keep unique keys
        duplicate_rows = df[duplicates]
        print(f"Removing duplicate entries for job_ids: {duplicate_rows['job_id'].unique()[:5]}...")
        df = df.drop_duplicates(subset=['job_id'], keep='first')
        
    # Check null Job IDs
    null_job_ids = df['job_id'].isnull().sum()
    if null_job_ids > 0:
        print(f"Warning: Found {null_job_ids} null Job IDs. Removing them.")
        df = df.dropna(subset=['job_id'])
        
    # 2. Work Type Normalization
    print("Normalizing work type categories...")
    # Map raw code values to clean values, default to 'Other' if not found
    df['work_type_clean'] = df['work_type'].map(config.WORK_TYPE_MAP).fillna('Other')
    
    # 3. Experience Level Normalization
    print("Standardizing experience levels...")
    df['experience_level_clean'] = df['formatted_experience_level'].fillna('Not Specified')
    
    # 4. Sponsored flag conversion (make it descriptive string)
    df['sponsored_clean'] = df['sponsored'].map({0: 'Non-Sponsored', 1: 'Sponsored'}).fillna('Non-Sponsored')
    
    return df
