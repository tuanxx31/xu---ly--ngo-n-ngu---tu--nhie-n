# -*- coding: utf-8 -*-
import json
import os

from application.history_repository import HistoryRepository
from domain.entities import AnalysisResult
from domain.topic_config import HISTORY_FILE


class JsonHistoryRepository(HistoryRepository):
    def __init__(self, file_path: str = HISTORY_FILE):
        self.file_path = file_path

    def load_all(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    def save(self, result: AnalysisResult) -> None:
        history = self.load_all()
        history.append(self._to_record(result))

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=2)

    def _to_record(self, result: AnalysisResult):
        prediction = result.prediction
        return {
            "input_text": result.input_text,
            "cleaned_text": prediction.processed.cleaned_text,
            "tokens": prediction.processed.tokens,
            "predicted_topic": prediction.predicted_topic,
            "confidence": prediction.confidence,
            "ambiguity_warning": prediction.ambiguity_warning,
            "scores": [
                {
                    "topic": topic,
                    "final_score": round(score, 6),
                    "cosine_score": round(prediction.score_breakdown[topic].cosine_score, 6),
                    "keyword_score": round(prediction.score_breakdown[topic].keyword_score, 6),
                    "phrase_score": round(prediction.score_breakdown[topic].phrase_score, 6),
                    "context_bonus": round(prediction.score_breakdown[topic].context_bonus, 6),
                    "conflict_penalty": round(prediction.score_breakdown[topic].conflict_penalty, 6),
                }
                for topic, score in prediction.scores
            ],
            "explanation": result.explanation,
        }
