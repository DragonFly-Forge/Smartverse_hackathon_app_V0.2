# 👁️ Voice Vision Assist - Backend Core

An assistive computer-vision API server built for the visually impaired and blind. This application acts as an intelligent, voice-directed spatial guide, accepting raw camera inputs alongside spoken user queries to identify physical room coordinates and flag immediate navigational environmental hazards (like spinning table fans, loose wires, or sharp boundaries).

Built for the **SMART VERSE HACKATHON**.

---

## 🚀 The Core Architecture
This server acts as the centralized gateway bridging the mobile device client and the AI cloud:
1. **The Client (Phone):** Sends a combined payload containing a voice-to-text string query and a raw JPEG frame from the camera.
2. **The Server (Flask):** Unpacks the multi-part request data, runs error-handling checks, and formats the inputs.
3. **The Brain (Gemini):** Leverages Google's state-of-the-art multimodal vision intelligence to analyze the frame geometry based on safety-first spatial system instructions.

---

## 🛠️ Tech Stack & Dependencies
* **Backend Framework:** Python 3.11+ / Flask
* **Cognitive AI Model:** Gemini 1.5 Flash (Optimized for ultra-low latency mobile streaming)
* **Official SDK:** Google GenAI SDK (`google-genai`)

---

## 📂 Project Structure
```text
Smartverse_app/
├── venv/                 # Isolated Python virtual environment (Git Ignored)
├── templates/            # UI templates (for preliminary web testing)
│   └── index.html        # One-touch accessible frontend test frame
├── app.py                # Main backend server application routing engine
└── .gitignore            # Version control filters
# ⚙️ Quickstart Installation & Local Setup

# 1. Clone the Repository & Navigate
git clone https://github.com/DragonFly-Forge/Smartverse_hackathon_app_V0.2.git
cd Smartverse_app

# 2. Initialize and Activate Virtual Environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\activate

# 3. Install Package Requirements
pip install flask google-genai

# 4. Inject Google AI Studio API Secret
# (Generate a free credential key from https://aistudio.google.com/)
$env:GEMINI_API_KEY="your_actual_copied_api_key_here"

# 5. Fire Up the Server Engine
python app.py
