import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# --- HACKATHON SAFETY CAPS ---
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
ALLOWED_MIMES = {'image/jpeg', 'image/png', 'image/webp'}
# -----------------------------

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("\n[WARNING] Gemini API Key not found! Make sure you ran the env variable command in your terminal.\n")
    client = None
else:
    client = genai.Client(api_key=API_KEY)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "The SmartVerse Backend Engine is running on the latest Google GenAI SDK!"
    })

@app.route('/process-scene', methods=['POST'])
def process_scene():
    try:
        if not client:
            return jsonify({"status": "error", "message": "Server API key is misconfigured."}), 500

        user_query = request.form.get('query')
        
        # 1. Get the file from the request FIRST
        image_file = request.files.get('image')

        # 2. Check if they are actually there
        if not user_query or not image_file:
            return jsonify({"status": "error", "message": "Missing query or image payload."}), 400

        # 3. NOW check the file type
        if image_file.content_type not in ALLOWED_MIMES:
            return jsonify({"status": "error", "message": f"Unsupported file type: {image_file.content_type}"}), 415

        # 4. Safe to read now!
        image_bytes = image_file.read()
        
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=image_file.content_type,
        )

        system_instruction = (
            "You are a dedicated, high-speed mobility assistant for the blind and visually impaired. "
            "Analyze the image coordinates precisely and answer the user's specific spatial query. "
            "1. Give directional orientations relative to their stance (e.g., left, right, upper foreground). "
            "2. Estimate proximity or layout relationships cleanly (e.g., 'about two feet away'). "
            "3. MANDATORY: Scan the active viewport for any structural physical hazards (like a table fan, "
            "sharp edges, open flames, or tripping hazards) and lead with a warning if they are dangerously close."
        )

        print(f"\n[AI RUN] Forwarding payload to Gemini: '{user_query}'...")
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image_part, f"User Query: {user_query}"],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )

        print(f"[AI SUCCESS] Gemini responded smoothly.")

        return jsonify({
            "status": "success",
            "spatial_description": response.text
        })

    except Exception as e:
        print(f"[ERROR] Engine Failure: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server processing failure."}), 500

if __name__ == '__main__':
    # 0.0.0.0 and debug=True are perfect for your local hackathon dev environment
    app.run(debug=True, host='0.0.0.0', port=5000)