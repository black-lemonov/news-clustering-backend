from xgboost import XGBClassifier

from src.config import XGB_MODEL_PATH
from src.summarizers.model_based_summarizer import ModelBasedSummarizer


class XGBoostSummarizer(ModelBasedSummarizer):
    def _load_model(self):
        return XGBClassifier().load_model(XGB_MODEL_PATH)
    