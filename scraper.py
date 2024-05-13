import json
import requests
from bs4 import BeautifulSoup

# URLs of the pages containing the tables
tags_url = "https://www.w3schools.com/tags/"
attributes_url = "https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes"

# Fetch the HTML content
tags_response = requests.get(tags_url)
tags_html_content = tags_response.text

attributes_response = requests.get(attributes_url)
attributes_html_content = attributes_response.text

# List of void elements
void_list = [
    "area", "base", "br", "col", "embed",
    "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr"
]

# Parse the HTML content for tags
tags_soup = BeautifulSoup(tags_html_content, 'html.parser')
tags_table = tags_soup.find("table", {"class": "ws-table-all notranslate"})

# Extract data from the tags table
tags_info = {}
for row in tags_table.find_all("tr")[1:]:  # Skip the header row
    cells = row.find_all("td")
    if len(cells) == 2:  # Ensure the row has exactly two columns
        tag = cells[0].text.strip('<> ').lower()  # Clean up the tag text and convert to lowercase
        description = cells[1].text.strip()
        void = tag in void_list
        tags_info[tag] = {
            "description": description,
            "void": void,
            "attributes": []  # Placeholder
        }

# Parse the HTML content for attributes
attributes_soup = BeautifulSoup(attributes_html_content, 'html.parser')
attributes_table = attributes_soup.find("table", {"class": "standard-table"})

# Extract data from the attributes table
global_attributes = []
element_specific_attributes = {}
for row in attributes_table.find_all("tr")[1:]:  # Skip the header row
    cells = row.find_all("td")
    if len(cells) == 3:  # Ensure the row has exactly three columns
        attribute_name = cells[0].text.strip()
        elements = cells[1].find_all("code")
        description = cells[2].text.strip()

        if "Global attribute" in cells[1].text:
            global_attributes.append({"name": attribute_name, "description": description})
        else:
            for element in elements:
                element_name = element.text.strip('<>').lower()
                if element_name not in element_specific_attributes:
                    element_specific_attributes[element_name] = []
                element_specific_attributes[element_name].append({"name": attribute_name, "description": description})

# Combine the global and element-specific attributes with the tag information
for tag in tags_info.keys():
    tag_name = tag.lower()
    tags_info[tag_name]["attributes"] = [attr["name"] for attr in
                                         global_attributes + element_specific_attributes.get(tag_name, [])]

# Write the data to a JSON file
file_path = "html_unified_info.json"
with open(file_path, 'w') as json_file:
    json.dump(tags_info, json_file, indent=4)

print(f"Data extracted and saved to {file_path}")
