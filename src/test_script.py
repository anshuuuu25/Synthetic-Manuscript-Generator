import os
import yaml
import pytest
from src.generator import SyntheticManuscriptGenerator

def test_script_rendering_and_gt():
    with open("config/config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    for script_key, script_info in cfg["scripts"].items():
        if not os.path.exists(script_info["font_path"]):
            pytest.skip(f"Font for {script_key} not present, skipping test.")

        generator = SyntheticManuscriptGenerator(
            script_key=script_key,
            font_path=script_info["font_path"],
            fallback_font=script_info["fallback_font"]
        )

        input_text = script_info["sample_text"]
        img, gt_text = generator.generate_sample(text_input=input_text, seed=123)

        assert img is not None
        assert img.size == (2048, 1024)
        assert gt_text == input_text