import json

file_path = "workflows/Google_Ads_Audit_Professional.json"
target_id = "D28PxgjqN7Ak3rpM0EYUf"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Set the ID explicitly
data["id"] = target_id
print(f"Set workflow ID to {target_id}")

# Ensure active is false to avoid conflict on import? Or true?
# If overwriting, better to keep it false first then user activates.
data["active"] = False

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
