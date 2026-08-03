# Data Dictionary: LinkedIn Job Market Analytics

This document defines the schema of the final cleaned master dataset `linkedin_jobs_clean.csv` produced by the ETL pipeline.

---

## Columns Profile

| Column Name | Data Type | Description | Source & Transformation |
| :--- | :--- | :--- | :--- |
| `job_id` | `int64` | Unique identifier for each job posting. | `postings.csv` (Primary Key) |
| `job_title` | `object` | Title of the advertised job position. | `postings.csv` (`title` column) |
| `company_name` | `object` | Name of the hiring organization. | `companies.csv` (`name` column) |
| `job_description` | `object` | Full text detailing the job listing description. | `postings.csv` (`description` column) |
| `work_type` | `object` | Standardized employment type (e.g. Full-time, Contract, Part-time). | Normalized from `postings.csv` (`work_type`) |
| `location` | `object` | Clean location string as posted. | `postings.csv` (`location` column) |
| `listed_time` | `float64` | UNIX epoch timestamp indicating when the job was listed. | `postings.csv` (`original_listed_time`) |
| `application_type` | `object` | Method of applying (e.g. Easy Apply, Offsite). | `postings.csv` (`application_type`) |
| `sponsored` | `object` | Indicates whether the listing is sponsored. | `postings.csv` (`sponsored` $\rightarrow$ text labels) |
| `company_size_code` | `float64` | Coded categories for organization sizes (1 to 7). | `companies.csv` (`company_size`) |
| `employee_count` | `float64` | Latest recorded employee count for the company. | Enriched from `employee_counts.csv` using `idxmax()` |
| `follower_count` | `float64` | Latest recorded company follower count. | Enriched from `employee_counts.csv` using `idxmax()` |
| `benefits` | `object` | Comma-separated list of benefits (e.g. Medical, Dental). | Grouped and merged from `benefits.csv` |
| `skill_categories` | `object` | Comma-separated list of general skill categories. | Aggregated and mapped from `job_skills.csv` & `skills.csv` |
| `salary_min` | `float64` | Disclosed minimum salary as posted. | `postings.csv` (`min_salary` column) |
| `salary_max` | `float64` | Disclosed maximum salary as posted. | `postings.csv` (`max_salary` column) |
| `salary_median` | `float64` | Disclosed median salary if bounds are unavailable. | `postings.csv` (`med_salary` column) |
| `pay_period` | `object` | Frequency of salary payouts (HOURLY, MONTHLY, YEARLY). | `postings.csv` (`pay_period` column) |
| `currency` | `object` | Payout currency code (e.g. USD). | `postings.csv` (`currency` column) |
| `experience_level` | `object` | Standardized career levels (e.g. Entry level, Associate). | `postings.csv` (`formatted_experience_level`) |
| `company_industries` | `object` | Comma-separated list of industry classifications. | Grouped and merged from `company_industries.csv` |
| `company_specialities` | `object` | Comma-separated list of company core specialities. | Grouped and merged from `company_specialities.csv` |
| `salary_min_annual` | `float64` | Standardized annual minimum salary. | Derived: `salary_min` annualized by `pay_period` |
| `salary_max_annual` | `float64` | Standardized annual maximum salary. | Derived: `salary_max` annualized by `pay_period` |
| `salary_midpoint_annual`| `float64` | Annual salary midpoint used as proxy for analytics. | Derived: `(salary_min_annual + salary_max_annual) / 2` |
| `salary_available` | `int64` | Binary flag indicating if salary data is present (1 or 0).| Derived: `1` if midpoint is not null, else `0` |
| `city` | `object` | Extracted city name. | Parsed from `location` |
| `state` | `object` | Extracted state code/region name. | Parsed from `location` |
| `country` | `object` | Extracted country name. | Parsed from `location` |
| `req_python` | `int64` | Flag indicating if Python is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_sql` | `int64` | Flag indicating if SQL is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_excel` | `int64` | Flag indicating if Excel is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_aws` | `int64` | Flag indicating if AWS is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_tableau` | `int64` | Flag indicating if Tableau is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_powerbi` | `int64` | Flag indicating if Power BI is mentioned (1 or 0). | Regex matching on `job_description` |
| `req_java` | `int64` | Flag indicating if Java is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_spark` | `int64` | Flag indicating if Spark is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_git` | `int64` | Flag indicating if Git is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_scala` | `int64` | Flag indicating if Scala is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_cpp` | `int64` | Flag indicating if C++ is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `req_docker` | `int64` | Flag indicating if Docker is mentioned in text (1 or 0). | Regex matching on `job_description` |
| `tech_skills_count` | `int64` | Count of core technical tools required by this posting. | Derived: Sum of all technical skill flags |
