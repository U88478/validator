import json
import re

from tututu import empiler, depiler

# Load tags and attributes information
with open("html_unified_info.json", "r") as info_file:
    unified_info = json.load(info_file)


def tag_details(tag_name):
    return unified_info.get(tag_name.lower())


def validate_html(html: str) -> list | str:
    html_lines = html.splitlines()

    tags_stack = []
    errors = []
    essential_errors = []
    doctype_found = False

    # Track essential tags
    essential_tags_order = ["html", "head", "body"]
    essential_tags_found = {tag: False for tag in essential_tags_order}
    essential_tags_closed = {tag: False for tag in essential_tags_order}
    essential_tags_lines = {tag: None for tag in essential_tags_order}

    def handle_essential_tag(tag, is_closing, line_number):
        if tag in essential_tags_order:
            if is_closing:
                essential_tags_closed[tag] = True
            else:
                essential_tags_found[tag] = True
                if essential_tags_lines[tag] is None:
                    essential_tags_lines[tag] = line_number

    def validate_essential_tags():
        # Check for missing essential tags in the correct order
        if not doctype_found:
            empiler(essential_errors, "Missing DOCTYPE declaration.")
        if not essential_tags_found["html"]:
            empiler(essential_errors, "Missing <html> tag.")
        elif not essential_tags_closed["html"]:
            empiler(essential_errors, "Missing closing </html> tag.")
        if essential_tags_found["html"]:
            if not essential_tags_found["head"]:
                empiler(essential_errors, "Missing <head> tag.")
            elif not essential_tags_closed["head"]:
                empiler(essential_errors, "Missing closing </head> tag.")
            if not essential_tags_found["body"]:
                empiler(essential_errors, "Missing <body> tag.")
            elif not essential_tags_closed["body"]:
                empiler(essential_errors, "Missing closing </body> tag.")

    def validate_attributes(tag, attributes_str, line_number):
        if attributes_str:
            attributes = re.findall(r'(\w+)(?:\s*=\s*"[^"]*")?', attributes_str)
            for attr in attributes:
                if attr not in tag_details(tag)["attributes"]:
                    empiler(errors, f"Line {line_number}: Invalid attribute '{attr}' for tag <{tag}>.")

    for line_number, line_content in enumerate(html_lines, start=1):
        line_content = line_content.strip()

        # Check the arrows < >
        an = []
        for i in line_content:
            if i == "<":
                empiler(an, (line_number, i))
            elif i == ">":
                depiler(an) if an else empiler(errors, f"Line {line_number}: Unexpected closing tag {i}")
        if an:
            for line_number, _ in an:
                empiler(errors, (f"Line {line_number}: Missing closing >."))

        # Check for DOCTYPE declaration
        if not doctype_found and re.match(r'<!DOCTYPE html>', line_content, re.IGNORECASE):
            doctype_found = True

        html_tags = re.findall(r'<(/?)(\w+)(?:\s+([^>]*?))?>', line_content)
        comments = re.findall(r'(?P<full_comment><!-{0,2}\s*(?P<conditional>\[)?[^>]*>)', line_content)

        # Check for valid comments
        for match in comments:
            full_comment, conditional = match
            if full_comment.startswith('<!DOCTYPE') or conditional or re.match(r'<!--.*-->', full_comment):
                continue
            else:
                empiler(errors, f"Line {line_number}: Malformed comment {full_comment}")

        for is_closing, tag_name, attributes_str in html_tags:
            tag_name_lower = tag_name.lower()
            tag_info = tag_details(tag_name_lower)

            if not tag_info:
                empiler(errors, f"Line {line_number}: Unknown or unsupported tag <{tag_name}>.")
                continue

            handle_essential_tag(tag_name_lower, is_closing == '/', line_number)
            validate_attributes(tag_name_lower, attributes_str, line_number)

            if is_closing == '/':
                if tags_stack and tags_stack[-1][1] == tag_name_lower:
                    depiler(tags_stack)
                else:
                    if any(t[1] == tag_name_lower for t in tags_stack):
                        empiler(errors, (
                            f"Line {line_number}: Unexpected closing tag </{tag_name}>. "
                            f"Other tags were expected to close first."))
                        while tags_stack and tags_stack[-1][1] != tag_name_lower:
                            line_num, unclosed_tag = tags_stack.pop()
                            empiler(errors, f"Line {line_num}: Missing closing </{unclosed_tag}>.")
                        depiler(tags_stack)
                    else:
                        expected_tag = tags_stack[-1][1] if tags_stack else 'None'
                        empiler(errors,
                                f"Line {line_number}: Unexpected closing tag </{tag_name}>. Expected </{expected_tag}>.")
            else:
                if not tag_info["void"]:
                    empiler(tags_stack, (line_number, tag_name_lower))

    # Final checks for essential tags
    validate_essential_tags()

    if essential_errors:
        for error in essential_errors[::-1]:
            errors.insert(0, error)

    if tags_stack:
        for line_number, tag_name in tags_stack:
            empiler(errors, f"Line {line_number}: Missing closing </{tag_name}>.")

    return errors if errors else "HTML validation passed."

# Example
# validate_html("test_index.html")
