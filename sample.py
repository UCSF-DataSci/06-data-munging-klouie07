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
