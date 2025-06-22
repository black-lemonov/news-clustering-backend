
import joblib

from src.config import RF_MODEL_PATH
from src.summarizers.model_based_summarizer import ModelBasedSummarizer


class RandomForestSummarizer(ModelBasedSummarizer):
    def _load_model(self):
        return joblib.load(RF_MODEL_PATH)
    