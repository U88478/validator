import re

with open('index.html', 'r') as file:
    line_content = file.readlines()

for line_number, line in enumerate(line_content, start=1):
    comments = re.findall(r'(?P<full><!-{0,2}\s*(\[)?[^>]*>)', line)
    for match in comments:
        a, b = match
        print(match)
