import os
import random

from src.generator import SyntheticManuscriptGenerator
from src.utils import load_config, set_seed


class DatasetBatchGenerator:

    def __init__(self, config_path="config/config.yaml"):
        self.cfg = load_config(config_path)

        set_seed(
            self.cfg.get(
                "dataset",
                {}
            ).get(
                "seed",
                123
            )
        )

    def _get_script_text(self, script_cfg):
        return script_cfg["sample_text"]

    def _filter_text(self, text, script_name):

        script_ranges = {
            "devanagari": (0x0900, 0x097F),
            "modi": (0x11600, 0x1166F),
            "sharada": (0x11180, 0x111DF)
        }

        start, end = script_ranges[script_name]

        allowed_common = set(
            " \n\t.,;:!?-'\"()[]0123456789।॥"
        )

        result = []

        for char in text:
            code = ord(char)

            if start <= code <= end:
                result.append(char)

            elif char in allowed_common:
                result.append(char)

        return "".join(result)

    def _prepare_text(self, text, script_name):

        text = self._filter_text(
            text,
            script_name
        )

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        if not lines:
            return ""

        random.shuffle(lines)

        number_of_lines = random.randint(
            2,
            min(5, len(lines))
        )

        selected_lines = lines[
            :number_of_lines
        ]

        return "\n".join(
            selected_lines
        )

    def _clear_old_dataset(self, output_base):

        if not os.path.exists(output_base):
            return

        for root, dirs, files in os.walk(
            output_base,
            topdown=False
        ):

            for file_name in files:
                file_path = os.path.join(
                    root,
                    file_name
                )

                os.remove(file_path)

            for dir_name in dirs:
                dir_path = os.path.join(
                    root,
                    dir_name
                )

                if not os.listdir(dir_path):
                    os.rmdir(dir_path)

    def generate_all(self):

        output_base = "output_dataset"

        scripts = self.cfg["scripts"]

        total_per_script = 100

        train_count = 85
        validation_count = 10
        test_count = 5

        split_plan = [
            ("train", train_count),
            ("validation", validation_count),
            ("test", test_count)
        ]

        background_types = [
            "Aged Handmade Paper",
            "Aged Paper",
            "Copper Plate",
            "Palm Leaf",
            "Stone Inscription"
        ]

        layout_modes = [
            "single_block",
            "multi_block",
            "marginal"
        ]

        self._clear_old_dataset(
            output_base
        )

        summary = {}

        for script_name, script_cfg in scripts.items():

            print(
                f"\nGenerating {script_name} dataset..."
            )

            generator = SyntheticManuscriptGenerator(
                script_key=script_name,
                font_path=script_cfg["font_path"],
                fallback_font=script_cfg.get(
                    "fallback_font"
                )
            )

            source_text = self._get_script_text(
                script_cfg
            )

            image_number = 1

            script_summary = {}

            for split_name, count in split_plan:

                image_dir = os.path.join(
                    output_base,
                    script_name,
                    split_name,
                    "images"
                )

                annotation_dir = os.path.join(
                    output_base,
                    script_name,
                    split_name,
                    "annotations"
                )

                os.makedirs(
                    image_dir,
                    exist_ok=True
                )

                os.makedirs(
                    annotation_dir,
                    exist_ok=True
                )

                for index in range(count):

                    input_text = self._prepare_text(
                        source_text,
                        script_name
                    )

                    if not input_text:
                        raise ValueError(
                            f"No valid text found for {script_name}"
                        )

                    background = random.choice(
                        background_types
                    )

                    layout = random.choice(
                        layout_modes
                    )

                    image, ground_truth = generator.generate_sample(
                        text_input=input_text,
                        bg_type=background,
                        layout_mode=layout,
                        font_size=self.cfg["defaults"].get(
                            "font_size",
                            58
                        ),
                        handwriting_variation=self.cfg["defaults"].get(
                            "handwriting_var",
                            40
                        ),
                        aging_val=self.cfg["defaults"].get(
                            "paper_aging",
                            75
                        ) / 100.0,
                        artifact_value=self.cfg["defaults"].get(
                            "artifacts",
                            25
                        ) / 100.0,
                        page_warping=self.cfg["defaults"].get(
                            "page_warping",
                            15
                        ) / 100.0,
                        use_procedural=False,
                        seed=123 + image_number
                    )

                    file_id = (
                        f"image_{image_number:04d}"
                    )

                    image_path = os.path.join(
                        image_dir,
                        f"{file_id}.png"
                    )

                    annotation_path = os.path.join(
                        annotation_dir,
                        f"{file_id}.md"
                    )

                    image.save(
                        image_path
                    )

                    with open(
                        annotation_path,
                        "w",
                        encoding="utf-8"
                    ) as file:
                        file.write(
                            ground_truth
                        )

                    image_number += 1

                    print(
                        f"{script_name} - "
                        f"{split_name}: "
                        f"{index + 1}/{count}"
                    )

                script_summary[
                    split_name
                ] = count

            summary[
                script_name
            ] = script_summary

        return summary