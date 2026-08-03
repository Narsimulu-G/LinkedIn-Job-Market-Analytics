import pandas as pd

def merge_all_datasets(df_postings, df_benefits, df_skills, df_companies, df_comp_ind, df_comp_spec, df_emp_counts):
    """
    Connects all data tables together.
    1. Enrich company metadata with industries, specialities, and employee counts.
    2. Left merge postings with benefits, skills, and enriched company records.
    3. Filter and cleanly rename target columns.
    """
    # 1. Enriched Companies Data
    df_comp_enriched = df_companies.copy()
    
    if df_comp_ind is not None:
        df_comp_enriched = df_comp_enriched.merge(df_comp_ind, on='company_id', how='left')
    if df_comp_spec is not None:
        df_comp_enriched = df_comp_enriched.merge(df_comp_spec, on='company_id', how='left')
    if df_emp_counts is not None:
        df_comp_enriched = df_comp_enriched.merge(df_emp_counts, on='company_id', how='left')
        
    print("Merging clean job postings with benefits and skills details...")
    df_merged = df_postings.copy()
    
    if df_benefits is not None:
        df_merged = df_merged.merge(df_benefits, on='job_id', how='left')
    if df_skills is not None:
        df_merged = df_merged.merge(df_skills, on='job_id', how='left')
        
    print("Integrating job records with company metrics...")
    # Left merge postings with company details on company_id
    df_final = df_merged.merge(df_comp_enriched, on='company_id', how='left', suffixes=('_job', '_company'))
    
    # 2. Select & Rename columns cleanly
    selected_columns = {
        'job_id': 'job_id',
        'title': 'job_title',
        'name': 'company_name',
        'description_job': 'job_description',
        'work_type_clean': 'work_type',
        'location': 'location', # remains 'location' as there's no name collision in companies
        'original_listed_time': 'listed_time',
        'application_type': 'application_type',
        'sponsored_clean': 'sponsored',
        'company_size': 'company_size_code',
        'employee_count': 'employee_count',
        'follower_count': 'follower_count',
        'job_benefits': 'benefits',
        'skill_categories': 'skill_categories',
        'min_salary': 'salary_min',
        'max_salary': 'salary_max',
        'med_salary': 'salary_median',
        'pay_period': 'pay_period',
        'currency': 'currency',
        'experience_level_clean': 'experience_level',
        'company_industries': 'company_industries',
        'company_specialities': 'company_specialities'
    }
    
    # Verify columns exist before filtering to prevent KeyErrors
    cols_to_use = [col for col in selected_columns.keys() if col in df_final.columns]
    mapping = {k: v for k, v in selected_columns.items() if k in cols_to_use}
    
    df_analytical = df_final[cols_to_use].rename(columns=mapping)
    
    # Fill categorical nulls with defaults instead of dropna()
    df_analytical['company_name'] = df_analytical['company_name'].fillna('Unknown Company')
    df_analytical['benefits'] = df_analytical['benefits'].fillna('Not Specified')
    df_analytical['skill_categories'] = df_analytical['skill_categories'].fillna('Not Specified')
    df_analytical['company_industries'] = df_analytical['company_industries'].fillna('Unknown Industry')
    
    print(f"Master dataset merged successfully: {df_analytical.shape[0]:,} rows.")
    return df_analytical
