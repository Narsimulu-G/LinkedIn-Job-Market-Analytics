import os
import time
from src import config
from src import data_loader
from src import data_cleaner
from src import data_transformer
from src import data_merger
from src import feature_engineering

def run_etl_pipeline():
    start_time = time.time()
    print("==================================================================")
    print("        LINKEDIN JOB MARKET ANALYTICS ETL PIPELINE STARTED        ")
    print("==================================================================")
    
    # 1. LOAD RAW DATA
    print("\n--- Phase 1: Data Ingestion ---")
    df_postings_raw = data_loader.load_job_postings()
    df_benefits_raw = data_loader.load_benefits()
    df_skills_raw = data_loader.load_job_skills()
    df_companies_raw = data_loader.load_companies()
    df_comp_ind_raw = data_loader.load_company_industries()
    df_comp_spec_raw = data_loader.load_company_specialities()
    df_emp_counts_raw = data_loader.load_employee_counts()
    df_skills_map = data_loader.load_skill_mappings()
    
    # 2. DATA CLEANING
    print("\n--- Phase 2: Data Cleaning ---")
    df_postings_clean = data_cleaner.clean_job_postings(df_postings_raw)
    
    # 3. DATA TRANSFORMATION (AGGREGATION)
    print("\n--- Phase 3: Aggregation & Mapping ---")
    df_benefits_agg = data_transformer.aggregate_benefits(df_benefits_raw)
    df_skills_agg = data_transformer.aggregate_skills(df_skills_raw, df_skills_map)
    df_emp_counts_latest = data_transformer.process_employee_counts(df_emp_counts_raw)
    df_comp_ind_agg = data_transformer.aggregate_company_industries(df_comp_ind_raw)
    df_comp_spec_agg = data_transformer.aggregate_company_specialities(df_comp_spec_raw)
    
    # 4. DATA INTEGRATION (MERGING)
    print("\n--- Phase 4: Data Integration ---")
    df_merged = data_merger.merge_all_datasets(
        df_postings_clean,
        df_benefits_agg,
        df_skills_agg,
        df_companies_raw,  # We merge raw companies, enriched with other aggregated frames inside data_merger
        df_comp_ind_agg,
        df_comp_spec_agg,
        df_emp_counts_latest
    )
    
    # 5. FEATURE ENGINEERING
    print("\n--- Phase 5: Feature Engineering ---")
    df_final = feature_engineering.run_feature_engineering(df_merged)
    
    # 6. EXPORT PROCESSED DATA
    print("\n--- Phase 6: Output Export ---")
    os.makedirs(config.PROCESSED_DATA_DIR, exist_ok=True)
    df_final.to_csv(config.PROCESSED_CSV_PATH, index=False)
    
    elapsed = time.time() - start_time
    print("\n" + "="*66)
    print("        ETL PIPELINE COMPLETED SUCCESSFULLY!        ")
    print("="*66)
    print(f"  - Final clean dataset shape: {df_final.shape[0]:,} rows, {df_final.shape[1]} columns")
    print(f"  - Saved to: {config.PROCESSED_CSV_PATH}")
    print(f"  - Execution time: {elapsed:.2f} seconds")
    print("="*66)
    
    return True

if __name__ == "__main__":
    run_etl_pipeline()
