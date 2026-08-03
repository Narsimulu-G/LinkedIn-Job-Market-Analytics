import pandas as pd
import numpy as np
from src.data_cleaner import clean_job_postings

def test_clean_job_postings():
    # Create a mock dataframe
    data = {
        'job_id': [1, 2, 2],  # ID 2 is duplicated
        'work_type': ['FULL_TIME', 'CONTRACT', 'CONTRACT'],
        'formatted_experience_level': ['Entry level', None, 'Associate'],
        'sponsored': [0, 1, 1]
    }
    df = pd.DataFrame(data)
    
    # Run cleaner
    df_clean = clean_job_postings(df)
    
    # Assert duplicates are dropped
    assert len(df_clean) == 2
    assert df_clean['job_id'].tolist() == [1, 2]
    
    # Assert work type is standardized
    assert df_clean['work_type_clean'].tolist() == ['Full-time', 'Contract']
    
    # Assert experience level nulls are handled
    assert df_clean['experience_level_clean'].tolist() == ['Entry level', 'Not Specified']
    
    # Assert sponsored string conversion
    assert df_clean['sponsored_clean'].tolist() == ['Non-Sponsored', 'Sponsored']
