import open_clip
import torch

from loguru import logger
from typing import Any, List

from embedding_search.models.embedding_model import EmbeddingModel


OPEN_CLIP_MODEL_MAP = dict(open_clip.list_pretrained())


class OpenClipTextModel(EmbeddingModel):
    def __init__(self, model_id: str, use_jit: bool, device):
        self.device = device
        logger.info("booting up model")
        print(model_id)
        print(OPEN_CLIP_MODEL_MAP[model_id])
        model, _, _ = open_clip.create_model_and_transforms(
            model_id, pretrained=OPEN_CLIP_MODEL_MAP[model_id], jit=use_jit
        )
        logger.info("moving model to device")
        self.model = model.to(self.device)

        logger.info("booting up tokenizer")
        self.tokenizer = open_clip.get_tokenizer(model_id)

        if use_jit:
            for _ in range(2):
                warmup_text = self.tokenizer(["two LLMs sitting in a tree"] * 32).to(
                    self.device
                )
                with torch.no_grad():
                    self.model.encode_text(warmup_text)

    def prepare(self, value: Any):
        return self.tokenizer([value])[0]

    def embed(self, value: List[Any]):
        with torch.no_grad():
            text_features = self.model.encode_text(value.to(self.device))
        text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().to(torch.float16).detach().numpy()
