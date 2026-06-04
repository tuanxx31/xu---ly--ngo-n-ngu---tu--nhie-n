# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class TextSample:
    text: str
    label: str


@dataclass(frozen=True)
class ProcessedText:
    normalized_text: str
    cleaned_text: str
    raw_tokens: List[str]
    tokens: List[str]
    phrases: List[str]


@dataclass(frozen=True)
class TopicScoreDetail:
    cosine_score: float
    keyword_score: float
    phrase_score: float
    context_bonus: float
    conflict_penalty: float
    final_score: float
    keyword_matches: List[str]
    phrase_matches: List[str]
    conflict_details: List[str]


@dataclass(frozen=True)
class TopicPrediction:
    predicted_topic: str
    confidence: str
    ambiguity_warning: str
    scores: List[Tuple[str, float]]
    relative_percentages: Dict[str, float]
    score_breakdown: Dict[str, TopicScoreDetail]
    processed: ProcessedText


@dataclass(frozen=True)
class AnalysisResult:
    input_text: str
    prediction: TopicPrediction
    explanation: str
