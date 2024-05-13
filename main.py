import json
import re

with open("html_tags_info.json", "r") as html_info:
    tags_info = json.load(html_info)


def tag_details(tag_name):
    tag_data = tags_info.get(tag_name.lower())  # Case-insensitive matching
    if tag_data:
        return {
            "Name": tag_name,
            "Description": tag_data.get('description', "No description provided."),
            "Void": tag_data.get('void', False)
        }
    return None


def validate_html(file_path):
    with open(file_path, "r") as html:
        html_lines = html.readlines()

    tags_stack = []  # Opened tags stack
    errors = []

    for line_number, line_content in enumerate(html_lines, start=1):
        html_tags = re.findall(r'<(/?)(\w+)(?:\s+[^>]*?)?>', line_content)
        for is_closing, tag_name in html_tags:
            tag_info = tag_details(tag_name)

            if not tag_info:
                errors.append(f"Line {line_number}: Unknown or unsupported tag <{tag_name}>.")
                continue

            if is_closing:
                if tags_stack and tags_stack[-1][1] == tag_name:
                    tags_stack.pop()
                else:
                    # Check if it matches any tag in the stack(unexpected closing tag) to provide specific feedback
                    if any(t[1] == tag_name for t in tags_stack):
                        errors.append(
                            f"Line {line_number}: Unexpected closing tag <{tag_name}>. "
                            f"Other tags were expected to close first.")
                        # Close up to the unexpected tag, noting an error for each
                        while tags_stack and tags_stack[-1][1] != tag_name:
                            line_num, unclosed_tag = tags_stack.pop()
                            errors.append(f"Line {line_num}: Missing closing </{unclosed_tag}>.")
                        tags_stack.pop()  # Remove the unexpected tag
                    else:
                        expected_tag = tags_stack[-1][1] if tags_stack else 'None'
                        errors.append(
                            f"Line {line_number}: Unexpected closing tag </{tag_name}>. Expected </{expected_tag}>.")
            else:
                if not tag_info["Void"]:
                    tags_stack.append((line_number, tag_name))

    if tags_stack:
        for line_number, tag_name in tags_stack:
            errors.append(f"Line {line_number}: Missing closing </{tag_name}>.")

    if errors:
        for error in errors:
            print(error)
    else:
        print("HTML validation passed.")


# Example call to validate_html function
validate_html("test_index.html")
