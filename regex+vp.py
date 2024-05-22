import re


def validate_html(file_path):
    with open(file_path, "r") as html:
        html_lines = html.readlines()

    tags_stack = []  # Opened tags stack
    errors = []

    for line_number, line_content in enumerate(html_lines, start=1):
        html_tags = re.findall(r'<(/?)(\w+)(?:\s+[^>]*?)?>', line_content)
        for is_closing, tag_name in html_tags:
            print(is_closing, tag_name)


#  VP Function

def vp(s):
    bn = 0
    for i in s:
        if i == "<":
            bn += 1
        elif i == ">":
            bn -= 1
        if bn < 0:
            return False
    return bn == 0


# with open("index.html", "r") as index:
#     html = index.read()
#     print(vp(html))

v = vp("<<>")
# print(v)


# Example call to validate_html function
validate_html("html examples/test_index.html")
