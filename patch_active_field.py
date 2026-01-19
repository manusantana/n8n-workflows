import json

file_path = "workflows/Google_Ads_Audit_Professional.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Add missing 'active' field
if "active" not in data:
    data["active"] = False
    print("Added 'active': False to workflow root")
else:
    print("'active' field already exists")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
