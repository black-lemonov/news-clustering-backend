from abc import ABC, abstractmethod

from src.preprocessing.features_extractor import FeaturesExtractor
from src.summarizers.base_summarizer import BaseSummarizer


class ModelBasedSummarizer(BaseSummarizer, ABC):
    def __init__(self) -> None:
        self._fe = FeaturesExtractor()
        self.__model = self._load_model()
    
    def summarize(self, text: str) -> str:
        features_df = FeaturesExtractor().convert_text_to_df(text)
        labels = self.__model.predict(features_df.drop("text", axis=1))

        return ' '.join(
            [
                sent
                for sent, label in zip(features_df["text"], labels)
                if label == 1
            ]
        )
    
    @abstractmethod
    def _load_model(self):
        pass