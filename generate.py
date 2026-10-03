from src.dataset import DatasetBatchGenerator
from src.utils import set_seed


def main():
    set_seed(123)

    print("Starting dataset generation...")
    print("Target: 100 images per script")
    print("Scripts: Devanagari, Modi, Sharada")

    generator = DatasetBatchGenerator()
    summary = generator.generate_all()

    print("\n" + "=" * 40)
    print("DATASET GENERATION SUMMARY")
    print("=" * 40)

    total_images = 0

    for script, splits in summary.items():
        script_total = sum(splits.values())
        total_images += script_total

        print(f"\n{script.upper()}: {script_total} images")

        for split, count in splits.items():
            print(f"  {split}: {count}")

    print("\n" + "=" * 40)
    print(f"TOTAL IMAGES: {total_images}")
    print("Dataset location: output_dataset/")
    print("=" * 40)


if __name__ == "__main__":
    main()