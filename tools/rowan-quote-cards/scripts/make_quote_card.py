#!/usr/bin/env python3
"""Generate deterministic Rowan quote cards with Pillow."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

PALETTE = {
    "shell": "#f5f2e8",
    "white": "#f8f7f4",
    "logo_green": "#485e3d",
    "dark_green": "#1c201b",
    "light_accent": "#d4c7b1",
    "pink": "#a66c6c",
    "dark_pink": "#744b4b",
    "blush": "#d9b8ad",
    "purple": "#392540",
    "darkest_purple": "#19161e",
}

SIZES = {
    "square": (1080, 1080),
    "4x5": (1080, 1350),
    "four-five": (1080, 1350),
    "portrait": (1080, 1350),
    "feed": (1080, 1350),
    "story": (1080, 1920),
    "landscape": (1200, 630),
}

VARIANTS = {
    "dark-statement": {"background": "dark_green", "text": "shell", "muted": "light_accent", "accent": "pink", "panel": None},
    "logo-green": {"background": "logo_green", "text": "shell", "muted": "light_accent", "accent": "light_accent", "panel": None},
    "purple": {"background": "purple", "text": "shell", "muted": "light_accent", "accent": "pink", "panel": None},
    "dark-purple": {"background": "darkest_purple", "text": "shell", "muted": "light_accent", "accent": "pink", "panel": None},
    "shell-editorial": {"background": "shell", "text": "dark_green", "muted": "logo_green", "accent": "purple", "panel": None},
    "offwhite-green": {"background": "shell", "text": "logo_green", "muted": "dark_green", "accent": "purple", "panel": None},
    "offwhite-purple": {"background": "shell", "text": "purple", "muted": "dark_green", "accent": "logo_green", "panel": None},
    "warm-insight": {"background": "light_accent", "text": "dark_green", "muted": "logo_green", "accent": "dark_pink", "panel": None},
    "pink-on-dark": {"background": "dark_green", "text": "pink", "muted": "shell", "accent": "light_accent", "panel": None},
    "white-panel": {"background": "dark_green", "text": "dark_green", "muted": "logo_green", "accent": "purple", "panel": "shell"},
    "shell-panel": {"background": "shell", "text": "dark_green", "muted": "logo_green", "accent": "purple", "panel": "white"},
}

TOKEN_RE = re.compile(r"(\[\[[\s\S]*?\]\]|~[^~]+~|\*[^*]+\*|_[^_]+_|\n)")


@dataclass(frozen=True)
class Token:
    text: str
    style: str  # bold | italic | regular
    accent: bool = False
    underline: bool = False


@dataclass
class FontSet:
    bold: ImageFont.FreeTypeFont
    regular: ImageFont.FreeTypeFont
    italic: ImageFont.FreeTypeFont


def hex_to_rgb(value: str) -> Tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def color(name: str, alpha: int | None = None):
    rgb = hex_to_rgb(PALETTE[name])
    return (*rgb, alpha) if alpha is not None else rgb


def size_from_arg(value: str) -> Tuple[int, int]:
    if value in SIZES:
        return SIZES[value]
    match = re.fullmatch(r"(\d{3,5})x(\d{3,5})", value)
    if not match:
        raise argparse.ArgumentTypeError("size must be square, 4x5, portrait, story, landscape, or WIDTHxHEIGHT")
    return int(match.group(1)), int(match.group(2))


def load_font(path: Path | str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size, index=index)


def resolve_fonts(size: int) -> FontSet:
    ultra = ASSETS / "Times New Roman MT Extra Bold.ttf"
    bold = load_font(ultra, size) if ultra.exists() else load_font("/System/Library/Fonts/Times.ttc", size, index=1)

    def first(candidates):
        for path, index in candidates:
            try:
                if Path(path).exists():
                    return load_font(path, size, index=index)
            except Exception:
                continue
        return bold

    regular = first([
        ("/System/Library/Fonts/Times.ttc", 0),
        ("/System/Library/Fonts/NewYork.ttf", 0),
        ("/System/Library/Fonts/Helvetica.ttc", 0),
    ])
    italic = first([
        ("/System/Library/Fonts/Times.ttc", 2),
        ("/System/Library/Fonts/NewYorkItalic.ttf", 0),
        ("/System/Library/Fonts/Times.ttc", 0),
    ])
    return FontSet(bold=bold, regular=regular, italic=italic)


def resolve_sans(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        ("/System/Library/Fonts/Avenir Next.ttc", 1 if bold else 0),
        ("/System/Library/Fonts/HelveticaNeue.ttc", 1 if bold else 0),
        ("/System/Library/Fonts/Helvetica.ttc", 1 if bold else 0),
        ("/System/Library/Fonts/SFNS.ttf", 0),
    ]
    for path, index in candidates:
        try:
            if Path(path).exists():
                return load_font(path, size, index=index)
        except Exception:
            continue
    return resolve_fonts(size).regular


def parse_tokens(text: str, default_style: str = "bold", accent: bool = False, underline: bool = False) -> List[Token]:
    """Parse lightweight inline styling.

    Default text is Ultra Bold. Use:
    - *italic* for Times italic
    - _regular_ for Times regular
    - [[accent text]] for a second font color, not a highlight box
    - ~underlined text~ for a restrained editorial underline
    Markers can be combined inside accent spans, e.g. [[*italic accent*]].
    """
    tokens: List[Token] = []
    for part in TOKEN_RE.split(text or ""):
        if not part:
            continue
        if part == "\n":
            tokens.append(Token("\n", default_style, accent, underline))
            continue
        if part.startswith("[[") and part.endswith("]]"):
            tokens.extend(parse_tokens(part[2:-2], default_style=default_style, accent=True, underline=underline))
            continue
        style = default_style
        clean = part
        token_underline = underline
        if part.startswith("*") and part.endswith("*"):
            style = "italic"
            clean = part[1:-1]
        elif part.startswith("_") and part.endswith("_"):
            style = "regular"
            clean = part[1:-1]
        elif part.startswith("~") and part.endswith("~"):
            clean = part[1:-1]
            token_underline = True
        chunks = re.split(r"(\n)", clean)
        for chunk in chunks:
            if chunk == "\n":
                tokens.append(Token("\n", style, accent, token_underline))
                continue
            for word in chunk.split():
                if tokens and re.fullmatch(r"[.,!?;:]+", word):
                    previous = tokens[-1]
                    tokens[-1] = Token(previous.text + word, previous.style, previous.accent, previous.underline)
                else:
                    tokens.append(Token(word, style, accent, token_underline))
    return tokens


def font_for(token: Token, fonts: FontSet) -> ImageFont.FreeTypeFont:
    if token.style == "italic":
        return fonts.italic
    if token.style == "regular":
        return fonts.regular
    return fonts.bold


def text_bbox(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont):
    return draw.textbbox((0, 0), text, font=font)


def token_width(draw: ImageDraw.ImageDraw, token: Token, fonts: FontSet) -> int:
    bbox = text_bbox(draw, token.text, font_for(token, fonts))
    return bbox[2] - bbox[0]


def space_width(draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont) -> int:
    bbox = text_bbox(draw, " ", font)
    return bbox[2] - bbox[0]


def wrap_tokens(draw: ImageDraw.ImageDraw, tokens: Sequence[Token], fonts: FontSet, max_width: int) -> List[List[Token]]:
    lines: List[List[Token]] = []
    current: List[Token] = []
    for token in tokens:
        if token.text == "\n":
            if current:
                lines.extend(wrap_paragraph(draw, current, fonts, max_width))
            current = []
            continue
        current.append(token)
    if current:
        lines.extend(wrap_paragraph(draw, current, fonts, max_width))
    return lines


def line_width(draw: ImageDraw.ImageDraw, line: Sequence[Token], fonts: FontSet) -> int:
    width = 0
    for i, token in enumerate(line):
        if i:
            width += space_width(draw, font_for(token, fonts))
        width += token_width(draw, token, fonts)
    return width


def wrap_paragraph(draw: ImageDraw.ImageDraw, paragraph: Sequence[Token], fonts: FontSet, max_width: int) -> List[List[Token]]:
    """Wrap one paragraph with balanced line breaks instead of greedy breaks."""
    n = len(paragraph)
    if n == 0:
        return []
    widths: dict[tuple[int, int], int] = {}
    for i in range(n):
        line: List[Token] = []
        for j in range(i, n):
            line.append(paragraph[j])
            w = line_width(draw, line, fonts)
            if w > max_width and j > i:
                break
            widths[(i, j + 1)] = w

    inf = 10**18
    dp = [inf] * (n + 1)
    nxt = [n] * (n + 1)
    dp[n] = 0
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            w = widths.get((i, j))
            if w is None:
                continue
            remaining = max_width - w
            words = j - i
            is_last = j == n
            ragged = (remaining / max_width) ** 2
            cost = ragged * (8 if is_last else 100)
            if words == 1 and n > 3:
                cost += 220 if is_last else 45
            if words == 2 and is_last and n > 7:
                cost += 24
            total = cost + dp[j]
            if total < dp[i]:
                dp[i] = total
                nxt[i] = j

    if dp[0] >= inf:
        return [[token] for token in paragraph]
    lines: List[List[Token]] = []
    i = 0
    while i < n:
        j = nxt[i]
        lines.append(list(paragraph[i:j]))
        i = j
    return lines


def common_metrics(fonts: FontSet) -> Tuple[int, int, int]:
    ascents, descents = [], []
    for font in (fonts.bold, fonts.regular, fonts.italic):
        ascent, descent = font.getmetrics()
        ascents.append(ascent)
        descents.append(descent)
    max_ascent = max(ascents)
    max_descent = max(descents)
    return max_ascent, max_descent, max_ascent + max_descent


def block_metrics(draw: ImageDraw.ImageDraw, lines: Sequence[Sequence[Token]], fonts: FontSet, leading: float) -> Tuple[int, int, int]:
    widths = [line_width(draw, line, fonts) for line in lines] or [0]
    if not lines:
        return 0, 0, 0
    ascent, descent, full_height = common_metrics(fonts)
    line_step = max(1, int(fonts.bold.size * leading))
    total_height = full_height + line_step * (len(lines) - 1)
    return max(widths), total_height, line_step


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, max_height: int, min_size: int, max_size: int, leading: float, default_style="bold"):
    for size in range(max_size, min_size - 1, -2):
        fonts = resolve_fonts(size)
        lines = wrap_tokens(draw, parse_tokens(text, default_style), fonts, max_width)
        width, height, _ = block_metrics(draw, lines, fonts, leading)
        if width <= max_width and height <= max_height and len(lines) <= 8:
            return fonts, lines, width, height
    fonts = resolve_fonts(min_size)
    lines = wrap_tokens(draw, parse_tokens(text, default_style), fonts, max_width)
    width, height, _ = block_metrics(draw, lines, fonts, leading)
    return fonts, lines, width, height


def draw_text_block(
    draw: ImageDraw.ImageDraw,
    lines: Sequence[Sequence[Token]],
    fonts: FontSet,
    box: Tuple[int, int, int, int],
    fill,
    align="center",
    leading=0.98,
    accent_fill=None,
):
    x1, y1, x2, y2 = box
    _, block_h, line_step = block_metrics(draw, lines, fonts, leading)
    ascent, descent, _ = common_metrics(fonts)
    top = y1 + max(0, (y2 - y1 - block_h) // 2)
    accent_fill = accent_fill or fill
    for idx, line in enumerate(lines):
        lw = line_width(draw, line, fonts)
        baseline = top + ascent + idx * line_step
        x = x1 if align == "left" else x1 + (x2 - x1 - lw) / 2
        for i, token in enumerate(line):
            if i:
                x += space_width(draw, font_for(token, fonts))
            font = font_for(token, fonts)
            bbox = text_bbox(draw, token.text, font)
            token_w = bbox[2] - bbox[0]
            token_fill = accent_fill if token.accent else fill
            draw.text((x, baseline), token.text, font=font, fill=token_fill, anchor="ls")
            if token.underline:
                actual = draw.textbbox((x, baseline), token.text, font=font, anchor="ls")
                y = int(baseline + max(5, font.size * 0.055))
                width = max(2, int(font.size * 0.035))
                draw.line((int(actual[0]), y, int(actual[2]), y), fill=token_fill, width=width)
            x += token_w


def draw_accent(draw: ImageDraw.ImageDraw, kind: str, variant: dict, W: int, H: int, panel_box: Tuple[int, int, int, int] | None = None, pill_text: str | None = None):
    accent = color(variant["accent"])
    muted = color(variant["muted"])
    x1, y1, x2, y2 = panel_box or (0, 0, W, H)
    if kind == "none":
        return
    if kind == "rule":
        y = y2 - int(H * 0.12)
        draw.line((x1 + int(W * 0.10), y, x1 + int(W * 0.28), y), fill=accent, width=max(4, W // 180))
    elif kind == "corner":
        m = int(W * 0.07)
        l = int(W * 0.13)
        draw.line((m, m, m + l, m), fill=accent, width=max(5, W // 160))
        draw.line((m, m, m, m + l), fill=accent, width=max(5, W // 160))
    elif kind == "dots":
        r = max(5, W // 140)
        gap = r * 4
        cx = W // 2 - gap
        cy = y2 - int(H * 0.09)
        for i in range(3):
            draw.ellipse((cx + i * gap - r, cy - r, cx + i * gap + r, cy + r), fill=muted if i else accent)
    elif kind == "quote-mark":
        fonts = resolve_fonts(int(W * 0.18))
        draw.text((x1 + int(W * 0.06), y1 + int(H * 0.02)), "“", font=fonts.bold, fill=(*accent, 120))
    elif kind == "pill":
        label = (pill_text or "THE POINT").upper()
        f = resolve_sans(max(22, W // 42), bold=True)
        bbox = draw.textbbox((0, 0), label, font=f)
        pad_x, pad_y = int(W * 0.025), int(H * 0.012)
        w, h = bbox[2] - bbox[0] + pad_x * 2, bbox[3] - bbox[1] + pad_y * 2
        px = x1 + int(W * 0.10)
        py = y1 + int(H * 0.09)
        draw.rounded_rectangle((px, py, px + w, py + h), radius=h // 2, fill=muted)
        draw.text((px + pad_x, py + pad_y - bbox[1]), label, font=f, fill=color("dark_green"))


def draw_kicker(draw: ImageDraw.ImageDraw, text: str, variant: dict, W: int, H: int, panel_box=None):
    if not text:
        return
    x1, y1, x2, _ = panel_box or (0, 0, W, H)
    f = resolve_sans(max(22, W // 42), bold=True)
    label = text.upper()
    bbox = draw.textbbox((0, 0), label, font=f)
    y = y1 + int(H * 0.105)
    x = x1 + (x2 - x1 - (bbox[2] - bbox[0])) / 2
    draw.text((x, y - bbox[1]), label, font=f, fill=color(variant["muted"]))


def draw_attribution(draw: ImageDraw.ImageDraw, text: str, variant: dict, W: int, H: int, box: Tuple[int, int, int, int], align="center"):
    if not text:
        return
    x1, y1, x2, y2 = box
    size = max(28, int(min(W, H) * 0.032))
    f = resolve_sans(size, bold=False)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    x = x1 if align == "left" else x1 + (x2 - x1 - tw) / 2
    y = y2 - int(H * 0.095)
    dark_backgrounds = {"dark_green", "logo_green", "purple", "darkest_purple"}
    fill = color("shell", 218) if variant["background"] in dark_backgrounds else color(variant["muted"])
    draw.text((x, y - bbox[1]), text, font=f, fill=fill)


def draw_bullets(draw: ImageDraw.ImageDraw, bullets: Sequence[str], variant: dict, W: int, H: int, box: Tuple[int, int, int, int], align="left"):
    if not bullets:
        return
    x1, y1, x2, y2 = box
    accent = color(variant["accent"])
    text_fill = color(variant["text"])
    base = min(W, H)
    bullet_x = x1
    text_x = x1 + int(W * 0.075)
    max_text_w = x2 - text_x
    min_size = max(28, int(base * 0.031))
    max_size = max(min_size, int(base * 0.046))
    available_h = y2 - y1
    for size in range(max_size, min_size - 1, -2):
        fonts = resolve_fonts(size)
        bullet_gap = int(size * 0.82)
        wrapped = [wrap_tokens(draw, parse_tokens(b, "regular"), fonts, max_text_w) for b in bullets]
        line_step = int(size * 1.02)
        item_heights = [max(line_step, len(lines) * line_step) for lines in wrapped]
        total_h = sum(item_heights) + bullet_gap * (len(bullets) - 1)
        if total_h <= available_h:
            break
    y = y1 + max(0, (y2 - y1 - total_h) // 2)
    for idx, lines in enumerate(wrapped):
        cy = y + int(size * 0.45)
        # Designed bullet: small outlined circle with filled center and short rule.
        r = max(10, int(size * 0.24))
        draw.ellipse((bullet_x, cy - r, bullet_x + 2 * r, cy + r), outline=accent, width=max(3, W // 360))
        inner = max(3, r // 3)
        draw.ellipse((bullet_x + r - inner, cy - inner, bullet_x + r + inner, cy + inner), fill=accent)
        draw.line((bullet_x + 2 * r + int(W * 0.012), cy, text_x - int(W * 0.018), cy), fill=accent, width=max(2, W // 540))
        item_box = (text_x, y - int(size * 0.20), x2, y + item_heights[idx] + int(size * 0.26))
        draw_text_block(draw, lines, fonts, item_box, text_fill, align=align, leading=1.02, accent_fill=accent)
        y += item_heights[idx] + bullet_gap


def split_bullets(raw: str | None) -> List[str]:
    if not raw:
        return []
    return [b.strip() for b in raw.split("|") if b.strip()]


def render_image(args: argparse.Namespace) -> Image.Image:
    W, H = args.size
    variant = VARIANTS[args.variant]
    img = Image.new("RGBA", (W, H), color(variant["background"], 255))
    draw = ImageDraw.Draw(img)

    panel_box = None
    if variant.get("panel"):
        inset = int(min(W, H) * 0.075)
        panel_box = (inset, inset, W - inset, H - inset)
        draw.rounded_rectangle(panel_box, radius=int(min(W, H) * 0.035), fill=color(variant["panel"], 255), outline=color("light_accent"), width=max(2, W // 450))

    if args.crop_word:
        word = args.crop_word.upper()
        f = resolve_fonts(int(W * 0.34)).bold
        fill = color("shell", 32) if variant["background"] in ("dark_green", "logo_green", "purple", "darkest_purple") else color("white", 210)
        draw.text((-int(W * 0.05), H - int(H * 0.25)), word, font=f, fill=fill)

    draw_accent(draw, args.accent, variant, W, H, panel_box, args.pill_text)
    draw_kicker(draw, args.kicker or "", variant, W, H, panel_box)

    x1, y1, x2, y2 = panel_box or (0, 0, W, H)
    margin_x = int(W * args.margin)
    bullets = split_bullets(args.bullets)
    has_lower = bool(args.subtext or args.attribution or bullets)
    top_pad = int(H * (0.15 if args.kicker else 0.10))
    bottom_pad = int(H * (0.64 if bullets else (0.22 if has_lower else 0.12)))
    text_box = (x1 + margin_x, y1 + top_pad, x2 - margin_x, y2 - bottom_pad)

    word_count = len(re.findall(r"\w+", args.text or ""))
    base = min(W, H)
    if word_count <= 8:
        max_size = int(base * 0.145)
    elif word_count <= 18:
        max_size = int(base * 0.112)
    elif word_count <= 32:
        max_size = int(base * 0.086)
    else:
        max_size = int(base * 0.068)
    font_scale = args.font_scale if args.font_scale is not None else 1.0
    max_size = max(34, int(max_size * font_scale))
    min_size = max(34, int(base * 0.042))

    align = args.align
    if align == "auto":
        align = "left" if args.variant in ("white-panel", "shell-panel") or word_count > 18 or bullets else "center"

    if args.text:
        fonts, lines, _, _ = fit_text(draw, args.text, text_box[2] - text_box[0], text_box[3] - text_box[1], min_size, max_size, args.leading)
        accent_name = args.accent_color or variant["accent"]
        draw_text_block(draw, lines, fonts, text_box, color(variant["text"]), align=align, leading=args.leading, accent_fill=color(accent_name))
    else:
        fonts = resolve_fonts(max_size)

    if bullets:
        bullet_box = (x1 + margin_x, y2 - int(H * 0.61), x2 - margin_x, y2 - int(H * 0.08))
        draw_bullets(draw, bullets, variant, W, H, bullet_box)

    if args.subtext:
        sub_size = max(30, int(fonts.bold.size * 0.42))
        sub_fonts = resolve_fonts(sub_size)
        sub_box = (x1 + margin_x, y2 - int(H * 0.19), x2 - margin_x, y2 - int(H * 0.09))
        sub_lines = wrap_tokens(draw, parse_tokens(args.subtext, "regular"), sub_fonts, sub_box[2] - sub_box[0])
        draw_text_block(draw, sub_lines, sub_fonts, sub_box, color(variant["muted"]), align=args.subtext_align, leading=0.98)

    if args.attribution:
        draw_attribution(draw, args.attribution, variant, W, H, (x1 + margin_x, y1, x2 - margin_x, y2), align=args.attribution_align)

    return img


def render(args: argparse.Namespace) -> Path:
    img = render_image(args)
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() in (".jpg", ".jpeg"):
        img.convert("RGB").save(output, quality=95)
    else:
        img.save(output)
    return output


def namespace_from_slide(base_args: argparse.Namespace, slide: dict[str, Any], output: Path) -> argparse.Namespace:
    data = vars(base_args).copy()
    data.update(slide)
    if isinstance(data.get("size"), str):
        data["size"] = size_from_arg(data["size"])
    data["output"] = str(output)
    return argparse.Namespace(**data)


def render_carousel(args: argparse.Namespace) -> List[Path]:
    slides_path = Path(args.slides_json).expanduser()
    slides = json.loads(slides_path.read_text())
    if not isinstance(slides, list) or not slides:
        raise ValueError("slides JSON must be a non-empty list of slide objects")
    out_dir = Path(args.output_dir or args.output or ".").expanduser()
    if out_dir.suffix:
        out_dir = out_dir.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    basename = args.basename or slides_path.stem
    paths: List[Path] = []
    images: List[Image.Image] = []
    for i, slide in enumerate(slides, start=1):
        output = out_dir / f"{basename}-{i:02d}.png"
        if slide.get("font_scale") is None:
            slide = {**slide, "font_scale": 0.92}
        slide_args = namespace_from_slide(args, slide, output)
        img = render_image(slide_args)
        img.save(output)
        paths.append(output)
        images.append(img.convert("RGB"))
    if args.pdf_output:
        pdf = Path(args.pdf_output).expanduser()
        pdf.parent.mkdir(parents=True, exist_ok=True)
        images[0].save(pdf, save_all=True, append_images=images[1:])
        paths.append(pdf)
    return paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Rowan quote cards")
    parser.add_argument("--text", default="", help="Main quote text. Use *asterisks* for italic, _underscores_ for regular, [[brackets]] for accent-color text, and ~tildes~ for underline. Use literal newlines only for intentional manual breaks.")
    parser.add_argument("--output", default=None, help="Output image path (.png/.jpg), or output directory for carousel when --output-dir is omitted")
    parser.add_argument("--variant", choices=sorted(VARIANTS), default="dark-statement")
    parser.add_argument("--size", type=size_from_arg, default=SIZES["square"], help="square, 4x5, portrait, story, landscape, or WIDTHxHEIGHT")
    parser.add_argument("--align", choices=["auto", "center", "left"], default="auto")
    parser.add_argument("--accent", choices=["none", "rule", "corner", "dots", "quote-mark", "pill"], default="none")
    parser.add_argument("--pill-text", default=None)
    parser.add_argument("--kicker", default=None)
    parser.add_argument("--subtext", default=None, help="Optional smaller serif text, such as context. Default: none.")
    parser.add_argument("--subtext-align", choices=["center", "left"], default="center")
    parser.add_argument("--attribution", default=None, help="Small sans-serif attribution, e.g. Daniel Priestley")
    parser.add_argument("--attribution-align", choices=["center", "left"], default="center")
    parser.add_argument("--bullets", default=None, help="Pipe-separated bullets, e.g. 'One|Two|Three'. Uses designed bullet marks.")
    parser.add_argument("--crop-word", default=None, help="Optional huge low-opacity cropped word/number. Do not use ROWAN unless explicitly requested.")
    parser.add_argument("--accent-color", choices=sorted(PALETTE), default=None, help="Override [[accent text]] color. Defaults to the variant accent color.")
    parser.add_argument("--margin", type=float, default=0.10, help="Outer text margin as fraction of width")
    parser.add_argument("--leading", type=float, default=0.99, help="Hero baseline distance as fraction of font size. Default is tight editorial spacing with a little breathing room.")
    parser.add_argument("--font-scale", type=float, default=None, help="Scale hero font size. Use 0.88-0.94 for most carousel slides; 1.0+ for deliberate big opener cards.")
    parser.add_argument("--slides-json", default=None, help="JSON list of slide option objects for carousel generation")
    parser.add_argument("--output-dir", default=None, help="Directory for carousel PNG exports")
    parser.add_argument("--pdf-output", default=None, help="Optional multipage PDF output for carousel")
    parser.add_argument("--basename", default=None, help="Base filename for carousel PNGs")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.slides_json:
            paths = render_carousel(args)
            for path in paths:
                print(path)
            return 0
        if not args.text:
            parser.error("--text is required unless --slides-json is provided")
        if not args.output:
            parser.error("--output is required for single-card generation")
        print(render(args))
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
