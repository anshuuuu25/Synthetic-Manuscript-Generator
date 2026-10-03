from PIL import Image, ImageDraw
from src.text_renderer import CalligraphicTextRenderer


class ManuscriptLayoutEngine:

    def __init__(
        self,
        font_manager,
        canvas_size=(2048, 1024)
    ):
        self.w, self.h = canvas_size
        self.font_mgr = font_manager

    def render_layout(
        self,
        raw_text,
        layout_mode="single_block",
        font_size=58,
        handwriting_variation=40,
        primary_ink=(35, 28, 22),
        script_key="devanagari"
    ):
        layer = Image.new(
            "RGBA",
            (self.w, self.h),
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(layer)

        renderer = CalligraphicTextRenderer(
            self.font_mgr,
            base_size=font_size,
            variation_slider=handwriting_variation,
            script_key=script_key
        )

        margin_x = int(self.w * 0.08)
        margin_y = int(self.h * 0.10)

        max_width = int(
            self.w * 0.78
        )

        lines = [
            line.strip()
            for line in raw_text.split("\n")
            if line.strip()
        ]

        ground_truth = []

        spacing = int(
            font_size * 1.35
        )

        if layout_mode == "multi_block":
            current_y = margin_y

            block_gap = int(
                font_size * 0.8
            )

            for index, line in enumerate(lines):

                if index > 0 and index % 4 == 0:
                    current_y += block_gap

                if current_y + font_size >= self.h - margin_y:
                    break

                renderer.render_line(
                    line,
                    draw,
                    (
                        margin_x,
                        current_y
                    ),
                    max_width,
                    primary_ink
                )

                ground_truth.append(line)
                current_y += spacing

        elif layout_mode == "marginal":

            main_x = int(
                self.w * 0.20
            )

            main_width = int(
                self.w * 0.62
            )

            current_y = margin_y

            for line in lines:

                if current_y + font_size >= self.h - margin_y:
                    break

                renderer.render_line(
                    line,
                    draw,
                    (
                        main_x,
                        current_y
                    ),
                    main_width,
                    primary_ink
                )

                ground_truth.append(line)
                current_y += spacing

            side_text = "॥ शुभ ॥"

            renderer.render_line(
                side_text,
                draw,
                (
                    int(self.w * 0.05),
                    margin_y
                ),
                int(self.w * 0.12),
                primary_ink
            )

        else:

            current_y = margin_y

            for line in lines:

                if current_y + font_size >= self.h - margin_y:
                    break

                renderer.render_line(
                    line,
                    draw,
                    (
                        margin_x,
                        current_y
                    ),
                    max_width,
                    primary_ink
                )

                ground_truth.append(line)
                current_y += spacing

        return layer, "\n".join(ground_truth)