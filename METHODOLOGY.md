# Analytics Methodology: LinkedIn Job Market Analytics

This document details the data analytical methodology and technical transformation steps implemented in the data pipeline.

---

## 1. Data Cleaning & Validation
*   **Deduplication**: We run standard duplicate checks on the primary identifier `job_id`. Duplicated records are dropped keeping the first instance to avoid artificial inflation of volume metrics.
*   **Handling Nulls**: Instead of running blanket row removals (`.dropna()`) which severely degrades the volume of analyzable parameters, missing categorical values (like company names, job benefits, skill categories, and industries) are filled with a default label like `"Unknown"` or `"Not Specified"`. This preserves job postings that are still valuable for geographic and skill-based analysis.

---

## 2. Multi-Table Aggregation
*   **One-to-Many Mappings**: Job benefits and job skills abbreviations are aggregated using group concatenation. This collapses multiple details rows into a single, clean comma-separated list linked to a single `job_id`.
*   **Latest Employee Records Selection**: The company employee counts are tracked historical-log-style. To represent the company size accurately, we identify the maximum timestamp (`time_recorded`) per company using:
    `latest_indices = df_emp_counts.groupby('company_id')['time_recorded'].idxmax()`
    and subsetting the counts dataset to merge the latest headcount profile.

---

## 3. Feature Engineering & Enrichment

### A. Salary Annualization
To make wages comparable, we calculate annualized salaries based on reported pay periods:
$$\text{Annualized Minimum Salary} = \text{min\_salary} \times N$$
where:
*   $N = 2080$ for `HOURLY` pay (40 hours/week $\times$ 52 weeks)
*   $N = 12$ for `MONTHLY` pay
*   $N = 52$ for `WEEKLY` pay
*   $N = 260$ for `DAILY` pay
*   $N = 1$ for `YEARLY` pay

### B. Location Parsing
Geographic addresses are split by commas to extract standard administrative values:
$$\text{"City, State, Country" or "City, State"}$$
When the country is omitted but a two-letter state code is present (e.g. `CA`, `TX`), the country is inferred as `United States`.

### C. Technical Skills Text Matching
Since `job_skills.csv` only lists high-level categories (like `Information Technology`, `Engineering`), we search the full text of `job_description` using regular expressions. We use strict word boundaries:
$$\text{Regex Pattern} = \text{r'\b' + re.escape(Skill) + r'\b'}$$
This flags whether specific tools (e.g. `Python`, `SQL`, `AWS`, `Excel`, `Tableau`) are required.

---

## 4. Visual Analysis & Slicers
*   **Volume Distribution**: Visualized using frequency bar charts and pie breakdowns.
*   **Wage Ranges**: Analyzed using Box plots (revealing median pay, quartiles, and salary dispersion) and histograms.
*   **Global Cross-filtering**: Slicers allow users to interactively subset the dataset, updating KPIs and visualizations dynamically.
