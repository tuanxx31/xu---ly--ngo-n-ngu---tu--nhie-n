# Phân Tích Kỹ Thuật NLP Trong Source Code

## Tổng Quan Hệ Thống

Đây là hệ thống **phân loại chủ đề văn bản tiếng Việt** (Text Classification) cho 4 chủ đề: Công nghệ, Giáo dục, Sức khỏe, Thể thao. Hệ thống sử dụng phương pháp **rule-based kết hợp thống kê**, không dùng machine learning hay deep learning.

### Công thức tính điểm tổng hợp:

```
final_score = cosine_score + keyword_score + phrase_score + context_bonus - conflict_penalty
```

Chủ đề có `final_score` cao nhất sẽ được chọn làm kết quả dự đoán.

---

## 1. Text Preprocessing Pipeline (Tiền xử lý văn bản)

> **IMPORTANT**: Đây là bước nền tảng — mọi kỹ thuật NLP phía sau đều phụ thuộc vào kết quả tiền xử lý.

### Quy trình 5 bước

Được orchestrate tại `application/topic_analyzer.py` → hàm `preprocess_text()` (dòng 60–72):

```
Văn bản gốc → 1. Normalize (lowercase) → 2. Clean (loại ký tự đặc biệt) → 3. Tokenize (tách từ) → 4. Remove Stopwords (loại từ dừng)
                                                                           ↘ 5. Extract Phrases (trích cụm n-gram)
```

---

### 1.1 Text Normalization (Chuẩn hóa văn bản)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Lowercasing |
| **Vị trí** | `application/topic_analyzer.py` → `normalize_text()` (dòng 30–31) |

```python
def normalize_text(self, text: str) -> str:
    return text.lower().strip()
```

**Mục đích**: Đưa toàn bộ văn bản về chữ thường để so khớp không phân biệt hoa/thường. Ví dụ `"AI"` → `"ai"`, `"Python"` → `"python"`.

---

### 1.2 Text Cleaning (Làm sạch văn bản)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Regex-based cleaning giữ lại ký tự tiếng Việt |
| **Vị trí** | `application/topic_analyzer.py` → `clean_text()` (dòng 33–41) |

```python
def clean_text(self, text: str) -> str:
    text = re.sub(
        r"[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
        " ", text,
    )
    text = re.sub(r"_", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
```

**Mục đích**: Loại bỏ dấu câu, ký tự đặc biệt nhưng **giữ lại toàn bộ dấu tiếng Việt** (à, á, ả, ã, ạ, ă, â, đ, ...). Đây là điểm quan trọng khi xử lý NLP tiếng Việt — regex pattern phải liệt kê rõ ràng các ký tự có dấu.

**3 bước regex**:
1. Thay ký tự không phải chữ/số/khoảng trắng/tiếng Việt bằng dấu cách
2. Thay dấu gạch dưới `_` bằng dấu cách
3. Gộp nhiều khoảng trắng liên tiếp thành 1

---

### 1.3 Tokenization (Tách từ)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Whitespace Tokenization (tách theo khoảng trắng) |
| **Vị trí** | `application/topic_analyzer.py` → `tokenize()` (dòng 43–46) |

```python
def tokenize(self, text: str) -> List[str]:
    if not text:
        return []
    return [token for token in text.split() if token]
```

> **NOTE**: Đây là tokenizer đơn giản nhất — tách theo khoảng trắng. Tiếng Việt có đặc thù **từ ghép** (ví dụ "trí tuệ nhân tạo" là 1 từ nhưng sẽ bị tách thành 4 token). Source code giải quyết vấn đề này bằng kỹ thuật **N-gram Phrase Extraction** ở bước 5.

---

### 1.4 Stopword Removal (Loại bỏ từ dừng)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Danh sách từ dừng tiếng Việt tĩnh |
| **Vị trí** | `application/topic_analyzer.py` → `remove_stopwords()` (dòng 48–49) + `domain/topic_config.py` → `STOPWORDS` (dòng 9–17) |

```python
STOPWORDS = {
    "là", "và", "của", "có", "trong", "một", "những", "các", "cho", "với",
    "được", "khi", "để", "thì", "mà", "này", "đó", "cũng", "rất", "nhiều",
    "về", "từ", "đang", "trên", "theo", "vào", "ra", "ở", "tại", "do", "vì",
    "nên", "đã", "sẽ", "cần", "hơn", "giúp", "việc", "mỗi", "như", "hay",
    "bị", "đến", "cùng", "qua", "lại", "thêm", "nhằm", "sau", "trước",
    "ít", "vẫn", "đều", "vừa", "mới", "rằng", "thật", "sự", "kia", "ấy",
    "nơi", "đây",
}

def remove_stopwords(self, tokens):
    return [token for token in tokens if token not in STOPWORDS]
```

**Mục đích**: Loại bỏ ~62 từ chức năng tiếng Việt (là, và, của, có, trong, ...) — những từ xuất hiện ở mọi chủ đề, không mang thông tin phân biệt. Dùng `set` nên tra cứu O(1).

---

### 1.5 N-gram Phrase Extraction (Trích xuất cụm từ n-gram)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Sliding window N-gram (bigram, trigram, 4-gram) |
| **Vị trí** | `application/topic_analyzer.py` → `extract_phrases()` (dòng 51–58) |

```python
def extract_phrases(self, text: str) -> List[str]:
    cleaned_text = self.clean_text(self.normalize_text(text))
    tokens = self.tokenize(cleaned_text)
    phrases = []
    for size in (2, 3, 4):
        for index in range(len(tokens) - size + 1):
            phrases.append(" ".join(tokens[index:index + size]))
    return phrases
```

**Mục đích**: Giải quyết bài toán từ ghép tiếng Việt. Sinh ra tất cả cụm 2, 3, 4 từ liên tiếp.

**Ví dụ**: Câu `"trí tuệ nhân tạo giúp"` sẽ sinh ra:
- Bigram: `"trí tuệ"`, `"tuệ nhân"`, `"nhân tạo"`, `"tạo giúp"`
- Trigram: `"trí tuệ nhân"`, `"tuệ nhân tạo"`, `"nhân tạo giúp"`
- 4-gram: `"trí tuệ nhân tạo"`, `"tuệ nhân tạo giúp"`

Cụm `"trí tuệ nhân tạo"` sau đó sẽ được match với danh sách strong_phrases.

> **TIP**: Kỹ thuật này chạy **trước** bước loại stopwords (dùng `cleaned_text` thay vì `tokens` đã lọc), đảm bảo các cụm từ tự nhiên không bị phá vỡ.

---

## 2. Bag-of-Words + Cosine Similarity

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Vector Space Model (VSM) với Cosine Similarity |
| **Vị trí** | `application/topic_analyzer.py` → `text_to_vector()` (dòng 85–91), `cosine_similarity()` (dòng 93–99), `build_topic_profiles()` (dòng 101–109) |

### 2.1 Xây dựng Vocabulary

`build_vocabulary()` (dòng 74–83) — quét toàn bộ dataset, thu thập tất cả từ (đã loại stopwords) theo thứ tự xuất hiện đầu tiên, tạo ra vocabulary duy nhất.

### 2.2 Text → Vector (Bag-of-Words)

```python
def text_to_vector(self, text_or_tokens, vocabulary):
    token_counter = Counter(tokens)
    return [token_counter.get(word, 0) for word in vocabulary]
```

Chuyển văn bản thành vector đếm tần suất từ, kích thước = kích thước vocabulary. Mỗi phần tử là số lần xuất hiện của từ tương ứng.

### 2.3 Topic Profile

`build_topic_profiles()` (dòng 101–109) — gộp tất cả token của các văn bản cùng chủ đề lại thành 1 "siêu văn bản", rồi chuyển thành vector. Mỗi chủ đề có 1 vector đại diện (centroid).

### 2.4 Cosine Similarity

```python
def cosine_similarity(self, vector1, vector2):
    dot_product = sum(left * right for left, right in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(value * value for value in vector1))
    magnitude2 = math.sqrt(sum(value * value for value in vector2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)
```

**Công thức**: `cos(A, B) = (A · B) / (|A| × |B|)`, giá trị từ 0 đến 1.

Đo mức độ tương đồng giữa vector văn bản đầu vào và vector profile của từng chủ đề. Cosine similarity đo **hướng** (phân phối từ) chứ không phụ thuộc **độ dài** văn bản.

---

## 3. Weighted Keyword Matching (So khớp từ khóa có trọng số)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Dictionary-based keyword matching với trọng số tĩnh |
| **Vị trí** | `application/topic_analyzer.py` → `match_weighted_terms()` (dòng 111–123), `calculate_keyword_score()` (dòng 125–128) |

```python
def match_weighted_terms(self, processed_text, weighted_terms):
    for term, weight in weighted_terms.items():
        if " " in term:                        # Cụm từ → tìm trong text hoặc phrases
            if term in cleaned_text or term in phrases:
                matches.append((term, weight))
        elif term in tokens:                   # Từ đơn → tìm trong tokens
            matches.append((term, weight))
    return matches
```

**Cách hoạt động**:
- Mỗi chủ đề có danh sách `keywords` với trọng số 1.0–2.0
- Từ đơn (như `"thuốc"`) → tìm trong danh sách token
- Cụm từ (như `"trí tuệ nhân tạo"`) → tìm trong chuỗi text gốc hoặc danh sách phrases
- Tổng trọng số các từ khóa matched = `keyword_score`

**Cấu hình tại** `domain/topic_config.py` → `TOPIC_CONFIG` (dòng 19–77):

| Trọng số | Ý nghĩa | Ví dụ |
|---|---|---|
| 2.0 | Từ khóa đặc trưng mạnh | `"lập trình"`, `"bác sĩ"`, `"cầu thủ"` |
| 1.5 | Từ khóa phổ biến trong chủ đề | `"hệ thống"`, `"rau xanh"`, `"chiến thuật"` |
| 1.0 | Từ khóa chung, có thể xuất hiện nhiều chủ đề | `"ứng dụng"`, `"bệnh"`, `"sức khỏe"` |

---

## 4. Strong Phrase Matching (So khớp cụm từ mạnh)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Phrase-level matching với trọng số cao |
| **Vị trí** | `application/topic_analyzer.py` → `calculate_phrase_score()` (dòng 130–133) |

Tương tự keyword matching nhưng dùng danh sách `strong_phrases` — đều có trọng số **3.0**, cao hơn từ đơn. Các cụm từ này gần như chắc chắn thuộc một chủ đề cụ thể.

**Ví dụ strong_phrases**:
- Công nghệ: `"trí tuệ nhân tạo"`, `"cơ sở dữ liệu"`, `"an ninh mạng"`
- Giáo dục: `"học trực tuyến"`, `"phương pháp giảng dạy"`
- Sức khỏe: `"phác đồ điều trị"`, `"bác sĩ chuyên khoa"`
- Thể thao: `"chiến thuật pressing"`, `"đội hình thi đấu"`

---

## 5. Conflict Penalty (Phạt xung đột chủ đề)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Cross-topic penalty with signal-based scaling |
| **Vị trí** | `application/topic_analyzer.py` → `calculate_conflict_penalty()` (dòng 135–190) |

> **IMPORTANT**: Đây là kỹ thuật phức tạp nhất trong hệ thống, xử lý trường hợp văn bản chứa từ khóa của **nhiều chủ đề khác nhau**.

**Thuật toán**:

```
Với mỗi chủ đề X đang xét:
  1. Tìm keyword/phrase match của X (own_keywords, own_phrases)
  2. Duyệt các chủ đề khác Y ≠ X:
     a. Tìm keyword/phrase match của Y trong văn bản
     b. Nếu từ đó cũng thuộc X → Bỏ qua (không phạt)
     c. Nếu từ chỉ thuộc Y:
        - Keyword trọng số ≥ 2.0 → penalty += 0.75
        - Keyword trọng số < 2.0 → penalty += 0.50
        - Cụm từ mạnh → penalty += 1.0
  3. Điều chỉnh penalty theo own_signal:
     - own_signal = len(own_keywords) + 2 × len(own_phrases)
     - own_signal ≥ 3 → penalty × 0.6
     - own_signal ≥ 1 → penalty × 0.8
     - own_signal = 0 → penalty giữ nguyên
```

**Điểm đặc biệt**:
- Nếu 1 từ thuộc **cả chủ đề đang xét lẫn chủ đề khác** → không bị phạt (tránh phạt nhầm)
- `own_signal` — nếu chủ đề đang xét có **nhiều tín hiệu riêng** thì penalty giảm (×0.6), vì hệ thống tin rằng chủ đề đó đủ mạnh
- Keyword trọng số cao (≥2.0) bị phạt nặng hơn (0.75 vs 0.50)

---

## 6. Context Priority Boosting (Tăng cường theo ngữ cảnh)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Rule-based context boost |
| **Vị trí** | `application/topic_analyzer.py` → `apply_context_priority()` (dòng 192–221) |

Hand-crafted rules để boost điểm khi phát hiện **tổ hợp từ khóa/cụm từ đặc trưng**:

```python
if topic == "Giáo dục":
    if "học trực tuyến" in phrase_set or "bài giảng online" in phrase_set:
        boost += 1.8
    if "lớp học" in phrase_set and "bài giảng" in phrase_set:
        boost += 1.2
```

**Ý tưởng**: Một từ đơn lẻ có thể mơ hồ, nhưng **sự kết hợp** nhiều từ khóa đặc trưng là tín hiệu rất mạnh. Ví dụ: `"bác sĩ"` + `"bệnh viện"` cùng xuất hiện → gần chắc chắn là Sức khỏe.

---

## 7. Confidence Assessment (Đánh giá độ tin cậy)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Gap-ratio based confidence scoring |
| **Vị trí** | `application/topic_analyzer.py` → `assess_confidence()` (dòng 223–239) |

```python
gap_ratio = abs(top_score - second_score) / max(abs(top_score), 0.0001)
```

| Gap Ratio | Kết quả |
|---|---|
| < 0.10 | **Thấp** — khoảng cách quá nhỏ, có thể nhầm |
| 0.10 – 0.25 | **Trung bình** |
| > 0.25 | **Cao** — chủ đề top vượt trội |

---

## 8. Relative Percentage (Phần trăm tương đối)

| Thuộc tính | Giá trị |
|---|---|
| **Kỹ thuật** | Min-shifted score normalization |
| **Vị trí** | `application/topic_analyzer.py` → `calculate_relative_percentages()` (dòng 241–256) |

```python
minimum_score = min(score for _, score in sorted_scores)
shifted_scores = [(topic, score - minimum_score + 0.001) for topic, score in sorted_scores]
```

Dịch tất cả điểm lên sao cho điểm thấp nhất → 0.001, rồi tính tỷ lệ phần trăm. Giúp hiển thị kết quả trực quan cho người dùng.

---

## 9. Pipeline Tổng Hợp

Tại `application/topic_analyzer.py` → `predict_topic()` (dòng 258–298) — hàm chính kết hợp tất cả kỹ thuật:

```
Văn bản đầu vào
    ↓
Preprocess Text (normalize → clean → tokenize → stopwords → n-gram)
    ↓
Text → Vector (BoW)
    ↓
Với mỗi chủ đề (4 topics):
    ├── Cosine Similarity với topic profile
    ├── Keyword Matching (trọng số 1.0–2.0)
    ├── Phrase Matching (trọng số 3.0)
    ├── Conflict Penalty (phạt xung đột)
    └── Context Boost (tăng ngữ cảnh)
    ↓
final = cosine + keyword + phrase + context - penalty
    ↓
Sắp xếp giảm dần → Chọn chủ đề điểm cao nhất
    ↓
Đánh giá confidence + Tính phần trăm
    ↓
TopicPrediction
```

---

## Tóm Tắt Kỹ Thuật NLP

| # | Kỹ thuật | File | Dòng | Mô tả |
|---|---|---|---|---|
| 1 | **Text Normalization** | `topic_analyzer.py` | L30–31 | Lowercase + strip |
| 2 | **Regex Cleaning (Vietnamese)** | `topic_analyzer.py` | L33–41 | Loại ký tự đặc biệt, giữ dấu tiếng Việt |
| 3 | **Whitespace Tokenization** | `topic_analyzer.py` | L43–46 | Tách từ theo khoảng trắng |
| 4 | **Stopword Removal** | `topic_analyzer.py` | L48–49 | Loại 62 từ dừng tiếng Việt |
| 5 | **N-gram Extraction** | `topic_analyzer.py` | L51–58 | Sinh bigram, trigram, 4-gram |
| 6 | **Bag-of-Words** | `topic_analyzer.py` | L85–91 | Chuyển text → frequency vector |
| 7 | **Cosine Similarity** | `topic_analyzer.py` | L93–99 | Đo độ tương đồng vector |
| 8 | **Topic Profile (Centroid)** | `topic_analyzer.py` | L101–109 | Vector đại diện mỗi chủ đề |
| 9 | **Weighted Keyword Matching** | `topic_analyzer.py` | L111–128 | So khớp từ khóa có trọng số |
| 10 | **Strong Phrase Matching** | `topic_analyzer.py` | L130–133 | So khớp cụm từ đặc trưng mạnh |
| 11 | **Cross-topic Conflict Penalty** | `topic_analyzer.py` | L135–190 | Phạt từ khóa thuộc chủ đề khác |
| 12 | **Context Priority Boost** | `topic_analyzer.py` | L192–221 | Tăng điểm khi có tổ hợp đặc trưng |
| 13 | **Gap-ratio Confidence** | `topic_analyzer.py` | L223–239 | Đánh giá mức tin cậy kết quả |
| 14 | **Min-shift Normalization** | `topic_analyzer.py` | L241–256 | Tính phần trăm tương đối |

> **NOTE**: Toàn bộ logic NLP nằm gần như trọn vẹn trong file `application/topic_analyzer.py` (344 dòng), với cấu hình từ khóa/cụm từ tại `domain/topic_config.py` và data model tại `domain/entities.py`.
