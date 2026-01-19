import sqlite3
import json
import os

db_path = "/Users/manusantanameneses/Documents/Workspace/n8n/n8n_data/database.sqlite"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # query to find workflow by name
    cursor.execute("SELECT id, name, nodes, connections FROM workflow_entity WHERE name LIKE '%Automated Google Ads audit workflow%'")
    rows = cursor.fetchall()
    
    if not rows:
        print("No workflow found with that name.")
    else:
        for row in rows:
            wf_id, name, nodes_json, connections_json = row
            print(f"Found Workflow: {name} (ID: {wf_id})")
            
            # Reconstruct basic n8n workflow JSON structure
            workflow_data = {
                "name": name,
                "nodes": json.loads(nodes_json),
                "connections": json.loads(connections_json)
            }
            
            # Print specifically the Config nodes or nodes with "Set" operation to help user
            print("\n--- CONFIGURATION NODES ---")
            for node in workflow_data["nodes"]:
                if "Set" in node["name"] or "Config" in node["name"] or node["type"] == "n8n-nodes-base.set":
                     print(f"Node Name: {node['name']}")
                     print(f"Values: {json.dumps(node['parameters'], indent=2)}")

            # Also look for Google Ads nodes to see credentials used
            print("\n--- GOOGLE ADS NODES ---")
            for node in workflow_data["nodes"]:
                if "googleAds" in node["type"]:
                    creds = node.get("credentials", {})
                    print(f"Node: {node['name']} | Creds: {creds}")
            
    conn.close()

except Exception as e:
    print(f"Error reading DB: {e}")
