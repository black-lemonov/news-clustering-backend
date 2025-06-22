
import joblib

from src.config import SUMM_MODELS_FILEPATHS
from src.summarizers.model_based_summarizer import ModelBasedSummarizer


class RandomForestSummarizer(ModelBasedSummarizer):
    def _load_model(self):
        return joblib.load(SUMM_MODELS_FILEPATHS["rf"])
    