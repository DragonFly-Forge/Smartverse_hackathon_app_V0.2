import os
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# --- HACKATHON SAFETY CAPS ---
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
ALLOWED_IMAGE_MIMES = {'image/jpeg', 'image/png', 'image/webp'}
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
def process_scene():  # 🟢 FIX 1: Added missing function declaration
    try:
        if not client:
            return jsonify({"status": "error", "message": "Server API key is misconfigured."}), 500

        # Debug logging to see exactly what keys your phone is successfully delivering
        print(f"[DEBUG] Received files: {list(request.files.keys())}")
        
        user_query = request.form.get('query')
        image_file = request.files.get('image')
        audio_file = request.files.get('audio')

        # 1. Image is mandatory for your vision-based tool
        if not image_file:
            print("[ERROR] 400 Triggered: 'image' key missing or empty.")
            return jsonify({"status": "error", "message": "Missing image payload."}), 400

        # 2. Check image file type
        if image_file.content_type not in ALLOWED_IMAGE_MIMES:
            return jsonify({"status": "error", "message": f"Unsupported image type: {image_file.content_type}"}), 415

        # 3. Read image bytes and prepare part
        image_bytes = image_file.read()
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=image_file.content_type,
        )

        # Build contents array with our image
        contents_payload = [image_part]

        # 4. Multimodal Routing (🟢 FIX 2: Relaxed file validation for raw hackathon audio stability)
        if audio_file and audio_file.filename != '':
            print(f"[AI ROUTE] Found raw audio command file: '{audio_file.filename}' with Type: '{audio_file.content_type}'")
            audio_bytes = audio_file.read()
            audio_part = types.Part.from_bytes(
                data=audio_bytes,
                mime_type="audio/m4a" # Force treat binary stream envelope as audio
            )
            contents_payload.append(audio_part)
            
        elif user_query:
            print(f"[AI ROUTE] Found text command string: '{user_query}'")
            contents_payload.append(f"User Query: {user_query}")
            
        else:
            print("[AI ROUTE] No audio or custom text found. Defaulting to general safety scan.")
            contents_payload.append("User Query: Identify any obstacles or physical hazards in front of me.")

        system_instruction = (
            "You are a dedicated, high-speed mobility assistant for the blind and visually impaired. "
            "Analyze the image coordinates precisely and answer the user's specific spatial query. "
            "If an audio file is attached to the payload, that is the user speaking their query aloud. Listen to it carefully and respond to the spoken instruction contextually. "
            "1. Give directional orientations relative to their stance (e.g., left, right, upper foreground). "
            "2. Estimate proximity or layout relationships cleanly (e.g., 'about two feet away'). "
            "3. MANDATORY: Scan the active viewport for any structural physical hazards (like a table fan, "
            "sharp edges, open flames, or tripping hazards) and lead with a warning if they are dangerously close."
        )

        print(f"\n[AI RUN] Forwarding multimodal payload to Gemini...")
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents_payload,
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
        return jsonify({"status": "error", "message": "Internal server processing failure.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)