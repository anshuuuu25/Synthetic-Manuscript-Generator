import os
import random
import numpy as np
from PIL import Image, ImageDraw
import scipy.ndimage


FOLDER_MAP = {
    "Aged Handmade Paper": "aged_paper",
    "Aged Paper": "aged_paper",
    "Copper Plate": "copper_plates",
    "Palm Leaf": "palm_leaf",
    "Stone Inscription": "stone_inscription"
}


class ParchmentBackgroundGenerator:

    def __init__(self, canvas_size=(2048, 1024), assets_dir=None):
        self.w, self.h = canvas_size

        if assets_dir is None:
            base_dir = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            self.assets_dir = os.path.join(
                base_dir,
                "assets",
                "texture"
            )
        else:
            self.assets_dir = assets_dir

    def _generate_noise(self, scale=128):
        sw = max(1, self.w // scale)
        sh = max(1, self.h // scale)

        noise_small = np.random.uniform(
            0,
            1,
            (sh, sw)
        )

        smooth_noise = scipy.ndimage.zoom(
            noise_small,
            (
                self.h / sh,
                self.w / sw
            ),
            order=1
        )

        return smooth_noise[:self.h, :self.w]

    def _apply_procedural_aging(
        self,
        base_img: Image.Image,
        aging_factor=0.75
    ):

        base_arr = np.array(
            base_img,
            dtype=float
        )

        h, w, c = base_arr.shape

        dark_stain = np.array(
            [120.0, 90.0, 50.0]
        )

        stain_mask = np.zeros(
            (h, w),
            dtype=float
        )

        for _ in range(random.randint(2, 4)):

            sx = random.randint(
                int(w * 0.1),
                int(w * 0.9)
            )

            sy = random.randint(
                int(h * 0.1),
                int(h * 0.9)
            )

            rx = random.randint(120, 280)
            ry = random.randint(90, 220)

            y_i, x_i = np.indices(
                (h, w)
            )

            blob = (
                ((x_i - sx) ** 2) / (rx ** 2)
                +
                ((y_i - sy) ** 2) / (ry ** 2)
            )

            stain_raw = np.clip(
                1.0 - blob,
                0,
                1
            )

            stain_mask += (
                scipy.ndimage.gaussian_filter(
                    stain_raw,
                    sigma=20
                )
                *
                random.uniform(0.2, 0.4)
            )

        stain_mask = (
            np.clip(
                stain_mask,
                0,
                0.5
            )[:, :, np.newaxis]
            *
            aging_factor
        )

        aged_arr = (
            (1.0 - stain_mask) * base_arr
            +
            stain_mask * dark_stain
        )

        return Image.fromarray(
            np.clip(
                aged_arr,
                0,
                255
            ).astype(np.uint8)
        )

    def generate_parchment(
        self,
        bg_type="Aged Paper",
        aging_factor=0.75,
        edge_factor=0.25,
        use_procedural=False,
        **kwargs
    ):

        subfolder = FOLDER_MAP.get(
            bg_type,
            bg_type.lower().replace(" ", "_")
        )

        texture_folder = os.path.join(
            self.assets_dir,
            subfolder
        )

        if (
            not use_procedural
            and os.path.exists(texture_folder)
        ):

            image_files = [
                f
                for f in os.listdir(texture_folder)
                if f.lower().endswith(
                    (".png", ".jpg", ".jpeg")
                )
            ]

            if image_files:

                sample_file = random.choice(
                    image_files
                )

                raw_texture = Image.open(
                    os.path.join(
                        texture_folder,
                        sample_file
                    )
                ).convert("RGB")

                base_img = raw_texture.resize(
                    (self.w, self.h),
                    Image.Resampling.LANCZOS
                )

            else:

                base_cream = np.array(
                    [228.0, 214.0, 185.0]
                )

                noise = self._generate_noise(
                    scale=128
                )[:, :, np.newaxis]

                base_img = Image.fromarray(
                    np.clip(
                        base_cream *
                        (0.85 + 0.3 * noise),
                        0,
                        255
                    ).astype(np.uint8)
                )

        else:

            base_cream = np.array(
                [228.0, 214.0, 185.0]
            )

            noise = self._generate_noise(
                scale=128
            )[:, :, np.newaxis]

            base_img = Image.fromarray(
                np.clip(
                    base_cream *
                    (0.85 + 0.3 * noise),
                    0,
                    255
                ).astype(np.uint8)
            )

        if "palm" in bg_type.lower():

            draw = ImageDraw.Draw(
                base_img
            )

            hole_r = int(
                self.h * 0.04
            )

            for hx in [
                int(self.w * 0.15),
                int(self.w * 0.85)
            ]:

                hy = int(
                    self.h * 0.5
                )

                draw.ellipse(
                    [
                        hx - hole_r,
                        hy - hole_r,
                        hx + hole_r,
                        hy + hole_r
                    ],
                    fill=(30, 20, 15),
                    outline=(60, 45, 30),
                    width=3
                )

        return self._apply_procedural_aging(
            base_img,
            aging_factor=aging_factor
        )