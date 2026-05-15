# Rowan quote-card and carousel generator

Local deterministic generator for Rowan-branded quote cards, carousel PNG sets, and multipage PDF carousels.

Start with `SKILL.md` for usage.

## Quick test

```bash
python3 tools/rowan-quote-cards/scripts/make_quote_card.py \
  --text 'Comfort can look like wisdom right up until it becomes *decay*.' \
  --variant purple \
  --size 4x5 \
  --output output/quote-card.png
```

## PDF carousel

```bash
python3 tools/rowan-quote-cards/scripts/make_quote_card.py \
  --slides-json examples/carousel-slides.example.json \
  --output-dir output/carousel \
  --pdf-output output/rowan-carousel.pdf \
  --basename rowan-carousel
```
