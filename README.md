# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: 125718
- **Columns**: 5

### Column Details
| Column Name   | Data Type | Non-Null Count | Missing Values | Unique Values | Mean (with missing values removed) |
|---------------|-----------|----------------|----------------|---------------|------------------------------------|
| income_groups | object    | 119412         |  6306          | 8             |                                    |
| age           | float64   | 119495         |  6223          | 101           | 50.00703                           |
| gender        | float64   | 119811         |  5907          | 3             | 1.578578                           |
| year          | float64   | 119516         |  6202          | 169           | 2025.068                           |
| population    | float64   | 119378         |  6340          | 114925        | 1.137097e+08                       |

Duplicate rows: 2950

**EDA processing**
  ```
  import pandas as pd

  # Import data
  df = pd.read_csv('messy_population_data.csv')
  af = pd.read_csv('ddf--datapoints--population--by--income_groups--age--gender--year.csv')

  # Run EDA (Exploratory data analysis)
  df.head()
  df.info()
  df.describe()
  df.nunique()
  df.isna().sum()
  df.duplicated().sum()
  ```
During the data processing, it revealed 5 columns (income_groups, age, gender, year, population) with 125,718 columns. Columns were revealed to have approximately 5% missing data in each, with the number of unique values and means provided above. 

### Identified Issues

1. **Missing Data**
   - Description: Data missing from columns resulting in NaN values
   - Affected Column(s): income_groups, age, gender, year, population
   - Example: `df.value_counts()` shows `income_groups` has an `upper_middle_income
   - Potential Impact: Missing data can result in errors in analysis if the NaN is not removed. It also reduces usable data if those rows are removed. 

2. **Data Types**
   - Description: Data types are float
   - Affected Column(s): year, population
   - Example: `df.info()` reveals `Dtype` as 'float' for numerical values like year and population
   - Potential Impact: It's possible that these values were not meant to be float, given that they are whole numbers
   - NOTE: `gender` and `age` do not follow this pattern due to assigned variables

3. **Duplicate Values**
   - Description: Some rows were duplicated meaning entries appeared more than once
   - Affected Column(s): income_groups, age, gender, year, population
   - Example: `df.duplicated().sum()` reveals 2950 rows that appear more than once
   - Potential Impact: By having duplicate values, the analysis of the data could result in skewed points. This would not be as accurate. 

4. **Inconsistent Labeling**
   - Description: While it could be intentional, `gender` contained three unique values. In addition, columns in `income_groups` contained values ending with "_typo"
   - Affected Column(s): gender, income_group
   - Example: `df['income_groups'].unique()` reveals 'low_income' and 'low_income_typo' 
   - Potential Impact: Having additional groups within a column or inconsistent labeling for what is intended to be the same group, can result in data which is inaccurate when grouping by type. 

5. **Future-Year Values**
   - Description: Dates contained values past the current year 
   - Affected Column(s): year
   - Example: The maximum year in the data is 2115, with the mean of the non-null counts equaling 2025. 
   - Potential Impact: While this could be predictive, without the codebook or context, it's possible that this is a typo. Having future year values can also impact the analysis spread. 

## 2. Data Cleaning Process

### Issue 3: Duplicate Values
- **Cleaning Method**: Remove duplicate rows using `drop_duplicates()`
- **Implementation**:
  ```python
  df = df.drop_duplicates()
  ```
- **Justification**: To avoid data skewing for missing data. Also reduces the dataset size at the start, shortening code run time (esp. if it's a very large one)
- **Impact**: Rows affected: 2950. Duplicates deleted. 

### Issue 4: Inconsistent Labeling
- **Cleaning Method**: Convert gender unknown (3) to NaN and address variable names in `income_groups`
- **Implementation**:
  ```python
  df['gender'] = df['gender'].replace(3.0, np.nan)
  df['income_groups'] = df['income_groups'].replace({'high_income_typo': 'high_income', 'upper_middle_income_typo': 'upper_middle_income', 'lower_middle_income_typo': 'lower_middle_income', 'low_income_typo': 'low_income'})
  ```
- **Justification**: Standardizing the labeling and removing the _typo from the data set allows for better grouping. Removing the third group for gender as an unknown. 
- **Impact**: Rows affected: 5959

### Issue 5: Future-Year Values
- **Cleaning Method**: None
- **Implementation**:
  ```python
  df = df[df['year'] <= 2089]
  ```
- **Justification**: Because we do not know the context of the data, I initially was planning to try to remove the data after the current year. However, since the mean was already 2025, and a preliminary insight into how many values had years over 2024, it would have reduced the data over 50%, so I opted to leave the values as is. Upon returning to this question later, I reduced the year to 2089 (to maintain at least 90% of the data). 
- **Impact**: Rows affected: 8726

### Issue 1: Missing Data 
- **Cleaning Method**: Fill missing values with median or drop unknown values
- **Implementation**:
  ```python
  df['population'] = df['population'].fillna(df['population'].median())
  df['age'] = df['age'].fillna(df['age'].median())

  mean = df['year'].mean()
  std_dev = df['year'].std()
  num_missing = df['year'].isna().sum()
  random_values = np.random.normal(loc=mean, scale=std_dev, size=num_missing)
  df.loc[df['year'].isna(), 'year'] = random_values

  df['income_groups'] = df['income_groups'].dropna()
  df['gender'] = df['gender'].dropna()
  ```
- **Justification**: In order to retain as much data as possible, I planned to fill in the missing data before dropping the rows, although this can me more time intensive (especially for a larger dataset). However, to prevent skewing from the data in the median, I ended up dropping duplicates before filling in missing values. I opted to randomize the year before adding it back to the dataframe. The missing income and gender groups were then dropped. 
- **Impact**: Rows affected: 10,353

### Issue 2: Data Types
- **Cleaning Method**: None
- **Implementation**:
  ```python
  # None
  ```
- **Justification**: I opted to leave the code as is.
- **Impact**: Rows affected: None

## 3. Final State Analysis

### Dataset Overview
- **Name**: cleaned_population_data.csv 
- **Rows**: 108213
- **Columns**: 5

### Summary of Changes
- Dropped duplicates
- Adjusted missing values by substitution by median/curve or by dropping
- Standardized labeling for "income_groups"
- Result included an increase in age, approx. 50/50 distribution in gender, a lower mean and SD in year, and a slightly lower population count



