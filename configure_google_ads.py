import json

file_path = "workflows/Google_Ads_Audit_Professional.json"
developer_token = "KRf0ngVsjSngdG5dmVFh5w"
customer_id = "574-385-0460"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

nodes = data.get("nodes", [])

# 1. Configure "User Config" node
config_node = next((n for n in nodes if n["name"] == "User Config"), None)
if config_node:
    # Update values
    values = config_node.get("parameters", {}).get("values", {}).get("string", [])
    for val in values:
        if val["name"] == "customerId":
            val["value"] = customer_id
        if val["name"] == "developerToken":
            val["value"] = developer_token
    print("Updated User Config node with Token and Customer ID")

# 2. Configure Google Ads Nodes
google_ads_nodes = [n for n in nodes if n["type"] == "n8n-nodes-base.googleAds"]
for node in google_ads_nodes:
    # Ensure customerId parameter exists and is bound
    if "parameters" not in node:
        node["parameters"] = {}
    
    # Bind customerId to User Config output
    node["parameters"]["customerId"] = "={{ $('User Config').item.json.customerId }}"
    
    # Ensure Credentials use the standard ID we expect (User must name it this or we rely on import matching)
    if "credentials" not in node:
        node["credentials"] = {}
    
    # Force use of googleAdsOAuth2Api
    node["credentials"]["googleAdsOAuth2Api"] = {
        "id": "Google Ads Account",
        "name": "Google Ads account"
    }
    
print(f"Updated {len(google_ads_nodes)} Google Ads nodes with customerId binding")

# Save
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
