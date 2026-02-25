"""
AI Image Generator — Flask Backend
===================================
Uses Hugging Face's Inference API for Stable Diffusion image generation.
No local GPU or large model download required.
"""

import os
import uuid
import time
import logging
from pathlib import Path

from io import BytesIO

import requests as http_requests
from PIL import Image
from flask import Flask, render_template, request, jsonify, send_from_directory

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent / "generated_images"
OUTPUT_DIR.mkdir(exist_ok=True)

# HF Inference API model
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"

# Optional: set HF_TOKEN env var for higher rate limits
HF_TOKEN = os.environ.get("HF_TOKEN", None)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# HF Inference API setup
# ---------------------------------------------------------------------------

API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

log.info("HF Inference API ready  (model: %s)", MODEL_ID)
if HF_TOKEN:
    log.info("Using authenticated requests (HF_TOKEN set)")
else:
    log.info("Using unauthenticated requests — set HF_TOKEN env var for higher rate limits")

# ---------------------------------------------------------------------------
# Style Presets — appended to the user prompt
# ---------------------------------------------------------------------------

STYLE_PRESETS = {
    "none": "",
    "cinematic": ", cinematic lighting, dramatic atmosphere, film grain, anamorphic lens, "
                 "color grading, directed by Roger Deakins, 8k",
    "anime": ", anime style, studio ghibli, cel shading, vibrant colors, "
             "detailed illustration, manga aesthetic, high quality anime art",
    "realistic": ", ultra realistic, photorealistic, DSLR photo, 8k uhd, "
                 "sharp focus, natural lighting, detailed textures, professional photography",
    "cyberpunk": ", cyberpunk style, neon lights, futuristic cityscape, rain, "
                 "holographic, synthwave colors, blade runner aesthetic, 8k",
}

# ---------------------------------------------------------------------------
# Flask App
# ---------------------------------------------------------------------------

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the main UI."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """
    Generate an image from the supplied prompt.

    Expects JSON: { "prompt": "...", "style": "cinematic" }
    Returns JSON:  { "success": true, "image_url": "/images/<file>", "time": 12.3 }
    """
    data = request.get_json(force=True)
    prompt = (data.get("prompt") or "").strip()

    # --- Validation -----------------------------------------------------------
    if not prompt:
        return jsonify({"success": False, "error": "Prompt cannot be empty."}), 400

    style_key = (data.get("style") or "none").lower()
    style_suffix = STYLE_PRESETS.get(style_key, "")
    full_prompt = prompt + style_suffix

    log.info("Generating  ➜  prompt=%r  style=%s", prompt, style_key)

    # --- Inference via HF API ------------------------------------------------
    try:
        start = time.time()

        payload = {"inputs": full_prompt}
        response = http_requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)

        if response.status_code != 200:
            error_msg = response.json().get("error", response.text) if response.headers.get("content-type", "").startswith("application/json") else response.text
            log.error("HF API error %s: %s", response.status_code, error_msg)
            return jsonify({"success": False, "error": f"HF API error: {error_msg}"}), 502

        image = Image.open(BytesIO(response.content))

        elapsed = round(time.time() - start, 2)

        # --- Save to disk -----------------------------------------------------
        filename = f"{uuid.uuid4().hex}.png"
        filepath = OUTPUT_DIR / filename
        image.save(str(filepath))
        log.info("Saved  ➜  %s  (%.2fs)", filepath.name, elapsed)

        return jsonify({
            "success": True,
            "image_url": f"/images/{filename}",
            "time": elapsed,
        })

    except Exception as exc:
        log.exception("Generation failed")
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route("/images/<path:filename>")
def serve_image(filename):
    """Serve a generated image file."""
    return send_from_directory(str(OUTPUT_DIR), filename)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
