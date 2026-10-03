import os
import random
from PIL import ImageDraw
from src.background import ParchmentBackgroundGenerator
from src.font_manager import FontManager
from src.text_renderer import CalligraphicTextRenderer

SAMPLE_TEXTS = [
    "ॐ नमः शिवाय । श्रीगणेशाय नमः ॥",
    "अथ ताडपत्रे लिखितं श्लोक संग्रहः ।",
    "ताम्रपत्रे उत्कीर्णं राजशासनम् ॥"
]

def generate_samples(num_samples=50, output_dir="dataset/train"):
    os.makedirs(output_dir, exist_ok=True)
    bg_gen = ParchmentBackgroundGenerator(canvas_size=(1024, 512))
    font_mgr = FontManager(font_dir="assets/fonts")
    
    bg_types = ["Aged Paper", "Palm Leaf", "Copper Plate", "Stone Inscription"]

    for i in range(num_samples):
        bg_choice = random.choice(bg_types)
        canvas = bg_gen.generate_parchment(bg_type=bg_choice, aging_factor=0.5)
        draw = ImageDraw.Draw(canvas)
        
        renderer = CalligraphicTextRenderer(font_mgr, base_size=42)
        text_line = random.choice(SAMPLE_TEXTS)
        
        # Render line centered on canvas
        renderer.render_line(text_line, draw, start_pos=(80, 200), max_width=850)
        
        # Save image and ground-truth text file
        base_name = f"sample_{i:04d}"
        canvas.save(os.path.join(output_dir, f"{base_name}.png"))
        
        with open(os.path.join(output_dir, f"{base_name}.md"), "w", encoding="utf-8") as f:
            f.write(text_line)

    print(f"Successfully generated {num_samples} dataset pairs in '{output_dir}'.")

if __name__ == "__main__":
    generate_samples(num_samples=20)