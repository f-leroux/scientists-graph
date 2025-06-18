import pandas as pd

# Load the matrix
matrix = pd.read_csv("person_reference_matrix.csv", index_col=0)

# Compute how often each person is linked TO (column sums)
linked_to_counts = matrix.sum(axis=0).sort_values(ascending=False)
print("Top most linked-to individuals:")
print(linked_to_counts.head(), '\n')

# Compute how often each person links OUT to others (row sums)
links_out_counts = matrix.sum(axis=1).sort_values(ascending=False)
print("Top individuals who link to others:")
print(links_out_counts.head(), '\n')

# Identify mutual references (A↔B)
mutual_links = (matrix & matrix.T)
mutual_counts = mutual_links.sum().sort_values(ascending=False)
print("Top individuals with the most mutual references:")
print(mutual_counts.head(), '\n')

# Print overall stats
total_links = matrix.values.sum()
num_people = matrix.shape[0]
density = total_links / (num_people * (num_people - 1))  # excluding diagonal
print(f"Total links: {total_links}")
print(f"Matrix density (non-diagonal): {density:.4f}")

