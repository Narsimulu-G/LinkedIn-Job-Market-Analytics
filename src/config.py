import os

# 1. Base Project Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")
TABLES_DIR = os.path.join(OUTPUT_DIR, "tables")

# Cleaned dataset filename
PROCESSED_CSV_NAME = "linkedin_jobs_clean.csv"
PROCESSED_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, PROCESSED_CSV_NAME)

# 2. Analysis Settings
TOP_N = 10

# Tech skills keyword list to extract from job descriptions
TECH_SKILLS_LIST = [
    'Python', 'SQL', 'Excel', 'AWS', 'Tableau', 
    'Power BI', 'Java', 'Spark', 'Git', 'Scala', 
    'C++', 'Docker', 'Hadoop', 'Kubernetes', 'Linux'
]

# Work type categories normalization mapping
WORK_TYPE_MAP = {
    'FULL_TIME': 'Full-time',
    'CONTRACT': 'Contract',
    'PART_TIME': 'Part-time',
    'TEMPORARY': 'Temporary',
    'INTERNSHIP': 'Internship',
    'VOLUNTEER': 'Volunteer',
    'OTHER': 'Other'
}

# 3. Create folders if they don't exist
for folder in [RAW_DATA_DIR, PROCESSED_DATA_DIR, CHARTS_DIR, REPORTS_DIR, TABLES_DIR]:
    os.makedirs(folder, exist_ok=True)
