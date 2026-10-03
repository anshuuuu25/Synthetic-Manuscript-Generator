import os
from PIL import ImageFont


class FontManager:

    def __init__(self, script_key, font_path, fallback_font=None):
        self.script_key = script_key
        self.font_path = font_path
        self.fallback_font = fallback_font
        self._validate_font()

    def _validate_font(self):
        if not os.path.exists(self.font_path):
            if self.fallback_font and os.path.exists(self.fallback_font):
                self.font_path = self.fallback_font
            else:
                raise FileNotFoundError(
                    f"Font not found: {self.font_path}"
                )

        try:
            font = ImageFont.truetype(self.font_path, 40)
            font.getbbox("test")
        except Exception as e:
            raise RuntimeError(
                f"Could not load font '{self.font_path}': {e}"
            )

    def get_font(self, size):
        try:
            return ImageFont.truetype(
                self.font_path,
                size
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to load font '{self.font_path}': {e}"
            )