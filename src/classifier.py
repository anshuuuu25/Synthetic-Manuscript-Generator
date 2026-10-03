import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from src.preprocess import normalize_sanskrit

class SanskritClassifier:
    def __init__(self):
        # Character n-grams (2 to 5) work best for compound Sanskrit words
        self.pipeline = make_pipeline(
            TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 5)),
            MultinomialNB(alpha=0.1)
        )
        self.is_trained = False

    def train(self, data_input):
        if isinstance(data_input, str):
            df = pd.read_csv(data_input)
        else:
            df = data_input

        df['cleaned'] = df['text'].apply(normalize_sanskrit)
        self.pipeline.fit(df['cleaned'], df['label'])
        self.is_trained = True

    def predict(self, text: str):
        cleaned = normalize_sanskrit(text)
        prediction = self.pipeline.predict([cleaned])[0]
        probs = self.pipeline.predict_proba([cleaned])[0]
        confidence = float(max(probs) * 100)
        
        return {
            "label": prediction,
            "confidence": round(confidence, 2)
        }