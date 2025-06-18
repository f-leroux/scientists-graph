import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Load list of slugs
with open("top_slugs.txt") as f:
    slugs = [line.strip() for line in f.readlines()]

# Initialize matrix
n = len(slugs)
slug_set = set(slugs)
link_matrix = pd.DataFrame(0, index=slugs, columns=slugs)

# Wikipedia base URL
base_url = "https://en.wikipedia.org/wiki/"

# Sections to exclude
excluded_sections = ["See also", "References", "Sources", "Further reading", "External links"]

def remove_after_first_excluded_section(content, excluded_sections):
    """Remove everything after the first encountered excluded section."""
    # Find all section headers
    headers = content.find_all(['h2', 'h3'])
    
    for header in headers:
        section_title = header.get_text().strip()
        
        if section_title in excluded_sections:
            # Found the first excluded section - remove this header and everything after it
            elements_to_remove = []
            
            # Get all elements that come after this header in the document
            for element in header.find_all_next():
                elements_to_remove.append(element)
            
            # Also remove the header itself
            elements_to_remove.append(header)
            
            # Remove all collected elements
            for element in elements_to_remove:
                if element and element.parent:
                    element.extract()
            
            break  # Stop after finding the first excluded section

# Loop through each person's Wikipedia page
for source_slug in slugs:
    print(f"Processing: {source_slug}")
    try:
        url = base_url + source_slug
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main content div
        content = soup.find('div', {'id': 'mw-content-text'})
        if not content:
            continue

        # Remove everything after first excluded section
        remove_after_first_excluded_section(content, excluded_sections)
        
        # Now find all remaining links
        links = content.find_all('a', href=True)
        linked_slugs = set(
            link['href'].split('/wiki/')[-1].split('#')[0]
            for link in links
            if link['href'].startswith('/wiki/') and ':' not in link['href']
        )

        # Check if any link matches a target slug
        for target_slug in slugs:
            if target_slug != source_slug and target_slug in linked_slugs:
                link_matrix.at[source_slug, target_slug] = 1

    except Exception as e:
        print(f"Failed for {source_slug}: {e}")
    
    time.sleep(1)  # Be nice to Wikipedia's servers

# Save matrix
link_matrix.to_csv("person_reference_matrix.csv")
print("Matrix saved to 'person_reference_matrix.csv'")

