import sys
import json
import re

diff_file = sys.argv[1]
content_file = sys.argv[2]

def is_valid_rgb(value):
    hex_pattern = r'^#[0-9A-Fa-f]{6}$'
    return bool(re.match(hex_pattern, value))

def validate_dict(item):
    if not isinstance(item, dict):
        return False, "Item is not a dictionary."

    required_keys = {"x", "y", "rgb"}
    if set(item.keys()) != required_keys:
        return False, f"Item keys do not match the required keys {required_keys}."

    if not isinstance(item['x'], int) or not (0 <= item['x'] <= 150):
        return False, "Invalid 'x' value. Must be an integer between 0 and 150."

    if not isinstance(item['y'], int) or not (0 <= item['y'] <= 60):
        return False, "Invalid 'y' value. Must be an integer between 0 and 60."

    if not is_valid_rgb(item['rgb']):
        return False, "Invalid 'rgb' value. Must be a valid hex color (e.g., #ffffff)."

    return True, None

with open(diff_file, 'r') as f:
    changes = f.readlines()

print("Changes from the PR:")
for change in changes:
    print(change)

with open(content_file, 'r') as f:
    file_content = f.read()

print("Content of the modified file (pixel_update.json):")
print(file_content)

try:
    data = json.loads(file_content)
except json.JSONDecodeError as e:
    print(f"Error: Failed to parse JSON. {str(e)}")
    sys.exit(1)

if not isinstance(data, list):
    print("Error: The content should be a list of dictionaries.")
    sys.exit(1)

if len(data) > 5:
    print("Error: The list contains more than 5 dictionaries.")
    sys.exit(1)

for i, item in enumerate(data):
    is_valid, error_message = validate_dict(item)
    if not is_valid:
        print(f"Error in dictionary at index {i}: {error_message}")
        sys.exit(1)

print("Validation successful: The pixel_update.json file is correctly formatted.")