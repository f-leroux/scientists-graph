import pandas as pd

# === Load the CSV file ===
file_path = "person_2020_update.csv"  # Replace with your actual path
df = pd.read_csv(file_path, sep=',')  # or use ',' if it's comma-separated

# === Define the occupations you're interested in ===
target_occupations = ['BIOLOGIST', 'MATHEMATICIAN', 'PHYSICIAN', 'PHYSICIST', 'ASTRONOMER', 'CHEMIST', 'INVENTOR', 'ENGINEER', 'COMPUTER SCIENTIST', 'GEOLOGIST', 'GEOGRAPHER', 'STATISTICIAN']

# === Filter by occupation ===
filtered_df = df[df['occupation'].isin(target_occupations)]

# === Sort by HPI descending and keep top N ===
n = 500
top_df = filtered_df.sort_values(by='hpi', ascending=False).head(n)

# === Extract the 'slug' column into a list ===
slug_list = top_df['slug'].tolist()

# === Save the list to a file ===
with open("top_slugs.txt", "w") as f:
    for slug in slug_list:
        f.write(f"{slug}\n")

# === Optional: Print the result ===
print("Top slugs:", slug_list)

