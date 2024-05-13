import json

import requests
from bs4 import BeautifulSoup

# URL of the page containing the table
url = "https://www.w3schools.com/tags/"

# Fetch the HTML content
response = requests.get(url)
html_content = response.text

void_list = [
    "area", "base", "br", "col", "embed",
    "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr"
]

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table by its class name
table = soup.find("table", {"class": "ws-table-all notranslate"})

# Extract data from the table
tags_info = {}

for row in table.find_all("tr")[1:]:  # Skip the header row
    cells = row.find_all("td")
    if len(cells) == 2:  # Ensure the row has exactly two columns
        tag = cells[0].text.strip('<> ')  # Clean up the tag text
        description = cells[1].text.strip()
        void = tag in void_list
        tags_info[tag] = {
            "description": description,
            "void": void
        }

# Write the data to a JSON file
file_path = "html_tags_info.json"
with open(file_path, 'w') as json_file:
    json.dump(tags_info, json_file, indent=4)

print(f"Data extracted and saved to {file_path}")
