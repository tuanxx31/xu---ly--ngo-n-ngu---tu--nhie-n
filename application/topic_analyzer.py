# -*- coding: utf-8 -*-
import math
import re
from collections import Counter, defaultdict
from typing import Iterable, List

from domain.entities import AnalysisResult, ProcessedText, TextSample, TopicPrediction, TopicScoreDetail
from domain.topic_config import STOPWORDS, TOPIC_CONFIG, TOPICS


class TopicAnalyzer:
    def __init__(self, dataset: Iterable[TextSample]):
        self.dataset = list(dataset)
        self.vocabulary = self.build_vocabulary(self.dataset)
        self.topic_profiles = self.build_topic_profiles(self.dataset, self.vocabulary)

    def analyze(self, text: str) -> AnalysisResult:
        prediction = self.predict_topic(text)
        explanation = self.explain_prediction(text, prediction)
        return AnalysisResult(input_text=text, prediction=prediction, explanation=explanation)

    def normalize_text(self, text: str) -> str:
        return text.lower().strip()

    def clean_text(self, text: str) -> str:
        text = re.sub(
            r"[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
            " ",
            text,
        )
        text = re.sub(r"_", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        return [token for token in text.split() if token]

    def remove_stopwords(self, tokens: Iterable[str]) -> List[str]:
        return [token for token in tokens if token not in STOPWORDS]

    def extract_phrases(self, text: str) -> List[str]:
        cleaned_text = self.clean_text(self.normalize_text(text))
        tokens = self.tokenize(cleaned_text)
        phrases = []
        for size in (2, 3):
            for index in range(len(tokens) - size + 1):
                phrases.append(" ".join(tokens[index:index + size]))
        return phrases

    def preprocess_text(self, text: str) -> ProcessedText:
        normalized_text = self.normalize_text(text)
        cleaned_text = self.clean_text(normalized_text)
        raw_tokens = self.tokenize(cleaned_text)
        filtered_tokens = self.remove_stopwords(raw_tokens)
        phrases = self.extract_phrases(cleaned_text)
        return ProcessedText(
            normalized_text=normalized_text,
            cleaned_text=cleaned_text,
            raw_tokens=raw_tokens,
            tokens=filtered_tokens,
            phrases=phrases,
        )

    def build_vocabulary(self, dataset: Iterable[TextSample]) -> List[str]:
        vocabulary = []
        seen = set()
        for item in dataset:
            processed = self.preprocess_text(item.text)
            for token in processed.tokens:
                if token not in seen:
                    seen.add(token)
                    vocabulary.append(token)
        return vocabulary

    def text_to_vector(self, text_or_tokens, vocabulary: List[str]) -> List[int]:
        if isinstance(text_or_tokens, str):
            tokens = self.preprocess_text(text_or_tokens).tokens
        else:
            tokens = list(text_or_tokens)
        token_counter = Counter(tokens)
        return [token_counter.get(word, 0) for word in vocabulary]

    def cosine_similarity(self, vector1: List[int], vector2: List[int]) -> float:
        dot_product = sum(left * right for left, right in zip(vector1, vector2))
        magnitude1 = math.sqrt(sum(value * value for value in vector1))
        magnitude2 = math.sqrt(sum(value * value for value in vector2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)

    def build_topic_profiles(self, dataset: Iterable[TextSample], vocabulary: List[str]):
        grouped_tokens = defaultdict(list)
        for item in dataset:
            grouped_tokens[item.label].extend(self.preprocess_text(item.text).tokens)

        topic_profiles = {}
        for topic, tokens in grouped_tokens.items():
            topic_profiles[topic] = self.text_to_vector(tokens, vocabulary)
        return topic_profiles

    def match_weighted_terms(self, processed_text: ProcessedText, weighted_terms):
        cleaned_text = processed_text.cleaned_text
        tokens = processed_text.tokens
        phrases = processed_text.phrases
        matches = []

        for term, weight in weighted_terms.items():
            if " " in term:
                if term in cleaned_text or term in phrases:
                    matches.append((term, weight))
            elif term in tokens:
                matches.append((term, weight))
        return matches

    def calculate_keyword_score(self, text: str, topic: str):
        processed_text = self.preprocess_text(text)
        matches = self.match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["keywords"])
        return sum(weight for _, weight in matches), [term for term, _ in matches]

    def calculate_phrase_score(self, text: str, topic: str):
        processed_text = self.preprocess_text(text)
        matches = self.match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["strong_phrases"])
        return sum(weight for _, weight in matches), [term for term, _ in matches]

    def calculate_conflict_penalty(self, text: str, topic: str):
        processed_text = self.preprocess_text(text)
        own_keywords = set(term for term, _ in self.match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["keywords"]))
        own_phrases = set(term for term, _ in self.match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["strong_phrases"]))

        penalty = 0.0
        details = []
        own_signal = len(own_keywords) + (2 * len(own_phrases))

        for other_topic in TOPICS:
            if other_topic == topic:
                continue

            other_keyword_matches = self.match_weighted_terms(processed_text, TOPIC_CONFIG[other_topic]["keywords"])
            other_phrase_matches = self.match_weighted_terms(processed_text, TOPIC_CONFIG[other_topic]["strong_phrases"])
            topic_penalty = 0.0

            for term, weight in other_keyword_matches:
                if term in own_keywords or term in own_phrases:
                    continue
                increment = 0.75 if weight >= 2.0 else 0.5
                topic_penalty += increment
                details.append(f"{other_topic}: từ khóa '{term}'")

            for term, _ in other_phrase_matches:
                if term in own_phrases:
                    continue
                topic_penalty += 1.0
                details.append(f"{other_topic}: cụm từ '{term}'")

            if own_signal >= 3:
                topic_penalty *= 0.6
            elif own_signal >= 1:
                topic_penalty *= 0.8

            penalty += topic_penalty

        return penalty, details

    def apply_context_priority(self, topic: str, keyword_matches: List[str], phrase_matches: List[str]) -> float:
        boost = 0.0
        keyword_set = set(keyword_matches)
        phrase_set = set(phrase_matches)

        if topic == "Giáo dục":
            if "học trực tuyến" in phrase_set or "bài giảng online" in phrase_set:
                boost += 1.8
            if "lớp học" in phrase_set and "bài giảng" in phrase_set:
                boost += 1.2

        if topic == "Công nghệ":
            if "trí tuệ nhân tạo" in phrase_set or "cơ sở dữ liệu" in phrase_set:
                boost += 1.8
            if "phần mềm" in keyword_set and "hệ thống" in keyword_set:
                boost += 1.0

        if topic == "Sức khỏe":
            if "khám bệnh" in phrase_set or "phác đồ điều trị" in phrase_set:
                boost += 1.8
            if "bác sĩ" in keyword_set and "bệnh viện" in keyword_set:
                boost += 1.0

        if topic == "Thể thao":
            if "trận đấu" in phrase_set or "ghi bàn" in phrase_set:
                boost += 1.8
            if "cầu thủ" in keyword_set and "huấn luyện viên" in keyword_set:
                boost += 1.0

        return boost

    def assess_confidence(self, sorted_scores):
        if not sorted_scores:
            return "Thấp", "Không có đủ dữ liệu để phân tích."

        top_score = sorted_scores[0][1]
        second_score = sorted_scores[1][1] if len(sorted_scores) > 1 else 0.0

        if top_score <= 0:
            return "Thấp", "Văn bản chưa chứa đủ tín hiệu đặc trưng của các chủ đề."

        gap_ratio = abs(top_score - second_score) / max(abs(top_score), 0.0001)

        if gap_ratio < 0.10:
            return "Thấp", "Kết quả chưa thật sự chắc chắn vì văn bản có dấu hiệu liên quan đến nhiều chủ đề."
        if gap_ratio < 0.25:
            return "Trung bình", ""
        return "Cao", ""

    def calculate_relative_percentages(self, sorted_scores):
        if not sorted_scores:
            return {}

        minimum_score = min(score for _, score in sorted_scores)
        shifted_scores = [(topic, score - minimum_score + 0.001) for topic, score in sorted_scores]
        total_score = sum(score for _, score in shifted_scores)

        if total_score <= 0:
            equal_share = round(100.0 / len(sorted_scores), 2)
            return {topic: equal_share for topic, _ in sorted_scores}

        return {
            topic: round((score / total_score) * 100, 2)
            for topic, score in shifted_scores
        }

    def predict_topic(self, text: str) -> TopicPrediction:
        processed_text = self.preprocess_text(text)
        input_vector = self.text_to_vector(processed_text.tokens, self.vocabulary)
        score_breakdown = {}
        topic_scores = []

        for topic in TOPICS:
            cosine_score = self.cosine_similarity(input_vector, self.topic_profiles[topic])
            keyword_score, keyword_matches = self.calculate_keyword_score(text, topic)
            phrase_score, phrase_matches = self.calculate_phrase_score(text, topic)
            conflict_penalty, conflict_details = self.calculate_conflict_penalty(text, topic)
            context_bonus = self.apply_context_priority(topic, keyword_matches, phrase_matches)
            final_score = cosine_score + keyword_score + phrase_score + context_bonus - conflict_penalty

            score_breakdown[topic] = TopicScoreDetail(
                cosine_score=cosine_score,
                keyword_score=keyword_score,
                phrase_score=phrase_score,
                context_bonus=context_bonus,
                conflict_penalty=conflict_penalty,
                final_score=final_score,
                keyword_matches=keyword_matches,
                phrase_matches=phrase_matches,
                conflict_details=conflict_details,
            )
            topic_scores.append((topic, final_score))

        sorted_scores = sorted(topic_scores, key=lambda item: item[1], reverse=True)
        predicted_topic = sorted_scores[0][0] if sorted_scores else "Không xác định"
        confidence, ambiguity_warning = self.assess_confidence(sorted_scores)
        relative_percentages = self.calculate_relative_percentages(sorted_scores)

        return TopicPrediction(
            predicted_topic=predicted_topic,
            confidence=confidence,
            ambiguity_warning=ambiguity_warning,
            scores=sorted_scores,
            relative_percentages=relative_percentages,
            score_breakdown=score_breakdown,
            processed=processed_text,
        )

    def explain_prediction(self, text: str, prediction: TopicPrediction) -> str:
        predicted_topic = prediction.predicted_topic
        detail = prediction.score_breakdown[predicted_topic]
        parts = [
            f"Hệ thống chọn chủ đề {predicted_topic.lower()} vì chủ đề này có tổng điểm cao nhất là {detail.final_score:.4f}.",
            f"Công thức chấm điểm gồm cosine={detail.cosine_score:.4f}, keyword={detail.keyword_score:.2f}, phrase={detail.phrase_score:.2f}, context_bonus={detail.context_bonus:.2f}, penalty={detail.conflict_penalty:.2f}.",
        ]

        if detail.keyword_matches:
            parts.append(f"Từ khóa nổi bật: {', '.join(detail.keyword_matches[:8])}.")
        if detail.phrase_matches:
            parts.append(f"Cụm từ đặc trưng: {', '.join(detail.phrase_matches[:6])}.")
        if detail.conflict_details:
            parts.append("Tín hiệu gây nhiễu được phát hiện: " + "; ".join(detail.conflict_details[:6]) + ".")

        if prediction.ambiguity_warning:
            parts.append(prediction.ambiguity_warning)

        if len(self.preprocess_text(text).raw_tokens) < 8:
            parts.append("Văn bản khá ngắn nên mức ổn định của dự đoán có thể giảm.")

        return " ".join(parts)

    def build_basic_python_report(self) -> str:
        lines = [
            "PHẦN KIẾN THỨC PYTHON CƠ BẢN",
            f"Tổng số văn bản mẫu: {len(self.dataset)}",
            "",
        ]

        for index, item in enumerate(self.dataset, start=1):
            processed = self.preprocess_text(item.text)
            lines.append(f"{index}. Nhãn: {item.label}")
            lines.append(f"   Văn bản gốc: {item.text}")
            lines.append(f"   Chữ thường: {processed.normalized_text}")
            lines.append(f"   Sau làm sạch: {processed.cleaned_text}")
            lines.append(f"   Số từ gốc: {len(processed.raw_tokens)}")
            lines.append(f"   Tách từ cơ bản: {processed.raw_tokens}")
            lines.append(f"   Số từ sau bỏ stopwords: {len(processed.tokens)}")
            lines.append(f"   Danh sách từ sau bỏ stopwords: {processed.tokens}")
            lines.append("")

        return "\n".join(lines)
