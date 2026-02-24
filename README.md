# AI Image Generator

> Transform text prompts into stunning images using **Stable Diffusion v1.5** — powered by Hugging Face Diffusers, Flask, and a premium glassmorphism UI.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![Stable Diffusion](https://img.shields.io/badge/Model-SD%20v1.5-purple)

---

## Features

- Text-to-image generation via **runwayml/stable-diffusion-v1-5**
- Auto GPU/CPU detection with `float16` optimisation on CUDA
- Style presets: Cinematic, Anime, Realistic, Cyberpunk
- One-click image download
- Generated images saved to `generated_images/`
- Loading spinner & error handling
- Dark premium glassmorphism UI (responsive)
- Keyboard shortcut: **Ctrl+Enter** to generate

---

## Project Structure

```
ai-image-generator/
├── app.py                  # Flask backend + model inference
├── requirements.txt        # Python dependencies
├── static/
│   ├── styles.css          # Premium dark theme CSS
│   └── script.js           # Frontend logic
├── templates/
│   └── index.html          # Main UI template
├── generated_images/       # Output folder (auto-created)
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kris-gadara/AI-Image-Generator.git
cd AI-Image-Generator
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **GPU users (NVIDIA):** Install PyTorch with CUDA support first:
>
> ```bash
> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
> ```
>
> Then install the rest:
>
> ```bash
> pip install -r requirements.txt
> ```

### 4. (Optional) Install xformers for lower VRAM usage

```bash
pip install xformers
```

---

## How to Run

```bash
python app.py
```

- The model downloads automatically on first run (~5 GB).
- Once loaded, open **http://localhost:5000** in your browser.
- Type a prompt, choose a style, and click **Generate**.

---

## System Requirements

| Component    | Minimum                         | Recommended |
| ------------ | ------------------------------- | ----------- |
| **RAM**      | 8 GB                            | 16 GB       |
| **GPU VRAM** | 4 GB (with attention slicing)   | 8+ GB       |
| **CPU-only** | Works but slow (~3-5 min/image) | —           |
| **Disk**     | ~7 GB (model weights + deps)    | 10 GB       |
| **Python**   | 3.10+                           | 3.11        |

---

## Suggested Improvements for v2

1. **Batch generation** — generate multiple images per prompt and let users pick
2. **Negative prompts** — add a field for things to exclude from the image
3. **Image-to-Image** — accept an input image and transform it
4. **Adjustable parameters** — UI sliders for inference steps, guidance scale, seed
5. **Gallery view** — browse and manage all previously generated images
6. **ControlNet support** — pose/edge-guided generation
7. **SDXL upgrade** — switch to Stable Diffusion XL for higher quality
8. **User authentication** — add login to manage personal galleries
9. **Queue system** — handle concurrent requests with Celery/Redis
10. **Docker deployment** — one-command containerised setup

---

## License

MIT
