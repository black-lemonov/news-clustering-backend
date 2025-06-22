import joblib

from src.config import LGBM_MODEL_PATH
from src.summarizers.model_based_summarizer import ModelBasedSummarizer


class LGBMSummarizer(ModelBasedSummarizer):
    def _load_model(self):
        return joblib.load(LGBM_MODEL_PATH)
    
    