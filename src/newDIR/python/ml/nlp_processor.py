"""spaCy NLP processing for code and text analysis."""

import spacy


def load_nlp_model(model_name: str = "en_core_web_sm"):
    """Load spaCy model for text processing."""
    return spacy.load(model_name)


def extract_entities(text: str, model_name: str = "en_core_web_sm") -> list[dict]:
    """Extract named entities from text using spaCy."""
    nlp = load_nlp_model(model_name)
    doc = nlp(text)
    return [
        {"text": ent.text, "label": ent.label_}
        for ent in doc.ents
    ]


def tokenize_and_lemmatize(text: str, model_name: str = "en_core_web_sm") -> list[str]:
    """Tokenize text and return lemmas."""
    nlp = load_nlp_model(model_name)
    doc = nlp(text)
    return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
