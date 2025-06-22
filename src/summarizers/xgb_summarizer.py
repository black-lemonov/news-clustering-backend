from xgboost import XGBClassifier

from src.config import SUMM_MODELS_FILEPATHS
from src.summarizers.model_based_summarizer import ModelBasedSummarizer


class XGBoostSummarizer(ModelBasedSummarizer):
    def _load_model(self):
        return XGBClassifier().load_model(SUMM_MODELS_FILEPATHS["xgb"])
    