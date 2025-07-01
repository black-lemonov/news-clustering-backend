import joblib

from src.summarizers.model_loaders.model_loader import ModelLoader


class JoblibLoader(ModelLoader):
    def load_model(self, filepath: str):
        return joblib.load(filepath)
