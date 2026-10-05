"""HuggingFace transformers and hub integration."""

from typing import Optional

from transformers import pipeline, AutoTokenizer, AutoModel
from huggingface_hub import HfApi


def load_text_classifier(model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
    """Load text classification pipeline from HuggingFace."""
    return pipeline("text-classification", model=model_name)


def classify_text(text: str, model_name: Optional[str] = None) -> list[dict]:
    """Classify text sentiment using transformers pipeline."""
    pipe = load_text_classifier(model_name or "distilbert-base-uncased-finetuned-sst-2-english")
    return pipe(text)


def load_model_and_tokenizer(model_name: str):
    """Load AutoModel and AutoTokenizer for custom inference."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return tokenizer, model


def list_models_on_hub(search: str = "code"):
    """List models from HuggingFace Hub using HfApi."""
    api = HfApi()
    return list(api.list_models(search=search, limit=5))
