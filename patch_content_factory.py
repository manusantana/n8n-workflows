import json

file_path = "workflows/3SujNhDcvxSyDmdAiUb7d.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Navigate to the Code in JavaScript node
nodes = data.get("nodes", [])
code_node = next((n for n in nodes if n["id"] == "fa6f59b2-6347-40d8-a075-2c32101aef86"), None)

if code_node:
    js_code = code_node["parameters"]["jsCode"]
    
    # Define replacement (insertion of raw_debug)
    target = 'data_json: JSON.stringify({ topics: topics })'
    replacement = 'data_json: JSON.stringify({ topics: topics }),\n    raw_debug: cleanContent'
    
    if target in js_code:
        new_js_code = js_code.replace(target, replacement)
        code_node["parameters"]["jsCode"] = new_js_code
        print("Successfully patched jsCode")
    else:
        print("Target string not found in jsCode")
        print("Current jsCode snippet:", js_code[-100:])
else:
    print("Code node not found")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
