import argparse
import os
from src.dataset import DatasetBatchGenerator
from src.generator import SyntheticManuscriptGenerator
from src.utils import set_seed

def main():
    parser = argparse.ArgumentParser(description="Indic Synthetic Manuscript Generator CLI")
    parser.add_argument("--script", type=str, choices=["devanagari", "modi", "sharada"], help="Single script target")
    parser.add_argument("--count", type=int, help="Number of images in single execution mode")
    parser.add_argument("--seed", type=int, default=123, help="Random seed for reproducibility")
    parser.add_argument("--background", type=str, default="Aged Handmade Paper")

    args = parser.parse_args()
    set_seed(args.seed)

    if args.script and args.count:
        print(f"--> Running single execution mode for script: {args.script.upper()} ({args.count} samples)")
        generator = SyntheticManuscriptGenerator(font_path=f"assets/fonts/{args.script}.ttf")
        os.makedirs("output_dataset/single_run", exist_ok=True)

        for i in range(1, args.count + 1):
            sample_text = "लक्षण। अपूर्व असे परियेसा ।८। ऋषि म्हणे रायासी।"
            img, gt = generator.generate_sample(sample_text, bg_type=args.background)
            file_id = f"{args.script}_{i:03d}"
            img.save(f"output_dataset/single_run/{file_id}.png")
            with open(f"output_dataset/single_run/{file_id}.md", "w", encoding="utf-8") as f:
                f.write(gt)
        print(f"✅ Generated {args.count} samples in output_dataset/single_run/")
    else:
        print("--> Initiating complete 300-image multi-script dataset generation...")
        batch_gen = DatasetBatchGenerator()
        summary = batch_gen.generate_all()

        print("\n" + "="*50)
        print("     DATASET GENERATION SUMMARY SUMMARY")
        print("="*50)
        total_images = 0
        for script, splits in summary.items():
            script_total = sum(splits.values())
            total_images += script_total
            print(f"Script: {script.upper():<12} | Total: {script_total}")
            for split, cnt in splits.items():
                print(f"  ├── {split:<10}: {cnt}")
        print("="*50)
        print(f"Grand Total Generated: {total_images} images + synchronized .md files")
        print("Dataset Directory: output_dataset/")
        print("="*50)

if __name__ == "__main__":
    main()