# Indic Synthetic Manuscript Generator & OCR Dataset Pipeline

Synthetic image generator that produces historical manuscript folios across Devanagari, Modi, and Sharada scripts for OCR training.

## Required Font Assets

Ensure Unicode-compatible TrueType fonts are placed inside `assets/fonts/`:

- **Devanagari:** `assets/fonts/devanagari.ttf`
- **Modi:** `assets/fonts/modi.ttf`
- **Sharada:** `assets/fonts/sharada.ttf`

## Dataset Directory Structure

Generated via `python generate_dataset.py`: