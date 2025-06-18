import pandas as pd

# Step 1: Load the list of slugs from top_slugs.txt
with open('top_slugs.txt', 'r') as f:
    top_slugs = {line.strip() for line in f if line.strip()}

# Step 2: Load the CSV file
df = pd.read_csv('person_2020_update.csv', sep=',')  # Use sep=',' if your CSV is comma-separated

# Step 3: Filter rows where slug is in top_slugs
filtered_df = df[df['slug'].isin(top_slugs)]

# Step 4: Write filtered rows to a new CSV
filtered_df.to_csv('scientists.csv', index=False)

