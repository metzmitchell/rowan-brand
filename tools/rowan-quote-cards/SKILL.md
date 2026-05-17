---
name: rowan-quote-cards
description: Generate bold, simple Rowan-branded quote cards, 4:5 social cards, carousel PNG sets, and multipage PDF carousels. Use when generating quote cards, carousel opener cards, social share cards, typographic graphics, Rowan dark green/purple/off-white/pink quote images, bullet-list cards, or reusable image generation for short text. Produces deterministic PNG/JPG/PDF outputs using Rowan colors, Times New Roman MT Ultra Bold, Times regular/italic, accent-color spans, optional small sans-serif attribution, and minimal editorial design without logos unless requested.
---

# Rowan Quote Cards

Use this skill to create reliable typographic social cards for Rowan.

Default stance: **do not use image generation**. Use the local Pillow generator first because exact text, brand colors, and repeatable iteration matter more than novelty.

## Quick workflow

1. Read `references/design-system.md` if you need design judgment or variant choice.
2. Run `scripts/make_quote_card.py` with the text, variant, size, and output path.
3. QA the image with the `image` tool before delivering.
4. Iterate by changing variant, manual line breaks, italic markers, attribution, bullets, accent, margin, or leading.

## Single-card command

```bash
python3 "tools/rowan-quote-cards/scripts/make_quote_card.py" \
  --text 'Comfort can look like wisdom right up until it becomes *decay*.' \
  --variant purple \
  --size 4x5 \
  --leading 0.99 \
  --output "output/quote-card.png"
```

Use `*asterisks*` inside `--text` for Times New Roman italic emphasis, `_underscores_` for Times regular, the generator's double-bracket accent markup for accent-color text, and `~tildes~` for a restrained underline.

Manual line breaks are allowed when the card needs exact composition:

```bash
--text $'Comfort can look\nlike wisdom\nright up until\nit becomes *decay*.'
```

## Common options

- `--size square` → 1080x1080
- `--size 4x5` / `portrait` / `feed` → 1080x1350
- `--size story` → 1080x1920
- `--size landscape` → 1200x630
- `--size WIDTHxHEIGHT` → custom
- `--variant dark-statement|logo-green|purple|dark-purple|shell-editorial|offwhite-green|offwhite-purple|warm-insight|pink-on-dark|white-panel|shell-panel`
- `--accent none|rule|corner|dots|quote-mark|pill`
- `--attribution "Daniel Priestley"` for small sans-serif attribution
- `--bullets 'Point one|Point two|Point three'` for designed bullet cards
- `--kicker "SMALL LABEL"` for an optional top label
- `--subtext "optional secondary text"` for smaller serif context
- `--align center|left|auto`
- `--margin 0.10` to control text breathing room
- `--leading 0.99` is the default tight editorial spacing with a little breathing room. Use `0.98-1.02` for most cards.
- `--font-scale 0.90` makes carousel text calmer and avoids awkward line breaks. Use `1.0+` only for deliberate big opener cards.
- `--accent-color blush` can make an ultra-bold accent word use the muted lighter pink, but avoid it for small or low-contrast text.
- `--crop-word "3"` for a huge low-opacity cropped word/number. Do not use `ROWAN` unless Mitch asks.

## Carousel command

Create a JSON list of slide objects. Any single-card option can be set per slide.

```json
[
  {"text":"Old systems survive because one good person absorbs the *pain*.","variant":"purple","size":"4x5"},
  {"text":"The fix is boring, visible structure.","variant":"offwhite-green","size":"4x5","bullets":"Document the workflow|Name the owner|Review it monthly"},
  {"text":"Comfort can look like wisdom right up until it becomes *decay*.","variant":"pink-on-dark","size":"4x5"}
]
```

Then run:

```bash
python3 "tools/rowan-quote-cards/scripts/make_quote_card.py" \
  --slides-json "/path/to/carousel.json" \
  --output-dir "/path/to/pngs" \
  --pdf-output "/path/to/carousel.pdf" \
  --basename rowan-carousel
```

This creates numbered PNG files plus a multipage PDF.

Most carousel slides should be slightly smaller than standalone quote cards. The carousel renderer defaults unscaled slides to `font_scale: 0.92`; set `"font_scale": 1.05` only for a big opener slide.

## Variant guidance

Default choices:
- Strong or contrarian quote: `dark-statement`, `purple`, or `dark-purple`
- Website-color variety: `purple`, `offwhite-purple`, `offwhite-green`, `pink-on-dark`
- Evergreen editorial quote: `shell-editorial`
- High-brand/simple card: `logo-green`
- Human/practical insight: `warm-insight`
- More polished carousel slide: `white-panel` or `shell-panel`

Avoid logos, handles, Rowan name, and taglines unless Mitch explicitly asks. These cards should usually contain only the text and very light design work.

## Design rules

Core rules live in `references/design-system.md`.

Keep the visible output:
- Bold
- Extremely simple
- Solid Rowan colors
- Large serif type
- Tight editorial leading
- One accent at most

Color freedom is allowed inside the Rowan palette:
- Purple background with Shell text is good
- Off-white background with green or purple text is good
- Pink text is allowed only when it is Ultra Bold on a very dark background
- Do not use pink text on logo-green, off-white, or light backgrounds
- Do not use pink highlight boxes. Highlighting is intentionally not part of this skill.
- On Shell/off-white backgrounds, create variety with green/purple accent-color words, regular text, italics, and tasteful underline.

## QA before delivery

Always check:
- Text is exact and spelled correctly
- Text is not clipped
- Lines are tight but not overlapping
- Same-line words share a baseline
- It reads at phone-feed size
- Color contrast follows Rowan rules
- Attribution, when used, is small sans-serif and readable
- Bullet marks look intentional, not like default bullets
- No Rowan logo/name/tag appears unless requested
- Output PNG/PDF opens correctly

Use the `image` tool for a quick visual QA pass.

## Method notes

See `references/method-notes.md` for the production-method research. Short version: Pillow is the primary path; HTML/CSS, SVG, PDF, MCP, and image generation are fallbacks only when the user asks for something outside the deterministic generator.
