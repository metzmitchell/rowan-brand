# Production Method Notes

Primary method: local Python + Pillow.

Reasons:
- Deterministic
- Runs locally without external services
- Fast iteration
- Exact text control
- No external auth, rate limits, or browser fragility

Fallbacks:
- SVG is useful as a future editable source format, but local renderers are inconsistent.
- HTML/CSS screenshots are good for complex layouts, but browser/Playwright state can be brittle.
- PDF/vector export via PyMuPDF is possible, but less natural for quick social cards.
- Image generation or MCP design tools are not recommended for text-card rendering because exact copy and brand consistency matter more than novelty.

Default output:
- PNG
- 1080x1080 square unless user asks for portrait/story/landscape
- Save outputs under `output/` unless the user names a destination
