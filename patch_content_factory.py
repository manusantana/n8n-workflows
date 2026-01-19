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
     // Maybe it's already the flat object? unlikely given symptoms
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

// 5. Escapar DEBUG para que no rompa el HTML de Telegram (<pre>)
const escapeHtml = (unsafe) => {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
};
// Truncate debug to avoid 4096 char limit failure
let debugSafe = escapeHtml(cleanContent);
if (debugSafe.length > 1500) {
    debugSafe = debugSafe.substring(0, 1500) + "... (TRUNCATED)";
}

// 6. Preparar Outputs
return [{
  json: {
    // Para Telegram (Texto) - Unwrapped String
    mensaje_final: finalMsg,
    
    // DEBUG: Raw Content (Escaped & Truncated)
    raw_debug: debugSafe,

    // Para Google Sheets
    data_json: JSON.stringify({ topics: topics })
  }
}];"""

    code_node["parameters"]["jsCode"] = new_code
    print("Successfully patched jsCode with HTML sanitization")

else:
    print("Code node not found")

# Patch Telegram Node Expression
telegram_node = next((n for n in nodes if n["name"] == "Notificar a Manu"), None)
if telegram_node:
    # Remove .parts[0].text from expression, just use mensaje_final directly
    # Also keep the debug output
    telegram_node["parameters"]["text"] = "={{ $json.mensaje_final }}\n\n🐞 DEBUG JSON:\n<pre>{{ $json.raw_debug }}</pre>"
    print("Successfully patched Telegram node expression")
else:
    print("Telegram node not found")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
