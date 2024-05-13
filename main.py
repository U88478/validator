import json
import re

# Load unified tags and attributes information
with open("html_unified_info.json", "r") as info_file:
    unified_info = json.load(info_file)


def tag_details(tag_name):
    return unified_info.get(tag_name.lower())


def validate_html(file_path):
    with open(file_path, "r") as html:
        html_lines = html.readlines()

    tags_stack = []  # Opened tags stack
    errors = []

    for line_number, line_content in enumerate(html_lines, start=1):
        html_tags = re.findall(r'<(/?)(\w+)(?:\s+([^>]*?))?>', line_content)
        for is_closing, tag_name, attributes_str in html_tags:
            tag_info = tag_details(tag_name)

            if not tag_info:
                errors.append(f"Line {line_number}: Unknown or unsupported tag <{tag_name}>.")
                continue

            if attributes_str:
                attributes = re.findall(r'(\w+)(?:\s*=\s*"[^"]*")?', attributes_str)
                for attr in attributes:
                    if attr not in tag_info["attributes"]:
                        errors.append(f"Line {line_number}: Invalid attribute '{attr}' for tag <{tag_name}>.")

            if is_closing:
                if tags_stack and tags_stack[-1][1] == tag_name:
                    tags_stack.pop()
                else:
                    # Check if it matches any tag in the stack (unexpected closing tag) to provide specific feedback
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
                if not tag_info["void"]:
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
