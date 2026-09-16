import os
from io import BytesIO

import reportlab
from PIL import Image, ImageDraw, ImageFont

from translations import t

CARD_SIZE = 1080

BG_COLOR = "#0f1c2e"
ACCENT_COLOR = "#f5a623"
TEXT_PRIMARY = "#ffffff"
TEXT_MUTED = "#9fb3c8"
DIVIDER_COLOR = "#26364a"
SOURCE_COLORS = {
    "grid": "#4da3ff",
    "generator": "#ff6b6b",
    "solar": "#ffd166",
}

# Bitstream Vera ships with reportlab (already a project dependency), so we
# reuse it here rather than adding a new font dependency or bundling a font
# file. It covers Latin scripts well; it has no Arabic glyphs, so Arabic
# labels on the card may show missing-glyph boxes rather than shaped Arabic
# text. That is an accepted limitation, in the same spirit as this app's
# existing "no RTL layout flip" note for the Streamlit UI.
_REPORTLAB_FONTS_DIR = os.path.join(os.path.dirname(reportlab.__file__), "fonts")


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "VeraBd.ttf" if bold else "Vera.ttf"
    path = os.path.join(_REPORTLAB_FONTS_DIR, filename)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


def _fit_text(draw: ImageDraw.ImageDraw, text: str, bold: bool, max_width: int, start_size: int, min_size: int = 28):
    """Shrink the font until `text` fits `max_width`; truncate with an ellipsis if even
    `min_size` doesn't fit. Always returns (font, text_to_draw)."""
    size = start_size
    while size > min_size:
        font = _load_font(size, bold)
        if draw.textlength(text, font=font) <= max_width:
            return font, text
        size -= 2

    font = _load_font(min_size, bold)
    truncated = text
    while truncated and draw.textlength(truncated + "…", font=font) > max_width:
        truncated = truncated[:-1]
    display_text = f"{truncated}…" if truncated != text else text
    return font, display_text


def generate_summary_card(
    business_name: str,
    month_label: str,
    total_cost: float,
    source_totals: dict,
    language: str = "en",
) -> bytes:
    """Render a square, WhatsApp-friendly PNG summarizing this month's energy costs.

    source_totals maps source keys ("grid", "generator", "solar") to their
    total cost in USD.
    """
    img = Image.new("RGB", (CARD_SIZE, CARD_SIZE), BG_COLOR)
    draw = ImageDraw.Draw(img)

    margin = 90
    content_width = CARD_SIZE - 2 * margin

    # Header label
    header_font = _load_font(32, bold=True)
    draw.text((CARD_SIZE // 2, 90), t("card_header_label", language).upper(), font=header_font,
               fill=TEXT_MUTED, anchor="mm")

    # Business name (auto-shrink / truncate to fit)
    name_font, business_name = _fit_text(
        draw, business_name, bold=True, max_width=content_width, start_size=64, min_size=32
    )
    draw.text((CARD_SIZE // 2, 170), business_name, font=name_font, fill=TEXT_PRIMARY, anchor="mm")

    # Month label
    month_font = _load_font(32)
    draw.text((CARD_SIZE // 2, 230), month_label, font=month_font, fill=TEXT_MUTED, anchor="mm")

    draw.line([(margin, 290), (CARD_SIZE - margin, 290)], fill=DIVIDER_COLOR, width=2)

    # Total this month
    total_label_font = _load_font(30)
    draw.text((CARD_SIZE // 2, 340), t("card_total_label", language), font=total_label_font,
               fill=TEXT_MUTED, anchor="mm")

    total_font = _load_font(104, bold=True)
    draw.text((CARD_SIZE // 2, 430), f"${total_cost:,.2f}", font=total_font, fill=ACCENT_COLOR, anchor="mm")

    draw.line([(margin, 510), (CARD_SIZE - margin, 510)], fill=DIVIDER_COLOR, width=2)

    # By-source breakdown
    section_font = _load_font(36, bold=True)
    draw.text((margin, 555), t("card_by_source_label", language), font=section_font, fill=TEXT_PRIMARY, anchor="lm")

    row_label_font = _load_font(34)
    row_amount_font = _load_font(34, bold=True)

    sources = ["grid", "generator", "solar"]
    max_cost = max(source_totals.get(s, 0.0) for s in sources) or 1.0

    bar_x = margin + 40
    bar_max_width = content_width - 40
    bar_height = 22
    row_y = 640
    row_height = 110

    for source in sources:
        cost = source_totals.get(source, 0.0)
        dot_center = (margin + 12, row_y)
        draw.ellipse(
            [dot_center[0] - 12, dot_center[1] - 12, dot_center[0] + 12, dot_center[1] + 12],
            fill=SOURCE_COLORS[source],
        )
        draw.text((margin + 40, row_y), t(f"source_{source}", language), font=row_label_font,
                   fill=TEXT_PRIMARY, anchor="lm")
        draw.text((CARD_SIZE - margin, row_y), f"${cost:,.2f}", font=row_amount_font,
                   fill=TEXT_PRIMARY, anchor="rm")

        bar_y = row_y + 30
        bar_width = int(bar_max_width * (cost / max_cost)) if max_cost > 0 else 0
        draw.rounded_rectangle(
            [bar_x, bar_y, bar_x + bar_max_width, bar_y + bar_height], radius=bar_height // 2, fill=DIVIDER_COLOR
        )
        if bar_width > 0:
            draw.rounded_rectangle(
                [bar_x, bar_y, bar_x + max(bar_width, bar_height), bar_y + bar_height],
                radius=bar_height // 2, fill=SOURCE_COLORS[source],
            )

        row_y += row_height

    # Footer
    footer_font = _load_font(26)
    draw.text((CARD_SIZE // 2, CARD_SIZE - 60), t("card_footer_note", language), font=footer_font,
               fill=TEXT_MUTED, anchor="mm")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
