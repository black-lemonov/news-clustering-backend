from src.summarizers.summarizers.base_summarizer import BaseSummarizer
from src.summarizers.config import SUMM_MODELS_FILEPATHS
from src.summarizers.model_loaders.joblib_loader import JoblibLoader
from src.summarizers.summarizers.model_summarizer import ModelSummarizer
from src.summarizers.utils import get_selected_model_name


def get_summarizer() -> BaseSummarizer:
    model = ModelSummarizer(
        SUMM_MODELS_FILEPATHS[get_selected_model_name()], JoblibLoader()
    )
    return model
