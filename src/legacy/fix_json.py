import json
import ast

# Read the file (it's actually Python dict format, not JSON)
with open('../export/out.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse as Python literal (handles single quotes properly)
try:
    data = ast.literal_eval(content)
    print(f"Successfully parsed {len(data)} records")
    
    # Write as proper JSON
    with open('../export/out.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("JSON format corrected and saved!")
    
except Exception as e:
    print(f"Error parsing Python literal: {e}")
    # Fallback: try manual cleaning
    print("Attempting manual cleaning...")
    
    # Remove trailing commas and fix structure
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        if line.strip() == ',':
            continue
        if line.strip().endswith(','):
            line = line.rstrip().rstrip(',')
        cleaned_lines.append(line)
    
    # Join and try to parse again
    cleaned_content = '\n'.join(cleaned_lines)
    cleaned_content = cleaned_content.replace("'", '"')
    
    with open('../export/out_cleaned.json', 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print("Cleaned version saved as out_cleaned.json")
