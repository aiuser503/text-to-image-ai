from flask import Flask, render_template, request
from gradio_client import Client
import shutil
import os

app = Flask(__name__)
client = Client("aiuser12345678/sanjay-image-ai")

OUTPUT_FOLDER = "static/generated"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    error = None

    if request.method == "POST":
        prompt = request.form.get("prompt")
        try:
            result = client.predict(prompt=prompt, api_name="/predict")

            if os.path.isfile(result):  # if it's a local file
                output_path = os.path.join(OUTPUT_FOLDER, "generated_image.webp")
                shutil.copy(result, output_path)
                image_url = "/" + output_path.replace("\\", "/")
            else:
                error = "Model did not return a valid image file."

        except Exception as e:
            error = str(e)

    return render_template("index.html", image_url=image_url, error=error)

if __name__ == "__main__":
    app.run(debug=True)
