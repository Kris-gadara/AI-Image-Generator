<p align="center">
  <img src="https://img.icons8.com/fluency/96/image.png" width="80" alt="logo" />
</p>

<h1 align="center">AI Image Generator</h1>

<p align="center">
  <strong>Transform text prompts into stunning visuals — powered by Stable Diffusion XL</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Model-SDXL%201.0-blueviolet?style=for-the-badge" alt="SDXL" />
  <img src="https://img.shields.io/badge/API-Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="HF API" />
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#live-demo">Live Demo</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#api-reference">API</a> •
  <a href="#project-structure">Structure</a> •
  <a href="#contributing">Contributing</a>
</p>

---

## Live Demo

<p align="center">
  <img src="images/Screenshot 2026-02-25 132722.png" alt="AI Image Generator — Prompt Interface" width="100%" />
</p>

<p align="center">
  <img src="images/Screenshot 2026-02-25 133018.png" alt="AI Image Generator — Generated Result" width="100%" />
</p>

---

## Features

| Feature                   | Description                                                                   |
| ------------------------- | ----------------------------------------------------------------------------- |
| 🎨 **Text-to-Image**      | Generate images from any text description using **Stable Diffusion XL 1.0**   |
| 🌐 **Cloud Inference**    | Uses Hugging Face Inference API — no GPU or large downloads required          |
| 🎬 **Style Presets**      | Choose from **Cinematic**, **Anime**, **Realistic**, and **Cyberpunk** styles |
| 💾 **Auto-Save**          | Every generated image is saved to `generated_images/`                         |
| ⬇️ **One-Click Download** | Download your creations instantly as PNG                                      |
| ⌨️ **Keyboard Shortcut**  | Press `Ctrl + Enter` to generate instantly                                    |
| 🌙 **Premium Dark UI**    | Glassmorphism design with animated gradient orbs                              |
| 📱 **Responsive**         | Works beautifully on desktop, tablet, and mobile                              |

---

## Tech Stack

<table>
  <tr>
    <td align="center" width="120"><strong>Backend</strong></td>
    <td>Python 3.10+ &bull; Flask 3.0 &bull; Requests &bull; Pillow</td>
  </tr>
  <tr>
    <td align="center" width="120"><strong>AI Model</strong></td>
    <td>Stable Diffusion XL 1.0 via 🤗 Hugging Face Inference API</td>
  </tr>
  <tr>
    <td align="center" width="120"><strong>Frontend</strong></td>
    <td>Vanilla HTML/CSS/JS &bull; Inter font &bull; Glassmorphism UI</td>
  </tr>
</table>

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kris-gadara/AI-Image-Generator.git
cd AI-Image-Generator
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Hugging Face token

Get a free token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens), then set it as an environment variable:

```bash
# Windows (PowerShell)
$env:HF_TOKEN = "hf_your_token_here"

# macOS / Linux
export HF_TOKEN="hf_your_token_here"
```

### 5. Run the app

```bash
python app.py
```

Open your browser and navigate to **http://localhost:5000** 🚀

---

## Usage

1. **Enter a prompt** — Describe the image you want to create  
   _Example:_ `A futuristic city floating in the clouds at sunset, ultra detailed`

2. **Pick a style** _(optional)_ — Choose from the dropdown:
   - 🎬 **Cinematic** — Film-like lighting with dramatic atmosphere
   - 🌸 **Anime** — Studio Ghibli / manga aesthetic
   - 📷 **Realistic** — Photorealistic DSLR-quality output
   - 🌃 **Cyberpunk** — Neon-lit futuristic visuals

3. **Click Generate** or press **Ctrl + Enter**

4. **Download** your image with one click

---

## API Reference

### `POST /generate`

Generate an image from a text prompt.

**Request Body:**

```json
{
  "prompt": "A majestic mountain landscape at golden hour",
  "style": "cinematic"
}
```

| Parameter | Type   | Required | Description                                                          |
| --------- | ------ | -------- | -------------------------------------------------------------------- |
| `prompt`  | string | ✅       | Text description of the image                                        |
| `style`   | string | ❌       | Style preset: `none`, `cinematic`, `anime`, `realistic`, `cyberpunk` |

**Response:**

```json
{
  "success": true,
  "image_url": "/images/a1b2c3d4.png",
  "time": 8.42
}
```

### `GET /images/<filename>`

Serve a previously generated image.

---

## Project Structure

```
AI-Image-Generator/
├── app.py                  # Flask backend + HF API integration
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── images/                 # Screenshots for README
│   ├── Screenshot 2026-02-25 132722.png
│   └── Screenshot 2026-02-25 133018.png
├── static/
│   ├── styles.css          # Premium glassmorphism dark theme
│   └── script.js           # Frontend logic (fetch, UI state)
├── templates/
│   └── index.html          # Main UI template
└── generated_images/       # Output folder (auto-created)
```

---

## Environment Variables

| Variable   | Required    | Description                                                              |
| ---------- | ----------- | ------------------------------------------------------------------------ |
| `HF_TOKEN` | Recommended | Hugging Face API token for authenticated requests and higher rate limits |

---

## Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m "Add amazing feature"`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Kris-gadara"><strong>Kris Gadara</strong></a>
</p>

<p align="center">
  <sub>Powered by <strong>Stable Diffusion XL 1.0</strong> &bull; Built with Flask & 🤗 Hugging Face Inference API</sub>
</p>
