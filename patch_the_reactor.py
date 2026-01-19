import json

file_path = "workflows/LTtD6izOWBatig-7qv8IA.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Navigate to the Code node (ID: 9a50eba4-e10c-4709-a4ec-776ccb89ba18)
nodes = data.get("nodes", [])
code_node = next((n for n in nodes if n["id"] == "9a50eba4-e10c-4709-a4ec-776ccb89ba18"), None)

if code_node:
    # Improved Robust Parsing Logic
    new_code = """// 1. Limpieza JSON
const root = items[0].json;
// Handle Gemini Envelope (parts vs text)
let rawText = (root.content && root.content.parts) ? root.content.parts[0].text : (root.text || root.content || "");

// Buscador de llaves para extraccion
const firstBrace = rawText.indexOf('{');
const lastBrace = rawText.lastIndexOf('}');
let cleanJSON = rawText;

if (firstBrace !== -1 && lastBrace !== -1) {
    cleanJSON = rawText.substring(firstBrace, lastBrace + 1);
}

// 2. Parsers intent (Try multiple strategies)
let content = {};
let parseSuccess = false;

// Strategy A: Direct Parse (Best for valid JSON)
if (!parseSuccess) {
    try {
        content = JSON.parse(cleanJSON);
        parseSuccess = true;
    } catch (e) {}
}

// Strategy B: Clean Markdown code blocks if existing
if (!parseSuccess) {
    try {
        let noMarkdown = cleanJSON.replace(/```json/g, "").replace(/```/g, "").trim();
        content = JSON.parse(noMarkdown);
        parseSuccess = true;
    } catch(e) {}
}

// Strategy C: Fix unescaped newlines (Old Logic - improved)
if (!parseSuccess) {
    try {
        // Only escape newlines if they seem to be breaking strings? 
        // Actually, replacing all \\n with \\\\n breaks headers.
        // Let's try to just parse what we can or return fallback.
        // Attempt aggressive cleanup:
        const fixedJSON = cleanJSON.replace(/\\n/g, "\\\\n").replace(/\\r/g, "");
        content = JSON.parse(fixedJSON);
        parseSuccess = true;
    } catch (e) {
        // Fallback final
        content = { 
            linkedin_content: "⚠️ Error formato: " + rawText.substring(0, 100), 
            blog_content: "Error",
            image_prompt: "Abstract AI concept"
        };
    }
}

// 3. RECUPERAR TÍTULO ORIGINAL
let originalTitle = "Borrador Automático";
try {
    originalTitle = $('Code in JavaScript').first().json.target_topic.title; 
} catch(e) {
    try { originalTitle = $('Code in JavaScript').first().json.topic_title; } catch(e2) {}
}

// SALIDA
return {
    json: {
        title: originalTitle,
        linkedin_draft: content.linkedin_content || content.linkedin_draft,
        blog_draft: content.blog_content || content.blog_draft,
        image_prompt: content.image_prompt || "Futuristic technology concept, editorial photography, 8k"
    }
};"""

    code_node["parameters"]["jsCode"] = new_code
    print("Successfully patched The Reactor Code node")

else:
    print("Code node not found")

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
