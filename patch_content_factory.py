import json

file_path = "workflows/3SujNhDcvxSyDmdAiUb7d.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Navigate to the Code in JavaScript node
nodes = data.get("nodes", [])
code_node = next((n for n in nodes if n["id"] == "fa6f59b2-6347-40d8-a075-2c32101aef86"), None)

if code_node:
    # New robust code
    new_code = """// 1. Obtener la respuesta cruda
const rawContent = items[0].json.content;
let cleanContent = "";
let parsed;

// 2. Determinar tipo y limpiar
if (typeof rawContent === 'object' && rawContent !== null) {
  // Ya es un objeto (Gemini output mode json?)
  parsed = rawContent;
  cleanContent = JSON.stringify(rawContent, null, 2);
} else {
  // Es string, limpiar markdown logs
  const rawString = String(rawContent || "");
  cleanContent = rawString.replace(/```json/g, "").replace(/```/g, "").trim();
  try {
    parsed = JSON.parse(cleanContent);
  } catch (e) {
    parsed = {
      briefing_html: "⚠️ Error JSON: " + rawString,
      topics: []
    };
  }
}

// 4. Robustez de Claves
const topics = parsed.topics || parsed.temas || parsed.items || parsed.noticias || [];

// 5. Preparar Outputs
return [{
  json: {
    // Para Telegram (Texto)
    mensaje_final: parsed.briefing_html || "Error de formato",
    
    // DEBUG: Raw Content
    raw_debug: cleanContent,

    // Para Google Sheets
    data_json: JSON.stringify({ topics: topics })
  }
}];"""

    code_node["parameters"]["jsCode"] = new_code
    print("Successfully patched jsCode with robust status")

else:
    print("Code node not found")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
