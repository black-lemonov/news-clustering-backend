import joblib

from src.config import DT_MODEL_PATH
from src.preprocessing.features_extractor import FeaturesExtractor
from src.summarizers.base_summarizer import BaseSummarizer


class DecisionTreeSummarizer(BaseSummarizer):
    def __init__(self) -> None:
        self.__fe = FeaturesExtractor()
        self.__dt = joblib.load(DT_MODEL_PATH)
    
    def summarize(self, text: str) -> str:
        features_df = FeaturesExtractor().convert_text_to_df(text)
        labels = self.__dt.predict(features_df.drop("text", axis=1))

        return ' '.join(
            [
                sent
                for sent, label in zip(features_df["text"], labels)
                if label == 1
            ]
        )
    