import random
from PIL import Image, ImageDraw, ImageFont, features


SCRIPT_RANGES = {
    "devanagari": (0x0900, 0x097F),
    "modi": (0x11600, 0x1166F),
    "sharada": (0x11180, 0x111DF),
}

ALLOWED_COMMON = set(" \n\t.,;:!?-'\"()[]0123456789")


def filter_text(text, script_key):
    if script_key not in SCRIPT_RANGES:
        return text

    start, end = SCRIPT_RANGES[script_key]

    result = []

    for char in text:
        code = ord(char)

        if start <= code <= end or char in ALLOWED_COMMON:
            result.append(char)

    return "".join(result)


class CalligraphicTextRenderer:
    def __init__(self, font_manager, base_size=58, variation_slider=40, script_key="devanagari"):
        self.font_mgr = font_manager
        self.base_size = base_size
        self.variation = variation_slider / 100.0
        self.script_key = script_key
        self.font = self.font_mgr.get_font(base_size)

    def render_line(self, text, draw_obj, start_pos, max_width, ink_rgb=(35, 28, 22)):
        text = filter_text(text, self.script_key)

        x_start, y_start = start_pos

        if not text.strip():
            return 0

        use_raqm = features.check("raqm")
        layout = ImageFont.Layout.RAQM if use_raqm else ImageFont.Layout.BASIC

        y_jitter = random.uniform(-1.0, 1.0) * self.variation

        ink_fade = (
            random.uniform(0.85, 1.0)
            if random.random() > 0.1
            else random.uniform(0.7, 0.85)
        )

        text_ink = (
            int(ink_rgb[0] * ink_fade),
            int(ink_rgb[1] * ink_fade),
            int(ink_rgb[2] * ink_fade),
            245
        )

        try:
            draw_obj.text(
                (int(x_start), int(y_start + y_jitter)),
                text,
                font=self.font,
                fill=text_ink,
                direction="ltr",
                layout_engine=layout
            )
        except Exception:
            draw_obj.text(
                (int(x_start), int(y_start + y_jitter)),
                text,
                font=self.font,
                fill=text_ink
            )

        bbox = draw_obj.textbbox(
            (0, 0),
            text,
            font=self.font
        )

        return bbox[2] - bbox[0]