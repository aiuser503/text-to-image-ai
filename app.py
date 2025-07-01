from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from gradio_client import Client
import os
import datetime

app = Flask(__name__)
CORS(app)

# Create generated images folder if it doesn't exist
os.makedirs("static/generated", exist_ok=True)

client = Client("aiuser12345678/sanjay-image-ai")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        prompt = request.json.get("prompt")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        result = client.predict(prompt, api_name="/predict")

        filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.webp"
        filepath = f"static/generated/{filename}"

        # Save image
        with open(filepath, "wb") as f:
            f.write(result)

        return jsonify({"url": f"/static/generated/{filename}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Bind to 0.0.0.0 for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
