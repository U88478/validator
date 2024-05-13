import re

# Regex to match HTML tags
tag_regex = r'<([a-z]+)\s*([^>]*)>'

# Find all tags in the HTML
with open("index.html", "r") as index:
    html_content = index.read()
    found_tags = re.findall(tag_regex, html_content, re.IGNORECASE)

# Print each found tag
for tag in found_tags:
    print(tag)
