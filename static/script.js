/**
 * AI Image Generator — Frontend Logic
 * ====================================
 * Handles prompt submission, loading state, error display,
 * and image preview / download.
 */

// ── DOM References ──────────────────────────────────
const promptEl    = document.getElementById("prompt");
const styleEl     = document.getElementById("style");
const genBtn      = document.getElementById("generate-btn");
const btnText     = genBtn.querySelector(".btn-text");
const btnLoader   = genBtn.querySelector(".btn-loader");
const errorMsg    = document.getElementById("error-msg");
const resultCard  = document.getElementById("result-card");
const resultImage = document.getElementById("result-image");
const genTime     = document.getElementById("gen-time");
const downloadBtn = document.getElementById("download-btn");

// ── Generate Image ──────────────────────────────────
async function generateImage() {
  const prompt = promptEl.value.trim();
  const style  = styleEl.value;

  // --- Validate ----------------------------------------------------------
  if (!prompt) {
    showError("Please enter a prompt before generating.");
    promptEl.focus();
    return;
  }

  // --- UI: loading state -------------------------------------------------
  hideError();
  setLoading(true);
  resultCard.classList.add("hidden");

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, style }),
    });

    const data = await res.json();

    if (!res.ok || !data.success) {
      showError(data.error || "Something went wrong. Please try again.");
      return;
    }

    // --- Display result ----------------------------------------------------
    resultImage.src = data.image_url;
    genTime.textContent = `⏱ ${data.time}s`;
    downloadBtn.href = data.image_url;
    downloadBtn.download = `ai-${Date.now()}.png`;
    resultCard.classList.remove("hidden");

    // Smooth scroll to the result
    resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });

  } catch (err) {
    console.error(err);
    showError("Network error — is the server running?");
  } finally {
    setLoading(false);
  }
}

// ── Helpers ─────────────────────────────────────────

function setLoading(on) {
  genBtn.disabled = on;
  btnText.classList.toggle("hidden", on);
  btnLoader.classList.toggle("hidden", !on);
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove("hidden");
}

function hideError() {
  errorMsg.classList.add("hidden");
}

// ── Keyboard Shortcut (Ctrl/Cmd + Enter) ────────────
promptEl.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    generateImage();
  }
});
