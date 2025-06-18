import pandas as pd

df = pd.read_csv('scientists.csv')

with open('birth_years.txt', 'w') as f:
	for value in df['birthyear'].values:
		f.write(f'{int(value)}\n')
