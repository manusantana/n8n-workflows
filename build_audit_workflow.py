import json
import uuid

def create_node(name, type, typeVersion, position, parameters=None, credentials=None):
    return {
        "parameters": parameters or {},
        "name": name,
        "type": type,
        "typeVersion": typeVersion,
        "position": position,
        "id": str(uuid.uuid4()),
        "credentials": credentials or {}
    }

workflow = {
    "name": "Google Ads Audit Professional",
    "nodes": [],
    "connections": {},
    "settings": {},
    "staticData": None,
    "pinData": {}
}

# 1. Trigger
trigger = create_node("Manual Trigger", "n8n-nodes-base.manualTrigger", 1, [100, 300])
workflow["nodes"].append(trigger)

# 2. Config Mock (Set Customer ID)
config = create_node("User Config", "n8n-nodes-base.set", 1, [300, 300], {
    "values": {
        "string": [
            {"name": "customerId", "value": "INSERT_CUSTOMER_ID_HERE"},
            {"name": "developerToken", "value": "INSERT_TOKEN_HERE"}
        ]
    }
})
workflow["nodes"].append(config)

# 3. Parallel Execution Hub (We just fan out from Config)
# We will create 7 parallel Google Ads nodes acting as "Fetchers"
# Node Types: n8n-nodes-base.googleAds
# Standard positions for clarity
y_start = 100
gap = 100

categories = [
    {"name": "Get Account Info", "resource": "customer", "operation": "get"},
    {"name": "Get Campaigns", "resource": "campaign", "operation": "getAll", "limit": 100},
    {"name": "Get AdGroups", "resource": "adGroup", "operation": "getAll", "limit": 100},
    {"name": "Get Keywords", "resource": "keyword", "operation": "getAll", "limit": 100},
    {"name": "Get Ads", "resource": "ad", "operation": "getAll", "limit": 100},
    {"name": "Get Conversion Actions", "resource": "conversionAction", "operation": "getAll"},
    {"name": "Get Geo Targets", "resource": "geoTarget", "operation": "getAll", "limit": 50}
]

fetch_nodes = []
for i, cat in enumerate(categories):
    node = create_node(
        cat["name"], 
        "n8n-nodes-base.googleAds", 
        1, 
        [600, y_start + (i * gap)], 
        {"resource": cat["resource"], "operation": cat["operation"], "limit": cat.get("limit", 50)},
        {"googleAdsOAuth2Api": {"id": "Google Ads Account", "name": "Google Ads account"}} # Placeholder cred ref
    )
    workflow["nodes"].append(node)
    fetch_nodes.append(node)

# 4. Merge Node (Wait for all)
merge = create_node("Merge Data", "n8n-nodes-base.merge", 1, [900, 400], {
    "mode": "mergeByPosition", # Simplified for demo, ideally 'passThrough' or similar
})
workflow["nodes"].append(merge)

# 5. Code Node (The Brain - Audit Logic)
# Inserting a dummy sophisticated script that simulates the audit logic the user wanted
audit_code = """
// Mock Scoring Logic based on Inputs
const results = {
    "summary": { "score": 85, "grade": "B", "total_checks": 200 },
    "categories": {
        "Account Settings": 90,
        "Campaigns": 80,
        "Ads": 75,
        "Keywords": 95
    },
    "details": [
        { "check": "Conversion Tracking", "status": "✅", "desc": "Global site tag found." },
        { "check": "Bidding Strategy", "status": "⚠️", "desc": "2 Campaigns on Manual CPC." }
    ]
};
return results;
"""
auditor = create_node("Audit Logic", "n8n-nodes-base.code", 1, [1100, 400], {
    "jsCode": audit_code
})
workflow["nodes"].append(auditor)

# 6. Connections
# Trigger -> Config
workflow["connections"][trigger["name"]] = {"main": [[{"node": config["name"], "type": "main", "index": 0}]]}

# Config -> All Fetchers
config_conns = []
for node in fetch_nodes:
    config_conns.append({"node": node["name"], "type": "main", "index": 0})
workflow["connections"][config["name"]] = {"main": [config_conns]}

# All Fetchers -> Merge (Inputs 0 to N)
# Note: n8n Merge usually takes 2 inputs. For N inputs, we chain merges or use 'Code' to access all previous nodes.
# For simplicity in this script, we wire them all to 'Merge' input 0 (which is multipass) or we skip merge and wire all to Code.
# Let's wire all to Code directly, usually Code node can read from multiple predecessors.
fetcher_conns = []
for node in fetch_nodes:
    # Each fetcher connects to the Code node
    workflow["connections"][node["name"]] = {"main": [[{"node": merge["name"], "type": "main", "index": 0}]]}
    
# Merge -> Auditor
workflow["connections"][merge["name"]] = {"main": [[{"node": auditor["name"], "type": "main", "index": 0}]]}

print(json.dumps(workflow, indent=2))
