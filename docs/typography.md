# Rowan typography

## Font stack

| Use | Font |
|---|---|
| H1-H3 | Times New Roman MT Ultra Bold |
| H4 / optional display label | Poppins Ultra Bold |
| Body | Livvic Regular |
| Buttons | Poppins Regular |

## Fallbacks

Use licensed fonts when available.

If Times New Roman MT Ultra Bold is unavailable, use the closest available heavy Times New Roman face. For generated PDFs and social cards, Times New Roman Bold is acceptable as a fallback.

The public repo does not include proprietary font binaries. See `assets/fonts/README.md`.

## Type color

- On Shell backgrounds, use dark green family colors for headings and body
- On dark backgrounds, use Shell for all type
- Pink and other accent colors are not body-text colors

## Scale and hierarchy

- Page and section titles can be extremely large
- Pair large headlines with smaller supporting copy
- Use generous spacing around big type
- Use tight but readable editorial leading for quote cards
- Avoid crowded typography

## Buttons

- Use Poppins Regular
- Keep labels short
- Prioritize contrast over decoration

## Quote-card typography

The quote-card generator uses:

- Times New Roman MT Ultra Bold for main statements
- Times New Roman Regular for secondary rhythm
- Times New Roman Italic for restrained emphasis
- A small sans-serif attribution when needed

Use `*asterisks*` for italic, `_underscores_` for regular, and the generator's double-bracket accent markup for accent-color spans in generated cards.
