import pandas as pd 


df = pd.read_csv('master_companies.csv')
df = df.head()
df.to_csv('master_companies.csv', index=False)
print(df)