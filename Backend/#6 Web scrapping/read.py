import pandas as pd

df = pd.read_csv('courses.csv', index_col=0, sep=';')

print(df.head())


print(df.columns)
