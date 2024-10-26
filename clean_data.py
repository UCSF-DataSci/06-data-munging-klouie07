import pandas as pd
import numpy as np

def clean_data(input_file, output_file):
    # Load dataset
    df = pd.read_csv(input_file)

    # Issue 3: Drop duplicates
    df = df.drop_duplicates()

    # Issue 4: Standardize labeling
    df['gender'] = df['gender'].replace(3.0, np.nan)
    df['income_groups'] = df['income_groups'].str.strip().str.lower()
    df['income_groups'] = df['income_groups'].replace({'high_income_typo': 'high_income', 
                                                       'upper_middle_income_typo': 'upper_middle_income', 
                                                       'lower_middle_income_typo': 'lower_middle_income', 
                                                       'low_income_typo': 'low_income'})

    # Issue 5: Delete year values
    df = df[df['year'] <= 2089]
    
    # Issue 1: Missing values
    df['population'] = df['population'].fillna(df['population'].median())
    df['age'] = df['age'].fillna(df['age'].median())

    mean = df['year'].mean()
    std_dev = df['year'].std()
    num_missing = df['year'].isna().sum()
    random_values = np.random.normal(loc=mean, scale=std_dev, size=num_missing)
    df.loc[df['year'].isna(), 'year'] = random_values

    df['income_groups'] = df['income_groups'].dropna()
    df['gender'] = df['gender'].dropna()

    # Issue 2: Data types
    # No actions taken to convert float to (int) or (num)

    # Save cleaned dataset
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    clean_data('messy_population_data.csv', 'cleaned_population_data.csv')

