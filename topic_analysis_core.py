# -*- coding: utf-8 -*-
"""Compatibility wrapper cho phiên bản trước khi tách Clean Architecture.

Code mới nên import trực tiếp từ:
- application.topic_analyzer
- domain.topic_config
- data.sample_dataset
- infrastructure.json_history_repository
- infrastructure.document_reader
"""

import json
import os

from application.topic_analyzer import TopicAnalyzer
from data.sample_dataset import SAMPLE_DATA as TEXT_SAMPLE_DATA
from domain.entities import ProcessedText, TextSample, TopicPrediction, TopicScoreDetail
from domain.topic_config import (
    APP_TITLE,
    HISTORY_FILE,
    MIN_WORDS_REQUIRED,
    STOPWORDS,
    TOPIC_CONFIG,
    TOPICS,
)
from infrastructure.document_reader import (
    read_document_file,
    read_docx_file,
    read_pdf_file,
    read_txt_file,
)


DEFAULT_ANALYZER = TopicAnalyzer(TEXT_SAMPLE_DATA)
SAMPLE_DATA = [{"text": item.text, "label": item.label} for item in TEXT_SAMPLE_DATA]
VOCABULARY = DEFAULT_ANALYZER.vocabulary
TOPIC_PROFILES = DEFAULT_ANALYZER.topic_profiles


def _as_text_sample(item):
    if isinstance(item, TextSample):
        return item
    return TextSample(text=item["text"], label=item["label"])


def _as_text_samples(dataset):
    return [_as_text_sample(item) for item in dataset]


def _processed_to_dict(processed: ProcessedText):
    return {
        "normalized_text": processed.normalized_text,
        "cleaned_text": processed.cleaned_text,
        "raw_tokens": processed.raw_tokens,
        "tokens": processed.tokens,
        "phrases": processed.phrases,
    }


def _processed_from_any(processed_text):
    if isinstance(processed_text, ProcessedText):
        return processed_text
    return ProcessedText(
        normalized_text=processed_text["normalized_text"],
        cleaned_text=processed_text["cleaned_text"],
        raw_tokens=processed_text["raw_tokens"],
        tokens=processed_text["tokens"],
        phrases=processed_text["phrases"],
    )


def _detail_to_dict(detail: TopicScoreDetail):
    return {
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


def _prediction_to_dict(prediction: TopicPrediction):
    return {
        "predicted_topic": prediction.predicted_topic,
        "confidence": prediction.confidence,
        "ambiguity_warning": prediction.ambiguity_warning,
        "scores": prediction.scores,
        "relative_percentages": prediction.relative_percentages,
        "score_breakdown": {
            topic: _detail_to_dict(detail)
            for topic, detail in prediction.score_breakdown.items()
        },
        "processed": _processed_to_dict(prediction.processed),
    }


def normalize_text(text):
    return DEFAULT_ANALYZER.normalize_text(text)


def clean_text(text):
    return DEFAULT_ANALYZER.clean_text(text)


def tokenize(text):
    return DEFAULT_ANALYZER.tokenize(text)


def remove_stopwords(tokens):
    return DEFAULT_ANALYZER.remove_stopwords(tokens)


def extract_phrases(text):
    return DEFAULT_ANALYZER.extract_phrases(text)


def preprocess_text(text):
    return _processed_to_dict(DEFAULT_ANALYZER.preprocess_text(text))


def build_vocabulary(dataset):
    return DEFAULT_ANALYZER.build_vocabulary(_as_text_samples(dataset))


def text_to_vector(text, vocabulary):
    return DEFAULT_ANALYZER.text_to_vector(text, vocabulary)


def cosine_similarity(vector1, vector2):
    return DEFAULT_ANALYZER.cosine_similarity(vector1, vector2)


def build_topic_profiles(dataset, vocabulary):
    return DEFAULT_ANALYZER.build_topic_profiles(_as_text_samples(dataset), vocabulary)


def match_weighted_terms(processed_text, weighted_terms):
    return DEFAULT_ANALYZER.match_weighted_terms(_processed_from_any(processed_text), weighted_terms)


def calculate_keyword_score(text, topic):
    return DEFAULT_ANALYZER.calculate_keyword_score(text, topic)


def calculate_phrase_score(text, topic):
    return DEFAULT_ANALYZER.calculate_phrase_score(text, topic)


def calculate_conflict_penalty(text, topic):
    return DEFAULT_ANALYZER.calculate_conflict_penalty(text, topic)


def apply_context_priority(topic, keyword_matches, phrase_matches):
    return DEFAULT_ANALYZER.apply_context_priority(topic, keyword_matches, phrase_matches)


def assess_confidence(sorted_scores):
    return DEFAULT_ANALYZER.assess_confidence(sorted_scores)


def calculate_relative_percentages(sorted_scores):
    return DEFAULT_ANALYZER.calculate_relative_percentages(sorted_scores)


def predict_topic(text):
    return _prediction_to_dict(DEFAULT_ANALYZER.predict_topic(text))


def explain_prediction(text, _scores=None):
    prediction = DEFAULT_ANALYZER.predict_topic(text)
    return DEFAULT_ANALYZER.explain_prediction(text, prediction)


def build_basic_python_report(dataset=None):
    if dataset is None:
        return DEFAULT_ANALYZER.build_basic_python_report()
    analyzer = TopicAnalyzer(_as_text_samples(dataset))
    return analyzer.build_basic_python_report()


def save_history(record):
    history = load_history()
    history.append(record)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []
