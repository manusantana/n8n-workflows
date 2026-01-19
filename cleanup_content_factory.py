import json

file_path = "workflows/3SujNhDcvxSyDmdAiUb7d.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Navigate to the Code in JavaScript node
nodes = data.get("nodes", [])
code_node = next((n for n in nodes if n["id"] == "fa6f59b2-6347-40d8-a075-2c32101aef86"), None)

if code_node:
    # Production Ready Code (Robust Logic kept, Debug output removed)
    new_code = """// 1. Obtener la respuesta cruda
const rawContent = items[0].json.content;
let cleanContent = "";
let parsed;

// 2. Determinar tipo y limpiar (Handling Gemini Envelope)
if (typeof rawContent === 'object' && rawContent !== null) {
  // Check if it's the Gemini Envelope { parts: [{ text: "..." }] }
  if (rawContent.parts && rawContent.parts[0] && rawContent.parts[0].text) {
      const innerText = rawContent.parts[0].text;
      const rawString = String(innerText || "");
      cleanContent = rawString.replace(/```json/g, "").replace(/```/g, "").trim();
      try {
        parsed = JSON.parse(cleanContent);
      } catch (e) {
        parsed = {
            briefing_html: "⚠️ Error Parseando Inner JSON: " + rawString,
            topics: []
        };
      }
  } else {
     // Maybe it's already the flat object?
     parsed = rawContent; 
     cleanContent = JSON.stringify(rawContent, null, 2);
  }
} else {
  // Es string directo?
  const rawString = String(rawContent || "");
  cleanContent = rawString.replace(/```json/g, "").replace(/```/g, "").trim();
  try {
    parsed = JSON.parse(cleanContent);
  } catch (e) {
    parsed = {
      briefing_html: "⚠️ Error Parseando String JSON: " + rawString,
      topics: []
    };
  }
}

// 3. Sanitizar HTML para Telegram (Dumb & Safe Replace)
// Telegram NO soporta <br> ni <p>
let finalMsg = parsed.briefing_html || "Error de formato (No briefing_html)";
finalMsg = finalMsg.split('<br>').join('\\n')
                 .split('<br/>').join('\\n')
                 .split('<br />').join('\\n')
                 .split('<p>').join('\\n')
                 .split('</p>').join('\\n');

// 4. Robustez de Claves
const topics = parsed.topics || parsed.temas || parsed.items || parsed.noticias || [];

// 5. Preparar Outputs
return [{\n  json: {\n    // Para Telegram (Texto) - Unwrapped String
    mensaje_final: finalMsg,
    
    // Para Google Sheets
    data_json: JSON.stringify({ topics: topics })
  }\n}];"""

    code_node["parameters"]["jsCode"] = new_code
    print("Successfully cleaned up jsCode (Debug Removed)")

else:
    print("Code node not found")

# Patch Telegram Node Expression to remove debug part
telegram_node = next((n for n in nodes if n["name"] == "Notificar a Manu"), None)
if telegram_node:
    # Set back to clean message
    telegram_node["parameters"]["text"] = "={{ $json.mensaje_final }}"
    print("Successfully reverted Telegram node expression")
else:
    print("Telegram node not found")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
