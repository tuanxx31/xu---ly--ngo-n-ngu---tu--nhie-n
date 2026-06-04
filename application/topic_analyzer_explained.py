# -*- coding: utf-8 -*-
# Dòng trên khai báo encoding UTF-8, cho phép file chứa ký tự tiếng Việt

import math
# Import module math để sử dụng hàm toán học như sqrt (căn bậc hai)

import re
# Import module re (regular expression) để xử lý chuỗi bằng biểu thức chính quy

from collections import Counter, defaultdict
# Counter: đếm tần suất xuất hiện của các phần tử trong danh sách
# defaultdict: dictionary tự tạo giá trị mặc định khi truy cập key chưa tồn tại

from typing import Iterable, List, Sequence
# Import các kiểu dữ liệu dùng cho type hint (gợi ý kiểu)
# Iterable: đối tượng có thể lặp qua (list, tuple, generator,...)
# List: danh sách
# Sequence: chuỗi có thứ tự (list, tuple,...)

from domain.entities import (
    AnalysisResult,      # Entity chứa kết quả phân tích tổng hợp
    ProcessedText,       # Entity chứa văn bản đã qua tiền xử lý
    TextSample,          # Entity đại diện 1 mẫu văn bản (text + label)
    TopicPrediction,     # Entity chứa kết quả dự đoán chủ đề
    TopicScoreDetail,    # Entity chứa chi tiết điểm số từng chủ đề
)
# Import các entity (thực thể dữ liệu) từ tầng domain

from domain.topic_config import STOPWORDS, TOPIC_CONFIG, TOPICS
# STOPWORDS: danh sách từ dừng (từ không mang ý nghĩa phân loại, VD: "là", "và", "của")
# TOPIC_CONFIG: cấu hình từ khóa + cụm từ đặc trưng cho mỗi chủ đề
# TOPICS: danh sách tên các chủ đề (VD: "Giáo dục", "Công nghệ",...)


class TopicAnalyzer:
    """Use case phân tích văn bản và dự đoán chủ đề."""
    # Đây là class chính, đóng vai trò Use Case trong kiến trúc Clean Architecture
    # Chịu trách nhiệm: tiền xử lý văn bản → tính điểm → dự đoán chủ đề

    def __init__(self, dataset: Iterable[TextSample]):
        # Hàm khởi tạo, nhận vào tập dữ liệu huấn luyện (dataset)

        self.dataset = list(dataset)
        # Chuyển dataset thành list và lưu lại để dùng sau

        self.vocabulary = self.build_vocabulary(self.dataset)
        # Xây dựng từ vựng (vocabulary) từ toàn bộ dataset
        # Vocabulary = danh sách tất cả từ duy nhất xuất hiện trong dataset

        self.topic_profiles = self.build_topic_profiles(self.dataset, self.vocabulary)
        # Xây dựng "hồ sơ" (profile) vector cho từng chủ đề
        # Mỗi profile là 1 vector BoW (Bag of Words) đại diện cho chủ đề đó

    # ========================================================================================
    # HÀM ENTRY POINT - Cổng vào duy nhất cho bên ngoài
    # ========================================================================================

    def analyze(self, text: str) -> AnalysisResult:
        # Hàm phân tích chính mà bên ngoài gọi vào
        # Nhận: 1 chuỗi văn bản cần phân tích
        # Trả về: AnalysisResult chứa dự đoán + giải thích

        prediction = self.predict_topic(text)
        # Bước 1: Gọi predict_topic() để dự đoán chủ đề

        explanation = self.explain_prediction(text, prediction)
        # Bước 2: Gọi explain_prediction() để tạo giải thích bằng ngôn ngữ tự nhiên

        return AnalysisResult(input_text=text, prediction=prediction, explanation=explanation)
        # Bước 3: Đóng gói kết quả vào AnalysisResult và trả về

    # ========================================================================================
    # NHÓM HÀM TIỀN XỬ LÝ VĂN BẢN (Text Preprocessing)
    # Pipeline: normalize → clean → tokenize → remove_stopwords → extract_phrases
    # ========================================================================================

    def normalize_text(self, text: str) -> str:
        # Chuẩn hóa văn bản: chuyển thành chữ thường + xóa khoảng trắng thừa 2 đầu
        return text.lower().strip()
        # .lower() → "Hello World" thành "hello world"
        # .strip() → "  hello  " thành "hello"

    def clean_text(self, text: str) -> str:
        # Làm sạch văn bản: loại bỏ ký tự đặc biệt, chỉ giữ lại chữ cái + số + dấu tiếng Việt

        text = re.sub(
            r"[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
            " ",
            text,
        )
        # Dùng regex thay thế mọi ký tự KHÔNG phải chữ/số/khoảng trắng/dấu tiếng Việt bằng dấu cách
        # VD: "xin chào! @bạn" → "xin chào  bạn"

        text = re.sub(r"_", " ", text)
        # Thay dấu gạch dưới (_) bằng khoảng trắng
        # VD: "machine_learning" → "machine learning"

        text = re.sub(r"\s+", " ", text)
        # Gộp nhiều khoảng trắng liên tiếp thành 1
        # VD: "xin   chào   bạn" → "xin chào bạn"

        return text.strip()
        # Xóa khoảng trắng 2 đầu và trả về

    def tokenize(self, text: str) -> List[str]:
        # Tách văn bản thành danh sách các từ (token) bằng khoảng trắng

        if not text:
            return []
            # Nếu text rỗng → trả về danh sách rỗng

        return [token for token in text.split() if token]
        # text.split() tách theo khoảng trắng
        # Lọc bỏ chuỗi rỗng (phòng trường hợp edge case)
        # VD: "xin chào bạn" → ["xin", "chào", "bạn"]

    def remove_stopwords(self, tokens: Iterable[str]) -> List[str]:
        # Loại bỏ stopwords (từ dừng) khỏi danh sách token

        return [token for token in tokens if token not in STOPWORDS]
        # Giữ lại những token KHÔNG có trong danh sách STOPWORDS
        # VD: ["đây", "là", "bài", "giảng"] → ["bài", "giảng"] (nếu "đây","là" là stopwords)

    def extract_phrases(self, text: str) -> List[str]:
        # Trích xuất cụm từ (n-gram) gồm 2, 3, 4 từ liên tiếp từ văn bản

        cleaned_text = self.clean_text(self.normalize_text(text))
        # Bước 1: Chuẩn hóa → làm sạch văn bản

        tokens = self.tokenize(cleaned_text)
        # Bước 2: Tách thành danh sách từ

        phrases = []
        # Khởi tạo danh sách chứa cụm từ

        for size in (2, 3, 4):
            # Lặp qua các kích thước cụm từ: 2-gram, 3-gram, 4-gram

            for index in range(len(tokens) - size + 1):
                # Duyệt qua các vị trí bắt đầu có thể tạo cụm từ

                phrases.append(" ".join(tokens[index:index + size]))
                # Nối các token liên tiếp thành cụm từ và thêm vào danh sách
                # VD: tokens = ["học", "trực", "tuyến", "miễn", "phí"]
                #   2-gram: "học trực", "trực tuyến", "tuyến miễn", "miễn phí"
                #   3-gram: "học trực tuyến", "trực tuyến miễn", "tuyến miễn phí"
                #   4-gram: "học trực tuyến miễn", "trực tuyến miễn phí"

        return phrases

    def preprocess_text(self, text: str) -> ProcessedText:
        # Hàm tổng hợp toàn bộ pipeline tiền xử lý
        # Gọi lần lượt các bước và đóng gói kết quả vào ProcessedText

        normalized_text = self.normalize_text(text)
        # Bước 1: Chuẩn hóa (chữ thường + strip)

        cleaned_text = self.clean_text(normalized_text)
        # Bước 2: Làm sạch (loại ký tự đặc biệt)

        raw_tokens = self.tokenize(cleaned_text)
        # Bước 3: Tách từ (chưa lọc stopwords)

        filtered_tokens = self.remove_stopwords(raw_tokens)
        # Bước 4: Lọc bỏ stopwords

        phrases = self.extract_phrases(cleaned_text)
        # Bước 5: Trích xuất cụm từ n-gram

        return ProcessedText(
            normalized_text=normalized_text,    # Văn bản đã chuẩn hóa
            cleaned_text=cleaned_text,          # Văn bản đã làm sạch
            raw_tokens=raw_tokens,              # Danh sách từ gốc (chưa lọc)
            tokens=filtered_tokens,             # Danh sách từ đã lọc stopwords
            phrases=phrases,                    # Danh sách cụm từ n-gram
        )

    # ========================================================================================
    # NHÓM HÀM XÂY DỰNG MÔ HÌNH (Model Building)
    # Xây dựng vocabulary và topic profiles từ dataset huấn luyện
    # ========================================================================================

    def build_vocabulary(self, dataset: Iterable[TextSample]) -> List[str]:
        # Xây dựng từ vựng từ toàn bộ dataset
        # Trả về danh sách các từ DUY NHẤT, giữ nguyên thứ tự xuất hiện đầu tiên

        vocabulary = []
        # Danh sách từ vựng (giữ thứ tự)

        seen = set()
        # Tập hợp (set) để kiểm tra trùng lặp nhanh O(1)

        for item in dataset:
            # Lặp qua từng mẫu văn bản trong dataset

            processed = self.preprocess_text(item.text)
            # Tiền xử lý văn bản của mẫu

            for token in processed.tokens:
                # Duyệt qua từng token đã lọc stopwords

                if token not in seen:
                    # Nếu token chưa xuất hiện trước đó

                    seen.add(token)
                    # Đánh dấu đã thấy

                    vocabulary.append(token)
                    # Thêm vào vocabulary

        return vocabulary
        # VD: vocabulary = ["học", "sinh", "trường", "công", "nghệ", "máy", "tính",...]

    def text_to_vector(self, text_or_tokens, vocabulary: Sequence[str]) -> List[int]:
        # Chuyển văn bản/danh sách token thành vector BoW (Bag of Words)
        # Mỗi phần tử trong vector = số lần từ tương ứng xuất hiện trong văn bản

        if isinstance(text_or_tokens, str):
            tokens = self.preprocess_text(text_or_tokens).tokens
            # Nếu đầu vào là chuỗi → tiền xử lý để lấy danh sách token
        else:
            tokens = list(text_or_tokens)
            # Nếu đầu vào đã là danh sách token → dùng trực tiếp

        token_counter = Counter(tokens)
        # Đếm tần suất mỗi token
        # VD: Counter(["học", "sinh", "học"]) → {"học": 2, "sinh": 1}

        return [token_counter.get(word, 0) for word in vocabulary]
        # Tạo vector: với mỗi từ trong vocabulary, lấy số lần xuất hiện (0 nếu không có)
        # VD: vocabulary = ["học", "sinh", "máy"]
        #     tokens = ["học", "sinh", "học"]
        #     → vector = [2, 1, 0]

    def cosine_similarity(self, vector1: Sequence[int], vector2: Sequence[int]) -> float:
        # Tính độ tương đồng cosine giữa 2 vector
        # Công thức: cos(θ) = (A·B) / (|A| × |B|)
        # Giá trị từ 0 (hoàn toàn khác) đến 1 (hoàn toàn giống)

        dot_product = sum(left * right for left, right in zip(vector1, vector2))
        # Tích vô hướng (dot product): tổng của tích từng cặp phần tử
        # VD: [2,1,0] · [1,0,3] = 2×1 + 1×0 + 0×3 = 2

        magnitude1 = math.sqrt(sum(value * value for value in vector1))
        # Độ lớn (magnitude) vector 1: căn bậc 2 của tổng bình phương
        # VD: |[2,1,0]| = √(4+1+0) = √5

        magnitude2 = math.sqrt(sum(value * value for value in vector2))
        # Độ lớn vector 2

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
            # Nếu 1 trong 2 vector là vector 0 → trả về 0 (tránh chia cho 0)

        return dot_product / (magnitude1 * magnitude2)
        # Trả về giá trị cosine similarity

    def build_topic_profiles(self, dataset: Iterable[TextSample], vocabulary: Sequence[str]):
        # Xây dựng vector profile cho từng chủ đề từ dataset
        # Gom tất cả token của mỗi chủ đề lại → tạo 1 vector BoW đại diện

        grouped_tokens = defaultdict(list)
        # Dictionary tự tạo list rỗng khi truy cập key mới
        # Key = tên chủ đề, Value = danh sách tất cả token thuộc chủ đề đó

        for item in dataset:
            grouped_tokens[item.label].extend(self.preprocess_text(item.text).tokens)
            # Với mỗi mẫu: lấy label (chủ đề) → thêm các token vào nhóm tương ứng
            # VD: item.label = "Giáo dục", tokens = ["học", "sinh", "trường"]
            #     → grouped_tokens["Giáo dục"].extend(["học", "sinh", "trường"])

        topic_profiles = {}
        for topic, tokens in grouped_tokens.items():
            topic_profiles[topic] = self.text_to_vector(tokens, vocabulary)
            # Chuyển danh sách token gộp thành vector BoW
            # Mỗi chủ đề có 1 vector profile riêng

        return topic_profiles
        # VD: {"Giáo dục": [5, 3, 4, 0, 0,...], "Công nghệ": [0, 0, 1, 7, 5,...]}

    # ========================================================================================
    # NHÓM HÀM TÍNH ĐIỂM (Scoring Functions)
    # Tính điểm cho từng chủ đề dựa trên nhiều tiêu chí
    # ========================================================================================

    def match_weighted_terms(self, processed_text: ProcessedText, weighted_terms):
        # So khớp văn bản với danh sách từ/cụm từ có trọng số
        # Trả về danh sách các cặp (term, weight) đã khớp

        cleaned_text = processed_text.cleaned_text
        # Văn bản đã làm sạch (dạng chuỗi liền)

        tokens = processed_text.tokens
        # Danh sách từ đơn

        phrases = processed_text.phrases
        # Danh sách cụm từ n-gram

        matches = []
        # Danh sách kết quả khớp

        for term, weight in weighted_terms.items():
            # Duyệt qua từng term (từ/cụm từ) và trọng số của nó

            if " " in term:
                # Nếu term chứa khoảng trắng → đây là cụm từ (phrase)

                if term in cleaned_text or term in phrases:
                    matches.append((term, weight))
                    # Kiểm tra cụm từ có xuất hiện trong văn bản gốc hoặc danh sách n-gram không

            elif term in tokens:
                matches.append((term, weight))
                # Nếu là từ đơn → kiểm tra trong danh sách token

        return matches
        # VD: [("học trực tuyến", 3.0), ("giáo viên", 2.0)]

    def calculate_keyword_score(self, text: str, topic: str):
        # Tính điểm từ khóa cho 1 chủ đề cụ thể
        # Tra cứu từ khóa trong TOPIC_CONFIG[topic]["keywords"]

        processed_text = self.preprocess_text(text)
        # Tiền xử lý văn bản

        matches = self.match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["keywords"])
        # So khớp với danh sách từ khóa có trọng số của chủ đề

        return sum(weight for _, weight in matches), [term for term, _ in matches]
        # Trả về: (tổng điểm, danh sách từ khóa đã khớp)
        # VD: (5.5, ["giáo viên", "học sinh", "trường học"])

    def calculate_phrase_score(self, text: str, topic: str):
        # Tính điểm cụm từ đặc trưng (strong phrases) cho 1 chủ đề
        # Tương tự calculate_keyword_score nhưng dùng "strong_phrases"

        processed_text = self.preprocess_text(text)
        matches = self.match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["strong_phrases"])
        return sum(weight for _, weight in matches), [term for term, _ in matches]
        # VD: (6.0, ["học trực tuyến", "bài giảng online"])

    def calculate_conflict_penalty(self, text: str, topic: str):
        # Tính điểm phạt xung đột (conflict penalty)
        # Nếu văn bản chứa từ khóa của CHỦ ĐỀ KHÁC → bị trừ điểm
        # Giúp phân biệt văn bản thuộc nhiều lĩnh vực

        processed_text = self.preprocess_text(text)

        own_keywords = set(
            term
            for term, _ in self.match_weighted_terms(
                processed_text,
                TOPIC_CONFIG[topic]["keywords"],
            )
        )
        # Lấy tập hợp từ khóa ĐÃ KHỚP của chủ đề đang xét
        # Dùng set để tra cứu nhanh O(1)

        own_phrases = set(
            term
            for term, _ in self.match_weighted_terms(
                processed_text,
                TOPIC_CONFIG[topic]["strong_phrases"],
            )
        )
        # Lấy tập hợp cụm từ ĐÃ KHỚP của chủ đề đang xét

        penalty = 0.0
        # Tổng điểm phạt

        details = []
        # Chi tiết các tín hiệu gây nhiễu

        own_signal = len(own_keywords) + (2 * len(own_phrases))
        # Sức mạnh tín hiệu riêng: số keyword + 2 × số phrase
        # Phrase được tính gấp đôi vì mang tín hiệu mạnh hơn
        # Giá trị này dùng để giảm penalty khi chủ đề chính đã rõ ràng

        for other_topic in TOPICS:
            # Lặp qua TẤT CẢ các chủ đề khác

            if other_topic == topic:
                continue
                # Bỏ qua chính chủ đề đang xét

            other_keyword_matches = self.match_weighted_terms(
                processed_text,
                TOPIC_CONFIG[other_topic]["keywords"],
            )
            # Tìm từ khóa của chủ đề khác xuất hiện trong văn bản

            other_phrase_matches = self.match_weighted_terms(
                processed_text,
                TOPIC_CONFIG[other_topic]["strong_phrases"],
            )
            # Tìm cụm từ của chủ đề khác xuất hiện trong văn bản

            topic_penalty = 0.0
            # Điểm phạt riêng cho chủ đề khác này

            for term, weight in other_keyword_matches:
                if term in own_keywords or term in own_phrases:
                    continue
                    # Bỏ qua nếu từ này CŨNG là keyword/phrase của chủ đề đang xét
                    # (từ đa nghĩa, không nên phạt)

                increment = 0.75 if weight >= 2.0 else 0.5
                # Từ khóa trọng số cao (≥2.0) → phạt 0.75 điểm
                # Từ khóa trọng số thấp (<2.0) → phạt 0.5 điểm

                topic_penalty += increment
                details.append(f"{other_topic}: từ khóa '{term}'")
                # Ghi nhận chi tiết gây nhiễu

            for term, _ in other_phrase_matches:
                if term in own_phrases:
                    continue
                    # Bỏ qua cụm từ trùng với chủ đề đang xét

                topic_penalty += 1.0
                # Cụm từ gây nhiễu → phạt 1.0 điểm (nặng hơn từ đơn)

                details.append(f"{other_topic}: cụm từ '{term}'")

            if own_signal >= 3:
                topic_penalty *= 0.6
                # Nếu tín hiệu riêng mạnh (≥3) → giảm 40% penalty
                # Lý do: chủ đề chính đã rõ, nhiễu ít ảnh hưởng
            elif own_signal >= 1:
                topic_penalty *= 0.8
                # Nếu tín hiệu riêng trung bình (≥1) → giảm 20% penalty

            penalty += topic_penalty
            # Cộng dồn penalty

        return penalty, details
        # Trả về: (tổng điểm phạt, danh sách chi tiết gây nhiễu)

    def apply_context_priority(self, topic: str, keyword_matches: List[str], phrase_matches: List[str]) -> float:
        # Tính điểm thưởng ngữ cảnh (context bonus)
        # Khi phát hiện TỔ HỢP từ khóa/cụm từ đặc trưng cao → thưởng thêm điểm
        # Giúp tăng độ chính xác khi văn bản có nhiều tín hiệu rõ ràng

        boost = 0.0
        # Điểm thưởng ban đầu = 0

        keyword_set = set(keyword_matches)
        # Chuyển list keyword đã khớp thành set để tra cứu nhanh

        phrase_set = set(phrase_matches)
        # Chuyển list phrase đã khớp thành set

        # --- Quy tắc thưởng cho từng chủ đề ---
        # Mỗi chủ đề có 2 loại thưởng:
        #   1. Cụm từ đặc trưng cao → +1.8 điểm
        #   2. Tổ hợp 2 từ khóa liên quan → +1.0 hoặc +1.2 điểm

        if topic == "Giáo dục":
            if "học trực tuyến" in phrase_set or "bài giảng online" in phrase_set:
                boost += 1.8
                # Cụm từ rất đặc trưng cho Giáo dục → thưởng lớn
            if "lớp học" in phrase_set and "bài giảng" in phrase_set:
                boost += 1.2
                # Tổ hợp 2 cụm từ cùng xuất hiện → thưởng thêm

        if topic == "Công nghệ":
            if "trí tuệ nhân tạo"  in phrase_set or "cơ sở dữ liệu" in phrase_set:
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

        if topic == "Kinh tế":
            if "thị trường chứng khoán" in phrase_set or "tăng trưởng kinh tế" in phrase_set:
                boost += 1.8
            if "đầu tư" in keyword_set and "lãi suất" in keyword_set:
                boost += 1.0

        if topic == "Ẩm thực":
            if "ẩm thực đường phố" in phrase_set or "công thức nấu ăn" in phrase_set:
                boost += 1.8
            if "đầu bếp" in keyword_set and "món ăn" in keyword_set:
                boost += 1.0

        if topic == "Văn hóa - Nghệ thuật":
            if "triển lãm nghệ thuật" in phrase_set or "di sản văn hóa" in phrase_set:
                boost += 1.8
            if "nghệ sĩ" in keyword_set and "sân khấu" in keyword_set:
                boost += 1.0

        if topic == "Pháp luật":
            if "tòa án nhân dân" in phrase_set or "khởi tố vụ án" in phrase_set:
                boost += 1.8
            if "bị cáo" in keyword_set and "xét xử" in keyword_set:
                boost += 1.0

        if topic == "Du lịch":
            if "tour du lịch" in phrase_set or "danh lam thắng cảnh" in phrase_set:
                boost += 1.8
            if "du khách" in keyword_set and "khách sạn" in keyword_set:
                boost += 1.0

        if topic == "Xe":
            if "động cơ turbo" in phrase_set or "hộp số tự động" in phrase_set:
                boost += 1.8
            if "ô tô" in keyword_set and "động cơ" in keyword_set:
                boost += 1.0

        if topic == "Đời sống":
            if "nuôi dạy con" in phrase_set or "đời sống gia đình" in phrase_set:
                boost += 1.8
            if "gia đình" in keyword_set and "vợ chồng" in keyword_set:
                boost += 1.0

        if topic == "Bất động sản":
            if "chung cư cao cấp" in phrase_set or "dự án bất động sản" in phrase_set:
                boost += 1.8
            if "chung cư" in keyword_set and "căn hộ" in keyword_set:
                boost += 1.0

        return boost
        # Trả về tổng điểm thưởng ngữ cảnh

    # ========================================================================================
    # NHÓM HÀM ĐÁNH GIÁ KẾT QUẢ (Result Assessment)
    # ========================================================================================

    def assess_confidence(self, sorted_scores):
        # Đánh giá mức độ tin cậy (confidence) của kết quả dự đoán
        # Dựa trên khoảng cách giữa điểm cao nhất và điểm thứ nhì

        if not sorted_scores:
            return "Thấp", "Không có đủ dữ liệu để phân tích."
            # Nếu không có điểm nào → tin cậy thấp

        top_score = sorted_scores[0][1]
        # Điểm cao nhất (chủ đề được chọn)

        second_score = sorted_scores[1][1] if len(sorted_scores) > 1 else 0.0
        # Điểm thứ nhì (đối thủ gần nhất)

        if top_score <= 0:
            return "Thấp", "Văn bản chưa chứa đủ tín hiệu đặc trưng của các chủ đề."
            # Nếu điểm cao nhất ≤ 0 → không có tín hiệu nào

        gap_ratio = abs(top_score - second_score) / max(abs(top_score), 0.0001)
        # Tỷ lệ khoảng cách = |điểm 1 - điểm 2| / |điểm 1|
        # Đo mức độ "vượt trội" của chủ đề đứng đầu
        # VD: top=10, second=9 → gap_ratio = 1/10 = 0.1 (sát nhau, không chắc)
        # VD: top=10, second=2 → gap_ratio = 8/10 = 0.8 (chênh lệch lớn, rất chắc)

        if gap_ratio < 0.10:
            return "Thấp", "Kết quả chưa thật sự chắc chắn vì văn bản có dấu hiệu liên quan đến nhiều chủ đề."
            # Khoảng cách < 10% → tin cậy thấp

        if gap_ratio < 0.25:
            return "Trung bình", ""
            # Khoảng cách 10-25% → tin cậy trung bình

        return "Cao", ""
        # Khoảng cách ≥ 25% → tin cậy cao

    def calculate_relative_percentages(self, sorted_scores):
        # Tính phần trăm tương đối cho mỗi chủ đề
        # Chuyển điểm thô thành % để dễ hiển thị

        if not sorted_scores:
            return {}

        minimum_score = min(score for _, score in sorted_scores)
        # Tìm điểm thấp nhất

        shifted_scores = [(topic, score - minimum_score + 0.001) for topic, score in sorted_scores]
        # Dịch chuyển tất cả điểm lên để điểm nhỏ nhất = 0.001
        # Tránh giá trị âm khi tính phần trăm
        # +0.001 để tránh chia cho 0

        total_score = sum(score for _, score in shifted_scores)
        # Tổng điểm sau dịch chuyển

        if total_score <= 0:
            equal_share = round(100.0 / len(sorted_scores), 2)
            return {topic: equal_share for topic, _ in sorted_scores}
            # Nếu tổng ≤ 0 → chia đều cho tất cả chủ đề

        return {
            topic: round((score / total_score) * 100, 2)
            for topic, score in shifted_scores
        }
        # Tính % = (điểm chủ đề / tổng điểm) × 100, làm tròn 2 chữ số thập phân
        # VD: {"Giáo dục": 45.32, "Công nghệ": 23.15, "Sức khỏe": 12.53,...}

    # ========================================================================================
    # HÀM XỬ LÝ CHÍNH - PREDICT TOPIC (Bộ não của hệ thống)
    # ========================================================================================

    def predict_topic(self, text: str) -> TopicPrediction:
        # ★ HÀM XỬ LÝ CHÍNH ★
        # Điều phối toàn bộ pipeline: tiền xử lý → tính điểm → xếp hạng → trả kết quả

        processed_text = self.preprocess_text(text)
        # Bước 1: Tiền xử lý văn bản đầu vào

        input_vector = self.text_to_vector(processed_text.tokens, self.vocabulary)
        # Bước 2: Chuyển văn bản thành vector BoW

        score_breakdown = {}
        # Dictionary lưu chi tiết điểm của từng chủ đề

        topic_scores = []
        # Danh sách (tên chủ đề, điểm tổng) để xếp hạng

        for topic in TOPICS:
            # Bước 3: Lặp qua TỪNG CHỦ ĐỀ để tính điểm

            cosine_score = self.cosine_similarity(input_vector, self.topic_profiles[topic])
            # 3a: Tính cosine similarity giữa vector input và profile chủ đề
            # Đo mức độ giống nhau về phân bố từ

            keyword_score, keyword_matches = self.calculate_keyword_score(text, topic)
            # 3b: Tính điểm từ khóa có trọng số

            phrase_score, phrase_matches = self.calculate_phrase_score(text, topic)
            # 3c: Tính điểm cụm từ đặc trưng

            conflict_penalty, conflict_details = self.calculate_conflict_penalty(text, topic)
            # 3d: Tính điểm phạt xung đột với chủ đề khác

            context_bonus = self.apply_context_priority(topic, keyword_matches, phrase_matches)
            # 3e: Tính điểm thưởng ngữ cảnh

            final_score = cosine_score + keyword_score + phrase_score + context_bonus - conflict_penalty
            # ★ CÔNG THỨC TỔNG HỢP ★
            # final_score = cosine + keyword + phrase + bonus - penalty
            # Đây là công thức cốt lõi quyết định chủ đề nào thắng

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
            # Lưu chi tiết điểm của chủ đề này

            topic_scores.append((topic, final_score))
            # Thêm vào danh sách để xếp hạng

        sorted_scores = sorted(topic_scores, key=lambda item: item[1], reverse=True)
        # Bước 4: Sắp xếp các chủ đề theo điểm GIẢM DẦN
        # Chủ đề điểm cao nhất sẽ ở vị trí đầu tiên

        predicted_topic = sorted_scores[0][0] if sorted_scores else "Không xác định"
        # Bước 5: Chọn chủ đề có điểm cao nhất làm kết quả dự đoán

        confidence, ambiguity_warning = self.assess_confidence(sorted_scores)
        # Bước 6: Đánh giá mức độ tin cậy (Cao/Trung bình/Thấp)

        relative_percentages = self.calculate_relative_percentages(sorted_scores)
        # Bước 7: Tính phần trăm tương đối cho mỗi chủ đề

        return TopicPrediction(
            predicted_topic=predicted_topic,         # Chủ đề được dự đoán
            confidence=confidence,                   # Mức tin cậy
            ambiguity_warning=ambiguity_warning,     # Cảnh báo nhập nhằng (nếu có)
            scores=sorted_scores,                    # Danh sách điểm đã sắp xếp
            relative_percentages=relative_percentages,  # Phần trăm từng chủ đề
            score_breakdown=score_breakdown,          # Chi tiết điểm từng chủ đề
            processed=processed_text,                 # Văn bản đã tiền xử lý
        )
        # Đóng gói toàn bộ kết quả và trả về

    # ========================================================================================
    # HÀM GIẢI THÍCH KẾT QUẢ (Explainability)
    # ========================================================================================

    def explain_prediction(self, text: str, prediction: TopicPrediction) -> str:
        # Tạo giải thích bằng ngôn ngữ tự nhiên cho kết quả dự đoán
        # Giúp người dùng hiểu TẠI SAO hệ thống chọn chủ đề này

        predicted_topic = prediction.predicted_topic
        # Lấy tên chủ đề được dự đoán

        detail = prediction.score_breakdown[predicted_topic]
        # Lấy chi tiết điểm của chủ đề đó

        parts = [
            f"Hệ thống chọn chủ đề {predicted_topic.lower()} vì chủ đề này có tổng điểm cao nhất là {detail.final_score:.4f}.",
            # Câu mở đầu: cho biết chủ đề được chọn và tổng điểm

            f"Công thức chấm điểm gồm cosine={detail.cosine_score:.4f}, keyword={detail.keyword_score:.2f}, phrase={detail.phrase_score:.2f}, context_bonus={detail.context_bonus:.2f}, penalty={detail.conflict_penalty:.2f}.",
            # Phân tích chi tiết từng thành phần điểm
        ]

        if detail.keyword_matches:
            parts.append(f"Từ khóa nổi bật: {', '.join(detail.keyword_matches[:8])}.")
            # Liệt kê tối đa 8 từ khóa đã khớp

        if detail.phrase_matches:
            parts.append(f"Cụm từ đặc trưng: {', '.join(detail.phrase_matches[:6])}.")
            # Liệt kê tối đa 6 cụm từ đã khớp

        if detail.conflict_details:
            parts.append("Tín hiệu gây nhiễu được phát hiện: " + "; ".join(detail.conflict_details[:6]) + ".")
            # Liệt kê tối đa 6 tín hiệu gây nhiễu

        if prediction.ambiguity_warning:
            parts.append(prediction.ambiguity_warning)
            # Thêm cảnh báo nhập nhằng nếu có

        if len(self.preprocess_text(text).raw_tokens) < 8:
            parts.append("Văn bản khá ngắn nên mức ổn định của dự đoán có thể giảm.")
            # Cảnh báo nếu văn bản quá ngắn (< 8 từ)

        return " ".join(parts)
        # Nối tất cả phần giải thích thành 1 chuỗi

    # ========================================================================================
    # HÀM BÁO CÁO (Reporting)
    # ========================================================================================

    def build_basic_python_report(self) -> str:
        # Tạo báo cáo dạng text về dataset và kết quả tiền xử lý
        # Dùng để hiển thị trong phần "Kiến thức Python cơ bản" của UI

        lines = [
            "PHẦN KIẾN THỨC PYTHON CƠ BẢN",
            f"Tổng số văn bản mẫu: {len(self.dataset)}",
            "",
        ]
        # Tiêu đề báo cáo + tổng số mẫu

        for index, item in enumerate(self.dataset, start=1):
            # Lặp qua từng mẫu, đánh số từ 1

            processed = self.preprocess_text(item.text)
            # Tiền xử lý mẫu

            lines.append(f"{index}. Nhãn: {item.label}")
            # Số thứ tự + nhãn chủ đề

            lines.append(f"   Văn bản gốc: {item.text}")
            # Văn bản gốc chưa xử lý

            lines.append(f"   Chữ thường: {processed.normalized_text}")
            # Sau bước normalize (chữ thường)

            lines.append(f"   Sau làm sạch: {processed.cleaned_text}")
            # Sau bước clean (loại ký tự đặc biệt)

            lines.append(f"   Số từ gốc: {len(processed.raw_tokens)}")
            # Số từ trước khi lọc stopwords

            lines.append(f"   Tách từ bằng khoảng trắng: {processed.raw_tokens}")
            # Danh sách từ gốc

            lines.append(f"   Cụm 2-3 từ từ extract_phrases: {processed.phrases[:20]}")
            # 20 cụm từ n-gram đầu tiên

            lines.append(f"   Số từ sau bỏ stopwords: {len(processed.tokens)}")
            # Số từ sau khi lọc stopwords

            lines.append(f"   Danh sách từ sau bỏ stopwords: {processed.tokens}")
            # Danh sách từ cuối cùng

            lines.append("")
            # Dòng trống ngăn cách giữa các mẫu

        return "\n".join(lines)
        # Nối tất cả dòng thành chuỗi báo cáo hoàn chỉnh
