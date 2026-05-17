# PDF and carousel generation notes

## Primary method

Use the local [Rowan quote-card generator](../tools/rowan-quote-cards/).

It creates deterministic PNG slides and optional multipage PDF carousels. This is preferred over image generation because exact text, brand colors, and repeatable iteration matter more than novelty.

## Carousel command

Create a slide JSON file, then run:

```bash
python3 tools/rowan-quote-cards/scripts/make_quote_card.py \
  --slides-json examples/carousel-slides.example.json \
  --output-dir output/carousel \
  --pdf-output output/rowan-carousel.pdf \
  --basename rowan-carousel
```

This creates numbered PNG slides plus a multipage PDF.

## Recommended output sizes

- Square: 1080 × 1080
- Feed / portrait / 4:5: 1080 × 1350
- Story: 1080 × 1920
- Landscape: 1200 × 630

Most Rowan carousel slides should use 4:5 unless the channel needs something else.

## QA checklist

Before sharing a PDF or carousel:

- Text is exact
- No spelling errors
- No clipped text
- Lines are tight but not overlapping
- The card reads at phone-feed size
- Color contrast follows Rowan rules
- Attribution, if used, is readable but secondary
- No Rowan logo/name appears unless requested
- PNGs open correctly
- PDF opens correctly and page order is right

## Fallback methods

- HTML/CSS screenshots are useful for complex layouts
- SVG is useful for editable sources, but local rendering can vary
- PDF/vector export can work for production pipelines
- Image generation is not recommended for exact text cards

## What does not belong here

Tax forms, government PDFs, customer documents, private contracts, and API-driven PDF workflows do not belong in the public brand repo.
