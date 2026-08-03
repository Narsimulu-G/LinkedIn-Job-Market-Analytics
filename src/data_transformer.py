import pandas as pd

def aggregate_benefits(df_benefits):
    """
    Groups benefits by job_id and joins them as a comma-separated string.
    e.g. Medical, Dental, Vision
    """
    df = df_benefits.copy()
    if 'inferred' in df.columns:
        df = df.drop(columns=['inferred'])
        
    print("Aggregating job benefits by job_id...")
    df_agg = df.groupby('job_id')['type'].agg(lambda x: ', '.join(x.dropna().unique())).reset_index()
    df_agg.rename(columns={'type': 'job_benefits'}, inplace=True)
    return df_agg

def aggregate_skills(df_skills_raw, df_skills_map):
    """
    Merges job skills with their full mappings and aggregates them.
    e.g. Information Technology, Engineering
    """
    print("Mapping skills abbreviations and aggregating...")
    df_named = df_skills_raw.merge(df_skills_map, on='skill_abr', how='left')
    df_agg = df_named.groupby('job_id')['skill_name'].agg(lambda x: ', '.join(x.dropna().unique())).reset_index()
    df_agg.rename(columns={'skill_name': 'skill_categories'}, inplace=True)
    return df_agg

def process_employee_counts(df_emp_counts):
    """
    Finds the latest recorded employee counts for each company using the idxmax() method.
    Fixes the bug in the original notebook which dropped employee count.
    """
    print("Selecting latest employee and follower counts for each company...")
    # Find row index of the maximum time_recorded per company_id
    latest_indices = df_emp_counts.groupby('company_id')['time_recorded'].idxmax()
    df_latest = df_emp_counts.loc[latest_indices].reset_index(drop=True)
    return df_latest

def aggregate_company_industries(df_comp_ind):
    """Groups company industries into a comma-separated list."""
    print("Aggregating company industries...")
    df_agg = df_comp_ind.groupby('company_id')['industry'].agg(lambda x: ', '.join(x.dropna().unique())).reset_index()
    df_agg.rename(columns={'industry': 'company_industries'}, inplace=True)
    return df_agg

def aggregate_company_specialities(df_comp_spec):
    """Groups company specialities into a comma-separated list."""
    print("Aggregating company specialities...")
    df_agg = df_comp_spec.groupby('company_id')['speciality'].agg(lambda x: ', '.join(x.dropna().unique())).reset_index()
    df_agg.rename(columns={'speciality': 'company_specialities'}, inplace=True)
    return df_agg
