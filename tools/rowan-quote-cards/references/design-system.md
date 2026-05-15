# Rowan Quote Card Design System

## Direction

Create bold, extremely simple editorial cards. The typography is the design.

Use:
- Solid Rowan color fields
- Huge Times New Roman MT Ultra Bold headlines
- Times New Roman regular or italic for secondary rhythm
- Small sans-serif attribution when needed
- Tight editorial line spacing with a little breathing room, usually `--leading 0.98-1.02`
- Generous outer margins
- One light design detail at most

Avoid:
- Gradients unless explicitly photo-overlay
- Busy texture
- Stock illustration
- Heavy frames
- Multiple badges
- Multiple accent colors fighting each other
- Pink highlight boxes
- Drop shadows as a core effect
- Logos, handles, or Rowan name unless the user asks
- Tiny serif attribution

## Rowan palette

- Shell: `#f5f2e8`
- White: `#f8f7f4`
- Logo Green: `#485e3d`
- Dark Green: `#1c201b`
- Light Accent: `#d4c7b1`
- Pink: `#a66c6c`
- Dark Pink: `#744b4b`
- Purple: `#392540`
- Darkest Purple: `#19161e`
- Blush Accent: `#d9b8ad` only for occasional ultra-bold accent text, never a highlight box

## Allowed color variety

Use more of the website palette than the website itself does. Stay solid and simple.

Good combinations:
- Dark Green background + Shell text
- Logo Green background + Shell text
- Purple background + Shell text
- Darkest Purple background + Shell text
- Shell background + Dark Green text
- Shell background + Logo Green text
- Shell background + Purple text
- Light Accent background + Dark Green text
- Very dark background + bold Pink headline text

Rules:
- Pink text only works when it is Ultra Bold on a very dark background
- Do not use pink text on logo-green, off-white, or light backgrounds
- Pink should not be used for small body text
- Do not use pink highlight boxes
- On Shell/off-white backgrounds, use green/purple font-color changes for accent words
- The blush accent may be used for one ultra-bold word only when contrast is strong enough
- Shell/off-white text belongs on dark solid backgrounds
- Green or purple text belongs on off-white backgrounds
- Keep each card to 2 core colors plus 1 restrained accent

## Variants in the generator

- `dark-statement`: Dark Green background, Shell text, small pink/light accent
- `logo-green`: Logo Green background, Shell text
- `purple`: Purple background, Shell text
- `dark-purple`: Darkest Purple background, Shell text
- `shell-editorial`: Shell background, Dark Green text
- `offwhite-green`: Shell background, Logo Green text
- `offwhite-purple`: Shell background, Purple text
- `warm-insight`: Light Accent background, Dark Green text
- `pink-on-dark`: Dark Green background, Pink Ultra Bold headline text
- `white-panel`: Dark Green field with light inset panel
- `shell-panel`: Shell field with White inset panel

## Typography

Main quote:
- Times New Roman MT Ultra Bold
- Very large
- Tight line height
- Centered or left-aligned

Regular secondary text:
- Times New Roman Regular
- Smaller than quote
- Use sparingly

Italic emphasis:
- Times New Roman Italic
- Use for one word or phrase marked with `*asterisks*`
- Same color as surrounding text unless the user asks otherwise

Accent-color spans:
- Use `[[accent text]]` to change the font color, not to draw a highlight box
- On Shell/off-white, default accent words should usually be Green or Purple
- Use `--accent-color blush` only for a single Ultra Bold accent word with strong contrast
- Use `~underlined text~` for a restrained editorial underline when the card needs extra rhythm
- Combine sparingly with regular or italic text so Ultra Bold still carries the card

Attribution:
- Small sans-serif
- Use `--attribution "Daniel Priestley"`
- Keep it readable but clearly secondary
- Do not use serif attribution for quote sources unless asked

## Layout patterns

1. Centered Quote Block
	- Center a large quote block
	- 2-6 lines
	- Optional small rule or dot

2. Kicker + Giant Headline
	- Small uppercase kicker near top
	- Giant centered statement below
	- Optional subline

3. Top-Left Editorial
	- Large left-aligned text in upper-left
	- Strong negative space
	- Optional small lower note or dots

4. Giant Cropped Word/Number
	- Huge background word or number cropped off one edge
	- Quote remains foreground
	- Low opacity only

5. Pill Callout
	- One rounded pill label
	- Small uppercase text
	- Use below or above main quote

6. Bullet Card
	- Use `--bullets 'One|Two|Three'`
	- Bullet marks should be designed elements, not default text bullets
	- Current design: outlined circle + center dot + short rule
	- Bullet copy should be short and readable

## Text fitting

- Ideal quote length: 8-22 words
- Acceptable: 23-32 words
- Split longer text across carousel slides if possible
- Prefer 2-6 lines
- Keep margins at 8-12% of canvas width
- Default leading is tight but not cramped: `0.99`
- Use `0.98-1.02` for most cards
- Use `1.00+` only if descenders/caps feel too cramped

If text does not fit:
1. Reduce font size gradually with `--font-scale`, especially for carousel slides
2. Add intentional manual line breaks only when the semantic phrase break is obvious
3. Remove optional accent
4. Split into multiple carousel slides

## Carousel output

Use `--slides-json` for multi-slide sets.

Required outputs for carousels when requested:
- Multiple numbered PNGs
- One multipage PDF if `--pdf-output` is provided

Default carousel size: `4x5` unless the user asks otherwise.

Default carousel feel:
- First/opener slide can use big type: `font_scale: 1.0-1.08`
- Most follow-up slides should be slightly smaller: `font_scale: 0.88-0.94`
- Do not force weird manual line breaks. Let the balanced wrapper choose lines unless a break is semantically obvious.

## QA checklist

- Text is exact and spelled correctly
- No clipping
- Same-line words share a baseline
- Leading is tight, artful, and not overlapping
- Quote is readable at phone-feed size
- Attribution is small sans-serif when used
- Bullet marks look intentional and branded
- Color contrast follows Rowan pairing rules
- Pink is either Ultra Bold headline/accent text on a very dark background or omitted
- No pink highlight boxes
- No logo, Rowan name, or tag unless requested
- PNGs and PDF open correctly
