import os
import shutil
from src import config

SOURCE_DIR = r"C:\Users\naras\Downloads\archive"

# Map source file relative paths to local target relative paths under data/raw
DATA_MAPPING = {
    "postings.csv": "job_postings.csv",
    "jobs/benefits.csv": "job_details/benefits.csv",
    "jobs/job_skills.csv": "job_details/job_skills.csv",
    "jobs/job_industries.csv": "job_details/job_industries.csv",
    "jobs/salaries.csv": "job_details/salaries.csv",
    "companies/companies.csv": "company_details/companies.csv",
    "companies/company_industries.csv": "company_details/company_industries.csv",
    "companies/company_specialities.csv": "company_details/company_specialities.csv",
    "companies/employee_counts.csv": "company_details/employee_counts.csv",
    "mappings/industries.csv": "mappings/industries.csv",
    "mappings/skills.csv": "mappings/skills.csv"
}

def setup_directories_and_files():
    print("Setting up local directory structure...")
    # Ensure config initializes paths
    raw_dir = config.RAW_DATA_DIR
    
    # Subdirectories to create inside data/raw
    subdirs = ["job_details", "company_details", "mappings"]
    for sdir in subdirs:
        os.makedirs(os.path.join(raw_dir, sdir), exist_ok=True)
        
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Source directory {SOURCE_DIR} does not exist.")
        print("Please ensure your Kaggle dataset is unzipped at: C:\\Users\\naras\\Downloads\\archive")
        return False
        
    print(f"Copying files from {SOURCE_DIR} to {raw_dir}...")
    copied_count = 0
    for src_rel, dest_rel in DATA_MAPPING.items():
        src_path = os.path.join(SOURCE_DIR, src_rel.replace("/", os.sep))
        dest_path = os.path.join(raw_dir, dest_rel.replace("/", os.sep))
        
        if os.path.exists(src_path):
            # Create subfolder of dest_path if not existing
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            print(f"  - Copying: {src_rel} -> {dest_rel}")
            shutil.copy(src_path, dest_path)
            copied_count += 1
        else:
            print(f"  - Warning: Missing source file {src_path}")
            
    print(f"\nCompleted copying {copied_count} files.")
    return copied_count > 0

if __name__ == "__main__":
    setup_directories_and_files()
