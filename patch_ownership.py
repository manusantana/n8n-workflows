import json

file_path = "workflows/Google_Ads_Audit_Professional.json"
project_id = "zZvuPL6pwZZ6dEqo"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# output full JSON structure for owner
shares = [
    {
        "role": "workflow:owner",
        "projectId": project_id
    }
]

data["shared"] = shares

# Also ensure meta doesn't conflict? 
# Usually meta is just for frontend state.

print(f"Added ownership for project {project_id}")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
