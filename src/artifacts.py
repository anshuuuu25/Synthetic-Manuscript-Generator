import numpy as np
from PIL import Image, ImageFilter, ImageDraw
import scipy.ndimage

class AgingEffectsEngine:
    def __init__(self, art_factor=0.25, warp_factor=0.15, scan_factor=0.15):
        self.art_factor = art_factor
        self.warp_factor = warp_factor
        self.scan_factor = scan_factor

    def apply_effects(self, image: Image.Image) -> Image.Image:
        img_arr = np.array(image)
        h, w, c = img_arr.shape

        # Perspective / spatial warp
        if self.warp_factor > 0:
            x = np.linspace(-1, 1, w)
            y = np.linspace(-1, 1, h)
            xx, yy = np.meshgrid(x, y)
            
            dx = np.sin(yy * np.pi) * 6.0 * self.warp_factor
            dy = np.cos(xx * np.pi) * 4.0 * self.warp_factor

            map_x = (np.tile(np.arange(w), (h, 1)) + dx).astype(np.float32)
            map_y = (np.repeat(np.arange(h), w).reshape(h, w) + dy).astype(np.float32)

            for channel in range(c):
                img_arr[:, :, channel] = scipy.ndimage.map_coordinates(
                    img_arr[:, :, channel], [map_y, map_x], order=1, mode='nearest'
                )

        res_img = Image.fromarray(img_arr)

        # Subtle blur / focus loss
        if self.art_factor > 0:
            res_img = res_img.filter(ImageFilter.GaussianBlur(radius=0.3))

        # Scan vignetting
        if self.scan_factor > 0:
            vignette = Image.new("L", (w, h), 255)
            # FIXED: ImageDraw.Draw instead of Image.Draw
            v_draw = ImageDraw.Draw(vignette)
            v_draw.ellipse([-int(w * 0.1), -int(h * 0.1), int(w * 1.1), int(h * 1.1)], fill=230)
            vignette = vignette.filter(ImageFilter.GaussianBlur(radius=100))
            
            dark_bg = Image.new("RGB", (w, h), (30, 25, 20))
            res_img = Image.composite(res_img.convert("RGB"), dark_bg, vignette)

        return res_img