"""
AI Image Generator — Flask Backend
===================================
Uses Hugging Face's Stable Diffusion v1-5 via the 🤗 diffusers library.
The model is loaded once at startup and reused for every request.
"""

import os
import uuid
import time
import logging
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_from_directory
import torch
from diffusers import StableDiffusionPipeline

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent / "generated_images"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_ID = "runwayml/stable-diffusion-v1-5"

# Inference defaults
DEFAULT_STEPS = 30          # Good quality / speed trade-off
DEFAULT_GUIDANCE = 7.5      # Classifier-free guidance scale
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Device & Model Setup (runs once at import / startup)
# ---------------------------------------------------------------------------

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

log.info("Detected device: %s  |  dtype: %s", DEVICE, DTYPE)
log.info("Loading model  %s …  (this may take a minute on first run)", MODEL_ID)

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=DTYPE,
    safety_checker=None,                   # Remove NSFW filter for speed
    requires_safety_checker=False,
)
pipe = pipe.to(DEVICE)

# Performance optimisations
if DEVICE == "cuda":
    pipe.enable_attention_slicing()         # Lower VRAM usage
    try:
        pipe.enable_xformers_memory_efficient_attention()
        log.info("xformers memory-efficient attention enabled")
    except Exception:
        log.info("xformers not available — using default attention")

log.info("Model loaded and ready on %s ✓", DEVICE)

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

    # --- Inference ------------------------------------------------------------
    try:
        start = time.time()

        generator = torch.Generator(device=DEVICE)
        generator.manual_seed(torch.randint(0, 2**32 - 1, (1,)).item())

        # Use autocast for mixed-precision on GPU
        with torch.autocast(DEVICE, enabled=(DEVICE == "cuda")):
            result = pipe(
                prompt=full_prompt,
                num_inference_steps=DEFAULT_STEPS,
                guidance_scale=DEFAULT_GUIDANCE,
                width=DEFAULT_WIDTH,
                height=DEFAULT_HEIGHT,
                generator=generator,
            )

        elapsed = round(time.time() - start, 2)
        image = result.images[0]

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
