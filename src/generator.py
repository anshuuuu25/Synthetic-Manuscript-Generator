import numpy as np
import random
from PIL import Image

from src.font_manager import FontManager
from src.background import ParchmentBackgroundGenerator
from src.layout import ManuscriptLayoutEngine
from src.artifacts import AgingEffectsEngine


class SyntheticManuscriptGenerator:

    def __init__(
        self,
        script_key: str,
        font_path: str,
        fallback_font: str = None
    ):
        self.script_key = script_key

        self.font_mgr = FontManager(
            script_key=script_key,
            font_path=font_path,
            fallback_font=fallback_font
        )

        self.bg_gen = ParchmentBackgroundGenerator(
            canvas_size=(2048, 1024)
        )

        self.layout_engine = ManuscriptLayoutEngine(
            self.font_mgr,
            canvas_size=(2048, 1024)
        )

    def generate_sample(
        self,
        text_input,
        bg_type="Aged Handmade Paper",
        layout_mode="single_block",
        font_size=58,
        handwriting_variation=40,
        ink_color=(35, 28, 22),
        aging_val=0.75,
        artifact_value=0.25,
        page_warping=0.15,
        use_procedural=False,
        seed=None
    ):

        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        bg_img = self.bg_gen.generate_parchment(
            bg_type=bg_type,
            aging_factor=aging_val,
            use_procedural=use_procedural
        )

        artifact_engine = AgingEffectsEngine(
            art_factor=artifact_value,
            warp_factor=page_warping,
            scan_factor=0.15
        )

        text_layer, gt_text = self.layout_engine.render_layout(
            raw_text=text_input,
            layout_mode=layout_mode,
            font_size=font_size,
            handwriting_variation=handwriting_variation,
            primary_ink=ink_color,
            script_key=self.script_key
        )

        folio = Image.alpha_composite(
            bg_img.convert("RGBA"),
            text_layer
        )

        final_folio = artifact_engine.apply_effects(folio)

        return final_folio, gt_text