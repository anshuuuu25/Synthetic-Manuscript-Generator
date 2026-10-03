import os
import random
import numpy as np
import yaml

def load_config(config_path="config/config.yaml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def set_seed(seed=123):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

def validate_text_boundary(text_bbox, canvas_size, margins=(60, 50)):
    canvas_w, canvas_h = canvas_size
    margin_x, margin_y = margins
    x_min, y_min, x_max, y_max = text_bbox
    
    if x_min < margin_x or y_min < margin_y:
        return False
    if x_max > (canvas_w - margin_x) or y_max > (canvas_h - margin_y):
        return False
    return True

def perform_preflight_checks(image, text_gt, min_size=(500, 200)):
    if image is None:
        raise ValueError("Pre-flight check failed: Generated image object is None.")
    if not text_gt or not text_gt.strip():
        raise ValueError("Pre-flight check failed: Ground truth text is empty.")
    w, h = image.size
    if w < min_size[0] or h < min_size[1]:
        raise ValueError(f"Pre-flight check failed: Image size ({w}x{h}) below minimum threshold.")
    img_np = np.array(image)
    if img_np.std() < 5.0:
        raise ValueError("Pre-flight check failed: Image is essentially blank/featureless.")
    return True