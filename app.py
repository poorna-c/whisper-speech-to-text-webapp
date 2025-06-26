from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import whisper
import tempfile
from scipy.io.wavfile import write
import os

app = Flask(__name__)
model = whisper.load_model("base")  # load once

def save_wav_from_base64(base64_audio, filename):
    audio_data = base64.b64decode(base64_audio.split(",")[1])
    with open(filename, "wb") as f:
        f.write(audio_data)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.json
    audio_base64 = data["audio"]

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        save_wav_from_base64(audio_base64, tmpfile.name)
        result = model.transcribe(tmpfile.name) 
        #os.unlink(tmpfile.name)
    
    return jsonify({"transcription": result["text"].strip()})

if __name__ == "__main__":
    app.run(debug=True)
