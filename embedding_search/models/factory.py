from embedding_search.config import settings
from embedding_search.models.open_clip import OpenClipTextModel


def get_model():
    return OpenClipTextModel(settings.MODEL_ID, False, "cpu")
