# -*- coding: utf-8 -*-
import json
import math
import os
import re
from collections import Counter, defaultdict


APP_TITLE = "HỆ THỐNG GỢI Ý CHỦ ĐỀ BÀI VIẾT NGẮN"
HISTORY_FILE = "analysis_history.json"
MIN_WORDS_REQUIRED = 5

TOPICS = ["Công nghệ", "Giáo dục", "Sức khỏe", "Thể thao"]

STOPWORDS = {
    "là", "và", "của", "có", "trong", "một", "những", "các", "cho", "với",
    "được", "khi", "để", "thì", "mà", "này", "đó", "cũng", "rất", "nhiều",
    "về", "từ", "đang", "trên", "theo", "vào", "ra", "ở", "tại", "do", "vì",
    "nên", "đã", "sẽ", "cần", "hơn", "giúp", "việc", "mỗi", "như", "hay",
    "bị", "đến", "cùng", "qua", "lại", "thêm", "các", "nhằm", "sau", "trước",
    "được", "nhiều", "ít", "vẫn", "đều", "đang", "vừa", "mới", "rằng", "thật",
    "sự", "của", "về", "với", "đó", "này", "kia", "ấy", "nơi", "đây"
}

TOPIC_CONFIG = {
    "Công nghệ": {
        "keywords": {
            "máy tính": 2.0, "phần mềm": 2.0, "internet": 1.0, "dữ liệu": 2.0,
            "ai": 2.0, "trí tuệ nhân tạo": 2.0, "lập trình": 2.0, "thuật toán": 2.0,
            "ứng dụng": 1.0, "bảo mật": 2.0, "hệ thống": 1.5, "mạng": 1.5,
            "thiết bị": 1.5, "server": 1.5, "website": 1.5, "robot": 1.5,
            "cơ sở dữ liệu": 2.0, "điện toán đám mây": 2.0, "công nghệ số": 2.0,
            "tự động hóa": 2.0, "api": 1.5
        },
        "strong_phrases": {
            "trí tuệ nhân tạo": 3.0, "cơ sở dữ liệu": 3.0, "điện toán đám mây": 3.0,
            "bảo mật thông tin": 3.0, "công nghệ số": 3.0, "tự động hóa": 3.0,
            "hệ thống phần mềm": 3.0, "lập trình python": 3.0, "an ninh mạng": 3.0
        }
    },
    "Giáo dục": {
        "keywords": {
            "học sinh": 2.0, "sinh viên": 2.0, "giáo viên": 2.0, "lớp học": 2.0,
            "bài giảng": 2.0, "học tập": 1.5, "kiến thức": 1.5, "kỳ thi": 2.0,
            "đào tạo": 2.0, "trường học": 2.0, "nhà trường": 2.0, "giảng dạy": 2.0,
            "môn học": 1.5, "điểm số": 1.5, "giáo trình": 2.0, "sách vở": 1.5,
            "thư viện": 1.5, "bài kiểm tra": 2.0, "kỹ năng": 1.0
        },
        "strong_phrases": {
            "học trực tuyến": 3.0, "bài giảng online": 3.0, "kỳ thi cuối kỳ": 3.0,
            "lớp học": 3.0, "bài giảng": 3.0, "phương pháp giảng dạy": 3.0,
            "chương trình đào tạo": 3.0, "môi trường học tập": 3.0
        }
    },
    "Sức khỏe": {
        "keywords": {
            "bác sĩ": 2.0, "bệnh": 1.0, "bệnh viện": 2.0, "thuốc": 2.0,
            "điều trị": 2.0, "khám bệnh": 2.0, "dinh dưỡng": 2.0, "cơ thể": 1.0,
            "giấc ngủ": 2.0, "sức đề kháng": 2.0, "sức khỏe": 1.0, "triệu chứng": 2.0,
            "chế độ ăn": 2.0, "rau xanh": 1.5, "nước uống": 1.5, "miễn dịch": 2.0,
            "huyết áp": 2.0, "xét nghiệm": 2.0, "bệnh nhân": 1.5
        },
        "strong_phrases": {
            "khám bệnh": 3.0, "điều trị bệnh": 3.0, "chế độ ăn": 3.0,
            "sức đề kháng": 3.0, "giấc ngủ": 3.0, "bác sĩ chuyên khoa": 3.0,
            "phác đồ điều trị": 3.0, "khám bệnh định kỳ": 3.0
        }
    },
    "Thể thao": {
        "keywords": {
            "bóng đá": 2.0, "cầu thủ": 2.0, "vận động viên": 2.0, "trận đấu": 2.0,
            "thi đấu": 2.0, "huấn luyện viên": 2.0, "ghi bàn": 2.0, "giải đấu": 2.0,
            "sân vận động": 2.0, "trọng tài": 2.0, "đội bóng": 2.0, "bóng rổ": 2.0,
            "chiến thuật": 1.5, "chuyền bóng": 2.0, "sút bóng": 2.0, "huy chương": 2.0,
            "tỷ số": 1.5, "khởi động": 1.0, "thể lực": 1.0
        },
        "strong_phrases": {
            "trận đấu": 3.0, "ghi bàn": 3.0, "sân vận động": 3.0,
            "huấn luyện viên": 3.0, "đội bóng": 3.0, "vận động viên": 3.0,
            "chiến thuật pressing": 3.0, "đội hình thi đấu": 3.0
        }
    }
}

SAMPLE_DATA = [
    {"text": "Phòng công nghệ vừa nâng cấp hệ thống máy tính và máy chủ để xử lý dữ liệu khách hàng an toàn hơn.", "label": "Công nghệ"},
    {"text": "Nhóm lập trình đang phát triển phần mềm quản lý kho bằng thuật toán tối ưu và cơ sở dữ liệu tập trung.", "label": "Công nghệ"},
    {"text": "Doanh nghiệp triển khai điện toán đám mây để lưu trữ dữ liệu và đồng bộ ứng dụng trên nhiều thiết bị.", "label": "Công nghệ"},
    {"text": "Chuyên gia an ninh mạng kiểm tra lỗ hổng bảo mật thông tin của website và hệ thống đăng nhập nội bộ.", "label": "Công nghệ"},
    {"text": "Kỹ sư tự động hóa thiết kế robot công nghiệp giúp dây chuyền sản xuất vận hành chính xác hơn.", "label": "Công nghệ"},
    {"text": "Trung tâm nghiên cứu trí tuệ nhân tạo huấn luyện mô hình nhận dạng hình ảnh cho thiết bị thông minh.", "label": "Công nghệ"},
    {"text": "Đội phát triển ứng dụng di động đang tối ưu giao diện và tốc độ phản hồi của phần mềm bán hàng.", "label": "Công nghệ"},
    {"text": "Hệ thống camera thông minh kết hợp cảm biến và thuật toán để nhận diện phương tiện trên đường phố.", "label": "Công nghệ"},
    {"text": "Lập trình viên sử dụng Python để xây dựng API kết nối cơ sở dữ liệu với nền tảng thương mại điện tử.", "label": "Công nghệ"},
    {"text": "Công nghệ số đang thay đổi cách doanh nghiệp phân tích dữ liệu và quản lý quy trình hoạt động.", "label": "Công nghệ"},

    {"text": "Giáo viên chuẩn bị bài giảng mới để học sinh dễ tiếp cận kiến thức trong môn khoa học tự nhiên.", "label": "Giáo dục"},
    {"text": "Nhà trường tổ chức kỳ thi cuối kỳ và sắp xếp phòng học phù hợp cho từng lớp học.", "label": "Giáo dục"},
    {"text": "Sinh viên năm nhất được hướng dẫn phương pháp học tập hiệu quả và kỹ năng ghi chép trong giảng đường.", "label": "Giáo dục"},
    {"text": "Thư viện trường học bổ sung giáo trình và sách vở phục vụ chương trình đào tạo mới.", "label": "Giáo dục"},
    {"text": "Giáo viên chủ nhiệm trao đổi với phụ huynh về điểm số và kế hoạch ôn tập của học sinh.", "label": "Giáo dục"},
    {"text": "Lớp học trực tuyến giúp sinh viên tiếp cận bài giảng online và tài liệu tham khảo mọi lúc.", "label": "Giáo dục"},
    {"text": "Khoa ngoại ngữ cập nhật giáo trình để nâng cao kỹ năng giao tiếp cho sinh viên trong từng môn học.", "label": "Giáo dục"},
    {"text": "Trung tâm đào tạo mở khóa bồi dưỡng nghiệp vụ giảng dạy dành cho giáo viên trẻ.", "label": "Giáo dục"},
    {"text": "Buổi tư vấn định hướng nghề nghiệp giúp học sinh hiểu rõ năng lực và chọn ngành phù hợp.", "label": "Giáo dục"},
    {"text": "Nhà trường áp dụng phương pháp giảng dạy theo dự án để tăng khả năng hợp tác và tự học của học sinh.", "label": "Giáo dục"},

    {"text": "Bác sĩ khuyến cáo người dân khám bệnh định kỳ để phát hiện sớm triệu chứng của bệnh tim mạch.", "label": "Sức khỏe"},
    {"text": "Chế độ ăn cân bằng với rau xanh và nước uống đầy đủ giúp cơ thể duy trì sức đề kháng tốt.", "label": "Sức khỏe"},
    {"text": "Bệnh viện triển khai khu điều trị mới cho bệnh nhân cần theo dõi huyết áp và nhịp tim liên tục.", "label": "Sức khỏe"},
    {"text": "Giấc ngủ sâu và tinh thần ổn định đóng vai trò quan trọng trong quá trình phục hồi của cơ thể.", "label": "Sức khỏe"},
    {"text": "Người bệnh cần uống thuốc đúng liều theo chỉ định của bác sĩ chuyên khoa để đạt hiệu quả điều trị.", "label": "Sức khỏe"},
    {"text": "Chuyên gia dinh dưỡng xây dựng chế độ ăn phù hợp cho trẻ em đang cần tăng cường miễn dịch.", "label": "Sức khỏe"},
    {"text": "Bệnh nhân có triệu chứng ho kéo dài nên đến bệnh viện xét nghiệm và nhận phác đồ điều trị sớm.", "label": "Sức khỏe"},
    {"text": "Việc phòng bệnh bằng vệ sinh cá nhân và tiêm ngừa giúp giảm nguy cơ lây nhiễm trong cộng đồng.", "label": "Sức khỏe"},
    {"text": "Khám sức khỏe tổng quát giúp theo dõi chỉ số đường huyết, huyết áp và chức năng gan định kỳ.", "label": "Sức khỏe"},
    {"text": "Tập thói quen ngủ đúng giờ và ăn sáng lành mạnh giúp cải thiện thể trạng và tinh thần lâu dài.", "label": "Sức khỏe"},

    {"text": "Đội bóng giành chiến thắng trong trận đấu quyết định sau pha ghi bàn ở phút cuối cùng.", "label": "Thể thao"},
    {"text": "Huấn luyện viên điều chỉnh chiến thuật pressing để các cầu thủ kiểm soát thế trận tốt hơn.", "label": "Thể thao"},
    {"text": "Vận động viên quốc gia đang tập luyện cho giải đấu điền kinh và đặt mục tiêu giành huy chương vàng.", "label": "Thể thao"},
    {"text": "Trọng tài xác nhận bàn thắng hợp lệ sau khi xem lại tình huống tranh chấp trong sân vận động.", "label": "Thể thao"},
    {"text": "Cầu thủ trẻ được đưa vào đội hình thi đấu chính thức nhờ tốc độ và khả năng chuyền bóng chính xác.", "label": "Thể thao"},
    {"text": "Giải bóng rổ học đường thu hút đông khán giả đến xem các đội thi đấu vòng loại sôi nổi.", "label": "Thể thao"},
    {"text": "Đội tuyển bóng đá nữ đang hoàn thiện chiến thuật phản công trước trận đấu với đối thủ mạnh.", "label": "Thể thao"},
    {"text": "Khán giả cổ vũ cuồng nhiệt khi tiền đạo sút bóng từ xa và nâng tỷ số lên hai không.", "label": "Thể thao"},
    {"text": "Ban huấn luyện theo dõi thể lực của vận động viên trước khi đăng ký danh sách thi đấu chính thức.", "label": "Thể thao"},
    {"text": "Câu lạc bộ tổ chức buổi khởi động và rèn kỹ năng dứt điểm cho các cầu thủ trẻ.", "label": "Thể thao"},
]


def normalize_text(text):
    return text.lower().strip()


def clean_text(text):
    text = re.sub(
        r"[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
        " ",
        text,
    )
    text = re.sub(r"_", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text):
    if not text:
        return []
    return [token for token in text.split() if token]


def remove_stopwords(tokens):
    return [token for token in tokens if token not in STOPWORDS]


def extract_phrases(text):
    cleaned_text = clean_text(normalize_text(text))
    tokens = tokenize(cleaned_text)
    phrases = []
    for size in (2, 3):
        for index in range(len(tokens) - size + 1):
            phrases.append(" ".join(tokens[index:index + size]))
    return phrases


def preprocess_text(text):
    normalized_text = normalize_text(text)
    cleaned_text = clean_text(normalized_text)
    raw_tokens = tokenize(cleaned_text)
    filtered_tokens = remove_stopwords(raw_tokens)
    phrases = extract_phrases(cleaned_text)
    return {
        "normalized_text": normalized_text,
        "cleaned_text": cleaned_text,
        "raw_tokens": raw_tokens,
        "tokens": filtered_tokens,
        "phrases": phrases,
    }


def build_vocabulary(dataset):
    vocabulary = []
    seen = set()
    for item in dataset:
        processed = preprocess_text(item["text"])
        for token in processed["tokens"]:
            if token not in seen:
                seen.add(token)
                vocabulary.append(token)
    return vocabulary


def text_to_vector(text, vocabulary):
    if isinstance(text, str):
        tokens = preprocess_text(text)["tokens"]
    else:
        tokens = list(text)
    token_counter = Counter(tokens)
    return [token_counter.get(word, 0) for word in vocabulary]


def cosine_similarity(vector1, vector2):
    dot_product = sum(left * right for left, right in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(value * value for value in vector1))
    magnitude2 = math.sqrt(sum(value * value for value in vector2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


def build_topic_profiles(dataset, vocabulary):
    grouped_tokens = defaultdict(list)
    for item in dataset:
        grouped_tokens[item["label"]].extend(preprocess_text(item["text"])["tokens"])

    topic_profiles = {}
    for topic, tokens in grouped_tokens.items():
        topic_profiles[topic] = text_to_vector(tokens, vocabulary)
    return topic_profiles


VOCABULARY = build_vocabulary(SAMPLE_DATA)
TOPIC_PROFILES = build_topic_profiles(SAMPLE_DATA, VOCABULARY)


def match_weighted_terms(processed_text, weighted_terms):
    cleaned_text = processed_text["cleaned_text"]
    tokens = processed_text["tokens"]
    phrases = processed_text["phrases"]
    matches = []

    for term, weight in weighted_terms.items():
        if " " in term:
            if term in cleaned_text or term in phrases:
                matches.append((term, weight))
        elif term in tokens:
            matches.append((term, weight))
    return matches


def calculate_keyword_score(text, topic):
    processed_text = preprocess_text(text)
    matches = match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["keywords"])
    return sum(weight for _, weight in matches), [term for term, _ in matches]


def calculate_phrase_score(text, topic):
    processed_text = preprocess_text(text)
    matches = match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["strong_phrases"])
    return sum(weight for _, weight in matches), [term for term, _ in matches]


def calculate_conflict_penalty(text, topic):
    processed_text = preprocess_text(text)
    own_keywords = set(term for term, _ in match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["keywords"]))
    own_phrases = set(term for term, _ in match_weighted_terms(processed_text, TOPIC_CONFIG[topic]["strong_phrases"]))

    penalty = 0.0
    details = []
    own_signal = len(own_keywords) + (2 * len(own_phrases))

    for other_topic in TOPICS:
        if other_topic == topic:
            continue

        other_keyword_matches = match_weighted_terms(processed_text, TOPIC_CONFIG[other_topic]["keywords"])
        other_phrase_matches = match_weighted_terms(processed_text, TOPIC_CONFIG[other_topic]["strong_phrases"])

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


def apply_context_priority(topic, keyword_matches, phrase_matches):
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


def assess_confidence(sorted_scores):
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


def calculate_relative_percentages(sorted_scores):
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


def predict_topic(text):
    processed_text = preprocess_text(text)
    input_vector = text_to_vector(processed_text["tokens"], VOCABULARY)
    score_breakdown = {}
    topic_scores = []

    for topic in TOPICS:
        cosine_score = cosine_similarity(input_vector, TOPIC_PROFILES[topic])
        keyword_score, keyword_matches = calculate_keyword_score(text, topic)
        phrase_score, phrase_matches = calculate_phrase_score(text, topic)
        conflict_penalty, conflict_details = calculate_conflict_penalty(text, topic)
        context_bonus = apply_context_priority(topic, keyword_matches, phrase_matches)

        final_score = cosine_score + keyword_score + phrase_score + context_bonus - conflict_penalty

        score_breakdown[topic] = {
            "cosine_score": cosine_score,
            "keyword_score": keyword_score,
            "phrase_score": phrase_score,
            "context_bonus": context_bonus,
            "conflict_penalty": conflict_penalty,
            "final_score": final_score,
            "keyword_matches": keyword_matches,
            "phrase_matches": phrase_matches,
            "conflict_details": conflict_details,
        }
        topic_scores.append((topic, final_score))

    sorted_scores = sorted(topic_scores, key=lambda item: item[1], reverse=True)
    predicted_topic = sorted_scores[0][0] if sorted_scores else "Không xác định"
    confidence, ambiguity_warning = assess_confidence(sorted_scores)
    relative_percentages = calculate_relative_percentages(sorted_scores)

    return {
        "predicted_topic": predicted_topic,
        "confidence": confidence,
        "ambiguity_warning": ambiguity_warning,
        "scores": sorted_scores,
        "relative_percentages": relative_percentages,
        "score_breakdown": score_breakdown,
        "processed": processed_text,
    }


def explain_prediction(text, scores):
    predicted_topic = scores["predicted_topic"]
    detail = scores["score_breakdown"][predicted_topic]
    parts = [
        f"Hệ thống chọn chủ đề {predicted_topic.lower()} vì chủ đề này có tổng điểm cao nhất là {detail['final_score']:.4f}.",
        f"Công thức chấm điểm gồm cosine={detail['cosine_score']:.4f}, keyword={detail['keyword_score']:.2f}, phrase={detail['phrase_score']:.2f}, context_bonus={detail['context_bonus']:.2f}, penalty={detail['conflict_penalty']:.2f}.",
    ]

    if detail["keyword_matches"]:
        parts.append(f"Từ khóa nổi bật: {', '.join(detail['keyword_matches'][:8])}.")
    if detail["phrase_matches"]:
        parts.append(f"Cụm từ đặc trưng: {', '.join(detail['phrase_matches'][:6])}.")
    if detail["conflict_details"]:
        parts.append("Tín hiệu gây nhiễu được phát hiện: " + "; ".join(detail["conflict_details"][:6]) + ".")

    if scores["ambiguity_warning"]:
        parts.append(scores["ambiguity_warning"])

    if len(preprocess_text(text)["raw_tokens"]) < 8:
        parts.append("Văn bản khá ngắn nên mức ổn định của dự đoán có thể giảm.")

    return " ".join(parts)


def build_basic_python_report(dataset):
    lines = [
        "PHẦN KIẾN THỨC PYTHON CƠ BẢN",
        f"Tổng số văn bản mẫu: {len(dataset)}",
        "",
    ]

    for index, item in enumerate(dataset, start=1):
        processed = preprocess_text(item["text"])
        lines.append(f"{index}. Nhãn: {item['label']}")
        lines.append(f"   Văn bản gốc: {item['text']}")
        lines.append(f"   Chữ thường: {processed['normalized_text']}")
        lines.append(f"   Sau làm sạch: {processed['cleaned_text']}")
        lines.append(f"   Số từ gốc: {len(processed['raw_tokens'])}")
        lines.append(f"   Tách từ cơ bản: {processed['raw_tokens']}")
        lines.append(f"   Số từ sau bỏ stopwords: {len(processed['tokens'])}")
        lines.append(f"   Danh sách từ sau bỏ stopwords: {processed['tokens']}")
        lines.append("")

    return "\n".join(lines)


def save_history(record):
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                history = json.load(file)
        except (json.JSONDecodeError, OSError):
            history = []

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
