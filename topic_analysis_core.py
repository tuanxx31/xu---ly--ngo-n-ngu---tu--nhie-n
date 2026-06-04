# -*- coding: utf-8 -*-
"""
Compatibility facade for older imports.

The main implementation now follows a moderate Clean Architecture split:
- domain: entities and business configuration
- data: sample dataset
- application: topic analysis use case
- infrastructure: JSON history persistence
- presentation: Tkinter UI
"""
from application.topic_analyzer import TopicAnalyzer
from data.sample_dataset import SAMPLE_DATA
from domain.entities import TextSample
from domain.topic_config import APP_TITLE, HISTORY_FILE, MIN_WORDS_REQUIRED, TOPIC_CONFIG, TOPICS, STOPWORDS
from infrastructure.json_history_repository import JsonHistoryRepository

_analyzer = TopicAnalyzer(SAMPLE_DATA)
_history_repository = JsonHistoryRepository(HISTORY_FILE)

VOCABULARY = _analyzer.vocabulary
TOPIC_PROFILES = _analyzer.topic_profiles


def _normalize_dataset(dataset):
    normalized = []
    for item in dataset:
        if isinstance(item, dict):
            normalized.append(TextSample(text=item["text"], label=item["label"]))
        else:
            normalized.append(item)
    return normalized


def _processed_to_dict(processed):
    return {
        "normalized_text": processed.normalized_text,
        "cleaned_text": processed.cleaned_text,
        "raw_tokens": processed.raw_tokens,
        "tokens": processed.tokens,
        "phrases": processed.phrases,
    }


def _prediction_to_dict(prediction):
    return {
        "predicted_topic": prediction.predicted_topic,
        "confidence": prediction.confidence,
        "ambiguity_warning": prediction.ambiguity_warning,
        "scores": prediction.scores,
        "relative_percentages": prediction.relative_percentages,
        "score_breakdown": {
            topic: {
                "cosine_score": detail.cosine_score,
                "keyword_score": detail.keyword_score,
                "phrase_score": detail.phrase_score,
                "context_bonus": detail.context_bonus,
                "conflict_penalty": detail.conflict_penalty,
                "final_score": detail.final_score,
                "keyword_matches": detail.keyword_matches,
                "phrase_matches": detail.phrase_matches,
                "conflict_details": detail.conflict_details,
            }
            for topic, detail in prediction.score_breakdown.items()
        },
        "processed": _processed_to_dict(prediction.processed),
    }


def normalize_text(text):
    return _analyzer.normalize_text(text)


def clean_text(text):
    return _analyzer.clean_text(text)


def tokenize(text):
    return _analyzer.tokenize(text)


def remove_stopwords(tokens):
    return _analyzer.remove_stopwords(tokens)


def extract_phrases(text):
    return _analyzer.extract_phrases(text)


def preprocess_text(text):
    return _processed_to_dict(_analyzer.preprocess_text(text))


def build_vocabulary(dataset):
    return TopicAnalyzer(_normalize_dataset(dataset)).vocabulary


def text_to_vector(text, vocabulary):
    return _analyzer.text_to_vector(text, vocabulary)


def cosine_similarity(vector1, vector2):
    return _analyzer.cosine_similarity(vector1, vector2)


def build_topic_profiles(dataset, vocabulary):
    return _analyzer.build_topic_profiles(_normalize_dataset(dataset), vocabulary)


def predict_topic(text):
    return _prediction_to_dict(_analyzer.predict_topic(text))


def explain_prediction(text, scores):
    if isinstance(scores, dict):
        prediction = _analyzer.predict_topic(text)
    else:
        prediction = scores
    return _analyzer.explain_prediction(text, prediction)


def build_basic_python_report(dataset=None):
    if dataset is None:
        return _analyzer.build_basic_python_report()
    return TopicAnalyzer(_normalize_dataset(dataset)).build_basic_python_report()


def save_history(record):
    history = _history_repository.load_all()
    history.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        import json

        json.dump(history, file, ensure_ascii=False, indent=2)


def load_history():
    return _history_repository.load_all()
