import re

def normalize_sanskrit(text: str) -> str:
    if not isinstance(text, str):
        return ""
    
    # Remove danda (| , ॥), numbers, and unnecessary symbols
    text = re.sub(r'[\|॥\d\:\;\,\.\?\!]', ' ', text)
    
    # Preserve Devanagari (\u0900-\u097F), Sharada (\u11180-\u111DF), and Modi (\u11600-\u1165F)
    text = re.sub(r'[^\u0900-\u097F\u11180-\u111DF\u11600-\u1165F\s]', '', text)
    
    # Collapse multiple whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()