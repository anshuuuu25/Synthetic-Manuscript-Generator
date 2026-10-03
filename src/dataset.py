import os
import random
from src.generator import SyntheticManuscriptGenerator
from src.utils import load_config, set_seed

class DatasetBatchGenerator:
    def __init__(self, config_path="config/config.yaml"):
        self.cfg = load_config(config_path)
        set_seed(self.cfg.get("dataset", {}).get("seed", 123))

    def _load_corpus(self, corpus_path):
        if os.path.exists(corpus_path):
            with open(corpus_path, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
                if lines:
                    return lines
        return [
            "लक्षण। अपूर्व असे परियेसा ।८। ऋषि म्हणे रायासी। पुत्रभविष्य पुससी।",
            "ऐकोनि दुःख पावसी। कवणेपरी सांगावे ।९। राव विनवी तये वेळी।"
        ]

    def generate_all(self):
        output_base = self.cfg["dataset"]["output_dir"]
        scripts = self.cfg["scripts"]
        total_per_script = self.cfg["dataset"]["images_per_script"]

        splits_def = self.cfg["dataset"]["splits"]
        train_cnt = int(total_per_script * splits_def["train"])
        val_cnt = int(total_per_script * splits_def["validation"])
        test_cnt = total_per_script - (train_cnt + val_cnt)

        split_plan = [("train", train_cnt), ("validation", val_cnt), ("test", test_cnt)]
        summary = {}

        for script_name, script_cfg in scripts.items():
            corpus = self._load_corpus(script_cfg["corpus_path"])
            generator = SyntheticManuscriptGenerator(
                font_path=script_cfg["font_path"],
                fallback_font=script_cfg.get("fallback_font"),
                config_path="config/config.yaml"
            )

            img_idx = 1
            script_summary = {}

            for split_name, count in split_plan:
                img_dir = os.path.join(output_base, script_name, split_name, "images")
                ann_dir = os.path.join(output_base, script_name, split_name, "annotations")
                os.makedirs(img_dir, exist_ok=True)
                os.makedirs(ann_dir, exist_ok=True)

                for _ in range(count):
                    sample_size = min(len(corpus), random.randint(3, 6))
                    input_text = "\n".join(random.sample(corpus, sample_size))

                    bg_style = random.choice(self.cfg["styles"]["background_types"])
                    layout_style = random.choice(self.cfg["layouts"]["modes"])

                    img, gt_text = generator.generate_sample(
                        text_input=input_text,
                        bg_type=bg_style,
                        layout_mode=layout_style
                    )

                    file_id = f"image_{img_idx:04d}"
                    img.save(os.path.join(img_dir, f"{file_id}.png"))
                    with open(os.path.join(ann_dir, f"{file_id}.md"), "w", encoding="utf-8") as f:
                        f.write(gt_text)

                    img_idx += 1

                script_summary[split_name] = count
            summary[script_name] = script_summary

        return summary