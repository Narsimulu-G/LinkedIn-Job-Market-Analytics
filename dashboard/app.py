import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src import config

# ----------------- CONFIGURATION & SETUP -----------------
st.set_page_config(
    page_title="LinkedIn Job Market Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #1f77b4;
    }
    .educational-box {
        background-color: #e3f2fd;
        border-left: 5px solid #0d47a1;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADER (CACHED) -----------------
@st.cache_data
def load_clean_data():
    csv_path = config.PROCESSED_CSV_PATH
    if not os.path.exists(csv_path):
        # Fallback to direct current directory check just in case
        csv_path = "data/processed/linkedin_jobs_clean.csv"
        
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        # Parse list fields
        df['tech_skills_count'] = df['tech_skills_count'].fillna(0).astype(int)
        return df
    else:
        return None

df_raw = load_clean_data()

if df_raw is None:
    st.error("❌ Processed dataset not found! Please run the ETL pipeline first using the command: `python -m src.pipeline`")
    st.stop()

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.title("🔍 Global Filters")

# Educational Mode Toggle
educational_mode = st.sidebar.toggle("📘 Learn Analytics Mode", value=True, help="Enable this to see step-by-step Pandas code explanations for every chart and KPI.")

st.sidebar.divider()

# Location Filter
countries = ['All'] + sorted(df_raw['country'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Country", options=countries)

if selected_country != 'All':
    df_filtered = df_raw[df_raw['country'] == selected_country]
    states = ['All'] + sorted(df_filtered['state'].dropna().unique().tolist())
    selected_state = st.sidebar.selectbox("State / Region", options=states)
else:
    df_filtered = df_raw.copy()
    selected_state = 'All'

if selected_state != 'All':
    df_filtered = df_filtered[df_filtered['state'] == selected_state]

# Work Type Filter
work_types = ['All'] + sorted(df_raw['work_type'].dropna().unique().tolist())
selected_work_type = st.sidebar.selectbox("Work Type", options=work_types)
if selected_work_type != 'All':
    df_filtered = df_filtered[df_filtered['work_type'] == selected_work_type]

# Experience Level Filter
exp_levels = ['All'] + sorted(df_raw['experience_level'].dropna().unique().tolist())
selected_exp = st.sidebar.selectbox("Experience Level", options=exp_levels)
if selected_exp != 'All':
    df_filtered = df_filtered[df_filtered['experience_level'] == selected_exp]

# Company Size Filter
sizes = ['All'] + sorted(df_raw['company_size_code'].dropna().unique().tolist())
selected_size = st.sidebar.selectbox("Company Size Code", options=sizes)
if selected_size != 'All':
    df_filtered = df_filtered[df_filtered['company_size_code'] == selected_size]

# Sponsored Filter
sponsored_options = ['All', 'Sponsored', 'Non-Sponsored']
selected_sponsored = st.sidebar.selectbox("Sponsorship", options=sponsored_options)
if selected_sponsored == 'Sponsored':
    df_filtered = df_filtered[df_filtered['sponsored'] == 'Sponsored']
elif selected_sponsored == 'Non-Sponsored':
    df_filtered = df_filtered[df_filtered['sponsored'] == 'Non-Sponsored']

# Salary Available Filter
salary_options = ['All', 'Salary Available', 'No Salary Data']
selected_salary_avail = st.sidebar.selectbox("Salary Info", options=salary_options)
if selected_salary_avail == 'Salary Available':
    df_filtered = df_filtered[df_filtered['salary_available'] == 1]
elif selected_salary_avail == 'No Salary Data':
    df_filtered = df_filtered[df_filtered['salary_available'] == 0]

# ----------------- MAIN APP PAGES -----------------
menu = ["Home & Overview", "Job Market Trends", "Skills Analysis", "Salary Insights", "Company & Industry Profile", "Dataset Explorer"]
page = st.selectbox("📂 Select Analytics Dashboard Page", menu)

# Helper function to show Educational explanations
def show_edu_box(what, why, how, result):
    if educational_mode:
        with st.expander("📘 Pandas Code Explanation (Learn Analytics)", expanded=False):
            st.markdown(f"""
            <div class="educational-box">
            <b>🔍 What are we calculating?</b><br>{what}<br><br>
            <b>💡 Why is this useful?</b><br>{why}<br><br>
            <b>💻 How is it calculated in Python/Pandas?</b><br><code>{how}</code><br><br>
            <b>📈 Result Insight:</b><br>{result}
            </div>
            """, unsafe_allow_html=True)

# ----------------- PAGE 1: HOME & OVERVIEW -----------------
if page == "Home & Overview":
    st.title("💼 LinkedIn Job Market Overview (2023)")
    st.write("Welcome to the LinkedIn Job Market Analytics Dashboard. This portal summarizes insights from 123,849 job postings.")
    
    # KPI metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_jobs = len(df_filtered)
    total_companies = df_filtered['company_name'].nunique()
    salary_rate = (df_filtered['salary_available'].sum() / total_jobs) * 100 if total_jobs > 0 else 0
    sponsored_rate = (df_filtered[df_filtered['sponsored'] == 'Sponsored'].shape[0] / total_jobs) * 100 if total_jobs > 0 else 0
    unique_locations = df_filtered['location'].nunique()
    
    col1.metric("Total Jobs", f"{total_jobs:,}")
    col2.metric("Unique Companies", f"{total_companies:,}")
    col3.metric("Locations", f"{unique_locations:,}")
    col4.metric("Salary Disclosure", f"{salary_rate:.1f}%")
    col5.metric("Sponsored Listings", f"{sponsored_rate:.1f}%")
    
    show_edu_box(
        "Headline statistics: Counts of job postings, unique companies, unique locations, and disclosure ratios.",
        "To get an immediate grasp of the size, diversity, and data completeness of the current job market snapshot.",
        "Total Jobs: len(df)\nUnique Companies: df['company_name'].nunique()\nSalary Disclosure: (df['salary_available'].sum() / len(df)) * 100",
        f"The selected filters yield {total_jobs:,} active postings from {total_companies:,} unique companies."
    )
    
    st.divider()
    
    # Main Charts Grid
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📌 Top 10 Job Titles")
        top_titles = df_filtered['job_title'].value_counts().head(10).reset_index()
        fig_titles = px.bar(top_titles, x='count', y='job_title', orientation='h', 
                            title="Top 10 Job Titles by Posting Volume",
                            labels={'count': 'Number of Postings', 'job_title': 'Job Title'},
                            color_discrete_sequence=['#1f77b4'])
        fig_titles.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_titles, use_container_width=True)
        
        show_edu_box(
            "Ranking of the most frequently occurring job titles.",
            "Helps identify which job roles are in highest demand in the market right now.",
            "df['job_title'].value_counts().head(10)",
            f"The most posted job title is '{top_titles.iloc[0]['job_title']}' with {top_titles.iloc[0]['count']:,} listings."
        )
        
    with col_right:
        st.subheader("🏢 Top Companies Posting Jobs")
        top_companies = df_filtered[df_filtered['company_name'] != 'Unknown Company']['company_name'].value_counts().head(10).reset_index()
        fig_companies = px.bar(top_companies, x='count', y='company_name', orientation='h',
                               title="Top 10 Hiring Companies",
                               labels={'count': 'Number of Postings', 'company_name': 'Company Name'},
                               color_discrete_sequence=['#2ca02c'])
        fig_companies.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_companies, use_container_width=True)
        
        show_edu_box(
            "Ranking of companies by the count of their postings.",
            "Identifies the most active recruiters/employers on LinkedIn.",
            "df['company_name'].value_counts().head(10)",
            f"The leading company is '{top_companies.iloc[0]['company_name']}' with {top_companies.iloc[0]['count']:,} postings."
        )

# ----------------- PAGE 2: JOB MARKET TRENDS -----------------
elif page == "Job Market Trends":
    st.title("📈 Job Market Trends & Demographics")
    
    col_w, col_e = st.columns(2)
    
    with col_w:
        st.subheader("💼 Employment Types (Work Types)")
        work_counts = df_filtered['work_type'].value_counts().reset_index()
        fig_work = px.pie(work_counts, values='count', names='work_type', hole=0.4,
                          title="Work Type Distribution",
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_work, use_container_width=True)
        
        show_edu_box(
            "A pie breakdown showing the ratio of full-time, contract, part-time, and internship jobs.",
            "Informs whether the market favors long-term employment, freelance contracts, or entry opportunities.",
            "df['work_type'].value_counts()",
            f"Full-time listings represent the vast majority of positions ({work_counts.iloc[0]['count']:,} postings)."
        )
        
    with col_e:
        st.subheader("🎓 Required Experience Levels")
        exp_counts = df_filtered['experience_level'].value_counts().reset_index()
        fig_exp = px.bar(exp_counts, x='experience_level', y='count',
                         title="Postings by Experience Level",
                         labels={'experience_level': 'Experience Level', 'count': 'Number of Postings'},
                         color_discrete_sequence=['#ff7f0e'])
        st.plotly_chart(fig_exp, use_container_width=True)
        
        show_edu_box(
            "A bar chart representing required career levels (Entry, Associate, Mid-Senior, Executive, etc.).",
            "Indicates what experience cohorts are targeted by hiring managers.",
            "df['experience_level'].value_counts()",
            f"The experience level in highest demand is '{exp_counts.iloc[0]['experience_level']}' ({exp_counts.iloc[0]['count']:,} postings)."
        )

# ----------------- PAGE 3: SKILLS ANALYSIS -----------------
elif page == "Skills Analysis":
    st.title("🛠️ Technical Skills Demand & Search")
    st.write("We extracted technical tools and skills directly from job descriptions to analyze technical tooling requirements.")
    
    # 1. Total Skills Ranking
    st.subheader("📊 Most Demanded Technical Tools & Languages")
    
    # Filter list of flag columns
    skill_cols = [f"req_{s.lower().replace('+', 'p')}" for s in config.TECH_SKILLS_LIST]
    # Sum columns to get counts
    skill_sums = df_filtered[skill_cols].sum().sort_values(ascending=False).reset_index()
    skill_sums.columns = ['skill_column', 'count']
    # Map back to readable name
    name_map = {f"req_{s.lower().replace('+', 'p')}": s for s in config.TECH_SKILLS_LIST}
    skill_sums['Skill'] = skill_sums['skill_column'].map(name_map)
    
    fig_skills = px.barplot(skill_sums, x='Skill', y='count',
                            title="Core Technical Skills Required by Volume",
                            labels={'count': 'Number of Postings', 'Skill': 'Skill/Tool'},
                            color='count', color_continuous_scale='Blues')
    st.plotly_chart(fig_skills, use_container_width=True)
    
    show_edu_box(
        "Frequency count of keyword flag columns extracted from job descriptions.",
        "Pinpoints which technical skills (e.g. Python, SQL, AWS) give candidates the highest market leverage.",
        "df[[req_python, req_sql, ...]].sum().sort_values(ascending=False)",
        f"The top technical skill demanded is '{skill_sums.iloc[0]['Skill']}' appearing in {skill_sums.iloc[0]['count']:,} job descriptions."
    )
    
    st.divider()
    
    # 2. Skill Search Slicer
    st.subheader("🔍 Deep-Dive: Search Individual Skill")
    search_skill = st.selectbox("Select a technical tool to filter details:", config.TECH_SKILLS_LIST)
    
    col_name = f"req_{search_skill.lower().replace('+', 'p')}"
    jobs_with_skill = df_filtered[df_filtered[col_name] == 1]
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write(f"💼 **Total job postings requiring {search_skill}:** `{len(jobs_with_skill):,}`")
        st.write(f"📈 **Market Share:** `{((len(jobs_with_skill) / len(df_filtered)) * 100):.2f}%` of postings in this subset.")
        
        # Top Job Titles requiring this
        st.write(f"**Top Job Titles Requiring {search_skill}:**")
        st.dataframe(jobs_with_skill['job_title'].value_counts().head(5).reset_index().rename(columns={'count': 'Job Postings'}))
        
    with col_s2:
        # Top Industries requiring this
        st.write(f"**Top Company Industries Requiring {search_skill}:**")
        st.dataframe(jobs_with_skill['company_industries'].value_counts().head(5).reset_index().rename(columns={'count': 'Job Postings'}))

# ----------------- PAGE 4: SALARY INSIGHTS -----------------
elif page == "Salary Insights":
    st.title("💲 Compensation & Salary Analytics")
    
    df_salary = df_filtered[df_filtered['salary_available'] == 1]
    
    if len(df_salary) == 0:
        st.warning("⚠️ No listings with salary details are available in this filtered subset. Please expand your filters (e.g., select 'All' countries) to view salary insights.")
    else:
        st.write(f"Analysis based on `{len(df_salary):,}` job postings with disclosed salary information.")
        
        # 1. Salary Distribution Histogram
        st.subheader("📊 Annual Salary Distribution")
        fig_sal_dist = px.histogram(df_salary, x='salary_midpoint_annual', nbins=50,
                                    title="Annual Salary Distribution Histogram (Midpoints)",
                                    labels={'salary_midpoint_annual': 'Annual Salary ($USD)', 'count': 'Number of Postings'},
                                    color_discrete_sequence=['#9467bd'], marginal="box")
        st.plotly_chart(fig_sal_dist, use_container_width=True)
        
        show_edu_box(
            "Histogram showing the frequency distribution of annualized job salary midpoints.",
            "Displays the market salary curve, revealing whether salaries are skewed and where the typical salary range sits.",
            "px.histogram(df[df['salary_available'] == 1], x='salary_midpoint_annual')",
            f"The median annual salary is ${df_salary['salary_midpoint_annual'].median():,.2f} USD."
        )
        
        st.divider()
        
        # 2. Box plots of salary by experience
        st.subheader("📈 Annual Salary by Experience Level")
        # Sort levels logically
        level_order = ['Internship', 'Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive', 'Not Specified']
        available_levels = [l for l in level_order if l in df_salary['experience_level'].unique()]
        
        fig_sal_box = px.box(df_salary, x='salary_midpoint_annual', y='experience_level',
                             category_orders={'experience_level': available_levels},
                             title="Salary Distribution Boxplots by Experience Level",
                             labels={'salary_midpoint_annual': 'Annual Salary ($USD)', 'experience_level': 'Experience Level'},
                             color='experience_level', color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig_sal_box, use_container_width=True)
        
        show_edu_box(
            "Boxplots displaying the minimum, maximum, median, and quartiles of salaries grouped by career level.",
            "Evaluates compensation scaling as seniority increases and quantifies salary dispersion.",
            "px.box(df, x='salary_midpoint_annual', y='experience_level')",
            "Box widths represent pay ranges. Executive roles show the highest median pay and dispersion."
        )

# ----------------- PAGE 5: COMPANY & INDUSTRY PROFILE -----------------
elif page == "Company & Industry Profile":
    st.title("🏢 Organization Sizes & Industries")
    
    col_c, col_i = st.columns(2)
    
    with col_c:
        st.subheader("📏 Distribution of Recruiter Company Sizes")
        # Map size codes to description
        size_counts = df_filtered['company_size_code'].value_counts().reset_index()
        fig_size = px.bar(size_counts, x='company_size_code', y='count',
                          title="Hiring Activity by Company Size Category",
                          labels={'company_size_code': 'Company Size Code (1=Smallest, 7=Largest)', 'count': 'Number of Postings'},
                          color_discrete_sequence=['#e377c2'])
        st.plotly_chart(fig_size, use_container_width=True)
        
        show_edu_box(
            "Distribution of postings across company size category codes.",
            "Shows whether hiring is dominated by massive enterprises (6-7) or small-to-medium businesses (1-3).",
            "df['company_size_code'].value_counts()",
            f"The category with the most job postings is Size Code '{size_counts.iloc[0]['company_size_code']}'."
        )
        
    with col_i:
        st.subheader("🏭 Leading Hiring Industries")
        # Split aggregated industry strings if multiple
        top_inds = df_filtered[df_filtered['company_industries'] != 'Unknown Industry']['company_industries'].value_counts().head(10).reset_index()
        fig_inds = px.bar(top_inds, x='count', y='company_industries', orientation='h',
                          title="Top 10 Active Industries",
                          labels={'count': 'Number of Postings', 'company_industries': 'Industry'},
                          color_discrete_sequence=['#bcbd22'])
        fig_inds.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_inds, use_container_width=True)
        
        show_edu_box(
            "Top active sectors posting jobs on LinkedIn.",
            "Pinpoints the healthiest hiring sectors for job seekers.",
            "df['company_industries'].value_counts().head(10)",
            f"The top industry sector is '{top_inds.iloc[0]['company_industries']}'."
        )

# ----------------- PAGE 6: DATASET EXPLORER -----------------
else:
    st.title("🗄️ Interactive Dataset Explorer")
    st.write("Browse, search, and filter the processed analytical dataset.")
    
    # Text Search Filter
    search_query = st.text_input("🔍 Search Job Title or Company Name:")
    df_search = df_filtered.copy()
    if search_query:
        df_search = df_search[
            df_search['job_title'].str.contains(search_query, case=False, na=False) |
            df_search['company_name'].str.contains(search_query, case=False, na=False)
        ]
        
    st.write(f"Showing `{min(100, len(df_search))}` rows of `{len(df_search):,}` matching postings:")
    st.dataframe(df_search[['job_title', 'company_name', 'location', 'work_type', 'experience_level', 'salary_midpoint_annual']].head(100))
    
    # Explanatory insights box (Section 31 of PRD)
    st.divider()
    st.subheader("💡 Automated Data Insights")
    
    # Calculate values dynamically
    median_val = df_raw['salary_midpoint_annual'].median()
    top_skill = skill_sums.iloc[0]['Skill'] if len(skill_sums) > 0 else "N/A"
    ft_pct = (df_raw[df_raw['work_type'] == 'Full-time'].shape[0] / len(df_raw)) * 100
    
    st.info(f"""
    *   **Insight 1**: **Full-time positions** represent the largest employment category in the dataset, accounting for **{ft_pct:.1f}%** of all listings.
    *   **Insight 2**: **{top_skill}** is the most frequently requested technical skill flag in the job description texts.
    *   **Insight 3**: Salary details are available for **{salary_rate:.1f}%** of postings in this filtered views subset. The median annual pay overall is **${median_val:,.2f} USD**. Keep in mind that salary comparisons should be interpreted within this specific disclosed subset.
    """)
