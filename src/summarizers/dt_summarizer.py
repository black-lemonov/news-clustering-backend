import joblib

from src.config import DT_MODEL_PATH
from src.summarizers.model_based_summarizer import ModelBasedSummarizer


class DecisionTreeSummarizer(ModelBasedSummarizer):
    def _load_model(self):
        return joblib.load(DT_MODEL_PATH)
    