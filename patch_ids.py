import json
import uuid

file_path = "workflows/Google_Ads_Audit_Professional.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Ensure 'active' is False
data["active"] = False

# Add versionId if missing
if "versionId" not in data:
    data["versionId"] = str(uuid.uuid4())
    print("Added versionId")

# Ensure it has an ID so it updates the same workflow if possible, 
# or let n8n create one if we don't have one.
# But for import to work cleanly, usually we don't need 'id' if creating new.
# However, the error suggests it might be trying to update and failing on constraints?
# Or the schema just enforces versionId presence.

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
