# 🎓 HỆ THỐNG GỢI Ý CHỦ ĐỀ BÀI VIẾT NGẮN

> **Môn học:** Xử lý Ngôn ngữ Tự nhiên (NLP)  
> **Ngôn ngữ lập trình:** Python  
> **Giao diện:** Tkinter (Desktop GUI)  
> **Đặc điểm nổi bật:** Không sử dụng bất kỳ thư viện Machine Learning / NLP có sẵn nào (không dùng scikit-learn, NLTK, spaCy, ...). Toàn bộ thuật toán được lập trình thủ công (from scratch).

---

## 📋 MỤC LỤC

1. [Tổng quan nhanh (Quick Overview)](#-tổng-quan-nhanh)
2. [Mô tả bài toán](#-mô-tả-bài-toán)
3. [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
4. [Pipeline xử lý](#-pipeline-xử-lý---8-bước)
5. [Chi tiết các kỹ thuật NLP](#-chi-tiết-các-kỹ-thuật-nlp)
   - [5.1. Text Normalization](#51-text-normalization---chuẩn-hóa-văn-bản)
   - [5.2. Text Cleaning](#52-text-cleaning---làm-sạch-văn-bản)
   - [5.3. Tokenization](#53-tokenization---tách-từ)
   - [5.4. Stopword Removal](#54-stopword-removal---loại-bỏ-từ-dừng)
   - [5.5. N-gram Extraction](#55-n-gram-extraction---trích-xuất-cụm-từ)
   - [5.6. Bag of Words (BoW)](#56-bag-of-words-bow---túi-từ)
   - [5.7. Cosine Similarity](#57-cosine-similarity---độ-tương-đồng-cosine)
   - [5.8. Weighted Keyword Matching](#58-weighted-keyword-matching---đối-sánh-từ-khóa-có-trọng-số)
   - [5.9. Conflict Penalty](#59-conflict-penalty---phạt-tín-hiệu-gây-nhiễu)
   - [5.10. Confidence Assessment](#510-confidence-assessment---đánh-giá-độ-tin-cậy)
6. [Công thức tính điểm tổng hợp](#-công-thức-tính-điểm-tổng-hợp)
7. [Dữ liệu mẫu](#-dữ-liệu-mẫu)
8. [Cách chạy chương trình](#-cách-chạy-chương-trình)
9. [Cấu trúc thư mục](#-cấu-trúc-thư-mục)

---

## 🚀 TỔNG QUAN NHANH

### Dự án làm gì?

Hệ thống nhận **một đoạn văn bản tiếng Việt** do người dùng nhập vào (hoặc import từ file `.txt`, `.docx`, `.pdf`), sau đó **tự động phân loại** đoạn văn đó thuộc **1 trong 4 chủ đề**: **Công nghệ**, **Giáo dục**, **Sức khỏe**, **Thể thao**.

### Các kỹ thuật NLP được sử dụng (tóm tắt nhanh)

| # | Kỹ thuật | Ý tưởng cốt lõi | Vai trò trong dự án |
|---|----------|-----------------|---------------------|
| 1 | **Text Normalization** | Đưa văn bản về dạng chuẩn (chữ thường) | Tiền xử lý – loại bỏ sự khác biệt hoa/thường |
| 2 | **Text Cleaning** | Loại bỏ ký tự đặc biệt, dấu câu, khoảng trắng thừa | Tiền xử lý – giữ lại chữ cái & dấu tiếng Việt |
| 3 | **Tokenization** | Tách văn bản thành danh sách các từ (token) | Tiền xử lý – cơ sở cho mọi bước phân tích sau |
| 4 | **Stopword Removal** | Loại bỏ các từ phổ biến không mang ý nghĩa phân loại | Tiền xử lý – giảm nhiễu, tăng chất lượng đặc trưng |
| 5 | **N-gram Extraction** | Tạo cụm 2, 3, 4 từ liên tiếp | Trích đặc trưng – bắt cụm từ mang ngữ nghĩa mạnh |
| 6 | **Bag of Words (BoW)** | Biểu diễn văn bản bằng vector đếm tần suất từ | Biểu diễn – chuyển text sang dạng toán học |
| 7 | **Cosine Similarity** | Đo góc giữa 2 vector để tính độ tương đồng | So sánh – tính mức độ giống nhau giữa văn bản và hồ sơ chủ đề |
| 8 | **Weighted Keyword Matching** | Đối sánh từ/cụm từ đặc trưng với trọng số cho trước | Chấm điểm – tăng điểm khi gặp từ khóa đặc thù |
| 9 | **Conflict Penalty** | Phạt khi văn bản chứa tín hiệu thuộc chủ đề khác | Chấm điểm – giảm nhầm lẫn khi văn bản đa chủ đề |
| 10 | **Confidence Assessment** | Đánh giá khoảng cách điểm giữa chủ đề cao nhất và nhì | Đánh giá – cho người dùng biết kết quả đáng tin cỡ nào |

### Công thức chấm điểm

```
Điểm cuối = Cosine_Similarity + Keyword_Score + Phrase_Score + Context_Bonus − Conflict_Penalty
```

Chủ đề có **điểm cuối cao nhất** được chọn làm kết quả dự đoán.

---

## 📝 MÔ TẢ BÀI TOÁN

| Tiêu chí | Chi tiết |
|----------|---------|
| **Bài toán** | Phân loại văn bản (Text Classification) |
| **Đầu vào** | Một đoạn văn bản tiếng Việt (tối thiểu 5 từ) |
| **Đầu ra** | Chủ đề dự đoán + Mức độ tin cậy + Giải thích chi tiết |
| **Số lớp (class)** | 4 chủ đề: Công nghệ, Giáo dục, Sức khỏe, Thể thao |
| **Phương pháp** | Kết hợp Cosine Similarity (BoW) + Keyword Scoring + N-gram Matching |
| **Ngôn ngữ xử lý** | Tiếng Việt |

---

## 🏗 KIẾN TRÚC HỆ THỐNG

Dự án được tổ chức theo mô hình **Clean Architecture**, chia thành 4 tầng rõ ràng:

```
┌─────────────────────────────────────────────────────┐
│                  presentation/                       │
│          (Giao diện Tkinter - tkinter_app.py)        │
├─────────────────────────────────────────────────────┤
│                  application/                        │
│     (Logic nghiệp vụ - TopicAnalyzer, Pipeline)      │
├─────────────────────────────────────────────────────┤
│                    domain/                           │
│   (Entities, Config: TextSample, TopicPrediction...) │
├─────────────────────────────────────────────────────┤
│               infrastructure/                        │
│   (Đọc file .txt/.docx/.pdf, Lưu lịch sử JSON)     │
├─────────────────────────────────────────────────────┤
│                     data/                            │
│            (Dataset 40 văn bản mẫu)                  │
└─────────────────────────────────────────────────────┘
```

| Tầng | Thư mục | Chức năng |
|------|---------|-----------|
| **Presentation** | `presentation/` | Giao diện người dùng Tkinter, biểu đồ xác suất |
| **Application** | `application/` | Class `TopicAnalyzer` – toàn bộ pipeline NLP |
| **Domain** | `domain/` | Entities (dataclass), cấu hình từ khóa, stopwords |
| **Infrastructure** | `infrastructure/` | Đọc file tài liệu, lưu/đọc lịch sử phân tích (JSON) |
| **Data** | `data/` | 40 văn bản mẫu đã gán nhãn (10 văn bản/chủ đề) |

---

## 🔄 PIPELINE XỬ LÝ - 8 BƯỚC

```
Văn bản đầu vào
      │
      ▼
┌─── Bước 1: Chuẩn hóa (Normalization) ──────────────────┐
│    Chuyển toàn bộ về chữ thường, xóa khoảng trắng đầu/cuối  │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─── Bước 2: Làm sạch (Cleaning) ────────────────────────┐
│    Xóa dấu câu, ký tự đặc biệt, giữ lại chữ cái       │
│    và dấu tiếng Việt (àáạảã, ăắặ, ...)                  │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─── Bước 3: Tách từ (Tokenization) ─────────────────────┐
│    Tách câu thành list các từ đơn bằng khoảng trắng     │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─── Bước 4: Loại bỏ Stopwords ──────────────────────────┐
│    Bỏ 62 từ dừng tiếng Việt (là, và, của, có, trong...) │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─── Bước 5: Trích xuất N-gram ──────────────────────────┐
│    Tạo cụm 2-gram, 3-gram, 4-gram từ văn bản            │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─── Bước 6: Biểu diễn BoW + Cosine Similarity ─────────┐
│    Tạo vector tần suất → tính cosine với hồ sơ chủ đề   │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─── Bước 7: Chấm điểm Keyword + Phrase + Context ──────┐
│    Cộng trọng số từ khóa, cụm từ, bonus ngữ cảnh       │
│    Trừ penalty nếu có tín hiệu nhiễu từ chủ đề khác     │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─── Bước 8: Chọn chủ đề + Đánh giá độ tin cậy ─────────┐
│    Chủ đề có điểm cao nhất → kết quả dự đoán            │
│    Tính xác suất tương đối & mức tin cậy (Cao/TB/Thấp)  │
└─────────────────────────────────────────────────────────┘
```

---

## 📖 CHI TIẾT CÁC KỸ THUẬT NLP

### 5.1. Text Normalization - Chuẩn hóa văn bản

**💡 Ý tưởng:**  
Trong NLP, cùng một từ có thể xuất hiện dưới nhiều dạng viết khác nhau: "Công Nghệ", "CÔNG NGHỆ", "công nghệ". Nếu không chuẩn hóa, hệ thống sẽ coi chúng là 3 từ khác nhau. Text Normalization đưa tất cả về cùng một dạng chuẩn.

**🔧 Cách áp dụng trong dự án:**
```python
def normalize_text(self, text: str) -> str:
    return text.lower().strip()
```
- `lower()`: Chuyển toàn bộ ký tự thành chữ thường
- `strip()`: Xóa khoảng trắng thừa ở đầu/cuối

**📌 Ví dụ:**  
`"  Công Nghệ THÔNG TIN  "` → `"công nghệ thông tin"`

---

### 5.2. Text Cleaning - Làm sạch văn bản

**💡 Ý tưởng:**  
Văn bản thực tế thường chứa nhiều "rác": dấu câu (. , ! ? :), ký tự đặc biệt (#, @, $), dấu gạch dưới, ... Những ký tự này không đóng góp vào việc phân loại chủ đề nên cần loại bỏ.

**🔧 Cách áp dụng trong dự án:**
```python
def clean_text(self, text: str) -> str:
    # Loại bỏ mọi ký tự KHÔNG phải chữ cái, số, khoảng trắng, hoặc dấu tiếng Việt
    text = re.sub(r"[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", " ", text)
    text = re.sub(r"_", " ", text)        # Thay dấu gạch dưới bằng khoảng trắng
    text = re.sub(r"\s+", " ", text)       # Gộp nhiều khoảng trắng thành một
    return text.strip()
```

**Điểm đặc biệt:** Regex được thiết kế riêng cho **tiếng Việt** – giữ lại tất cả các ký tự có dấu (ă, â, ơ, ư, đ, ...) thay vì chỉ giữ ASCII.

**📌 Ví dụ:**  
`"Lập trình Python (v3.12), @AI!"` → `"lập trình python v3 12 ai"`

---

### 5.3. Tokenization - Tách từ

**💡 Ý tưởng:**  
Tokenization là bước nền tảng trong NLP – chuyển một chuỗi văn bản thành danh sách các đơn vị ngôn ngữ nhỏ nhất (token). Máy tính không hiểu câu dạng chuỗi, nó cần danh sách các phần tử riêng biệt để xử lý.

**🔧 Cách áp dụng trong dự án:**
```python
def tokenize(self, text: str) -> List[str]:
    return [token for token in text.split() if token]
```

Sử dụng phương pháp **tách theo khoảng trắng** (whitespace tokenization). Đây là phương pháp đơn giản nhất, phù hợp khi không dùng thư viện NLP chuyên dụng.

**📌 Ví dụ:**  
`"lập trình python xây dựng api"` → `["lập", "trình", "python", "xây", "dựng", "api"]`

**⚠️ Lưu ý:** Tiếng Việt có từ ghép (ví dụ "học sinh" = 1 từ gồm 2 tiếng). Hệ thống bù trừ hạn chế này bằng cách sử dụng N-gram (mục 5.5).

---

### 5.4. Stopword Removal - Loại bỏ từ dừng

**💡 Ý tưởng:**  
Stopwords là những từ xuất hiện rất nhiều trong mọi văn bản nhưng không mang ý nghĩa phân loại (ví dụ: "là", "và", "của", "có", "trong", ...). Loại bỏ chúng giúp:
- Giảm kích thước vector
- Tăng trọng lượng cho các từ thật sự quan trọng
- Cải thiện chất lượng phân loại

**🔧 Cách áp dụng trong dự án:**
```python
STOPWORDS = {
    "là", "và", "của", "có", "trong", "một", "những", "các", "cho", "với",
    "được", "khi", "để", "thì", "mà", "này", "đó", "cũng", "rất", "nhiều",
    "về", "từ", "đang", "trên", "theo", "vào", "ra", "ở", "tại", "do", "vì",
    "nên", "đã", "sẽ", "cần", "hơn", "giúp", "việc", "mỗi", "như", "hay",
    "bị", "đến", "cùng", "qua", "lại", "thêm", "nhằm", "sau", "trước",
    "ít", "vẫn", "đều", "vừa", "mới", "rằng", "thật", "sự", "kia", "ấy",
    "nơi", "đây",
}  # Tổng cộng 62 từ dừng tiếng Việt

def remove_stopwords(self, tokens):
    return [token for token in tokens if token not in STOPWORDS]
```

**📌 Ví dụ:**  
`["bác", "sĩ", "khuyến", "cáo", "người", "dân", "khám", "bệnh", "định", "kỳ", "để", "phát", "hiện"]`  
→ (sau bỏ stopwords) → `["bác", "sĩ", "khuyến", "cáo", "người", "dân", "khám", "bệnh", "định", "kỳ", "phát", "hiện"]`

---

### 5.5. N-gram Extraction - Trích xuất cụm từ

**💡 Ý tưởng:**  
N-gram là chuỗi N từ liên tiếp nhau trong văn bản. Nhiều khái niệm quan trọng chỉ có ý nghĩa khi kết hợp nhiều từ:
- **"trí tuệ nhân tạo"** (3-gram) → thuộc Công nghệ (nhưng từng từ đơn lẻ "trí", "tuệ", "nhân", "tạo" thì không rõ ràng)
- **"bài giảng online"** (3-gram) → thuộc Giáo dục
- **"phác đồ điều trị"** (3-gram) → thuộc Sức khỏe
- **"huấn luyện viên"** (3-gram) → thuộc Thể thao

**🔧 Cách áp dụng trong dự án:**
```python
def extract_phrases(self, text: str) -> List[str]:
    cleaned_text = self.clean_text(self.normalize_text(text))
    tokens = self.tokenize(cleaned_text)
    phrases = []
    for size in (2, 3, 4):   # Tạo 2-gram, 3-gram, 4-gram
        for index in range(len(tokens) - size + 1):
            phrases.append(" ".join(tokens[index:index + size]))
    return phrases
```

Hệ thống trích xuất cụm **2 từ, 3 từ và 4 từ** liên tiếp từ văn bản để đối sánh với danh sách cụm từ đặc trưng (`strong_phrases`) đã định nghĩa sẵn cho mỗi chủ đề.

**📌 Ví dụ:** Câu `"trí tuệ nhân tạo rất mạnh"` tạo ra:
- 2-gram: `["trí tuệ", "tuệ nhân", "nhân tạo", "tạo rất", "rất mạnh"]`
- 3-gram: `["trí tuệ nhân", "tuệ nhân tạo", "nhân tạo rất", "tạo rất mạnh"]`
- 4-gram: `["trí tuệ nhân tạo", "tuệ nhân tạo rất", "nhân tạo rất mạnh"]`

→ Cụm `"trí tuệ nhân tạo"` (4-gram) khớp với `strong_phrases` của chủ đề Công nghệ → **+3.0 điểm**.

---

### 5.6. Bag of Words (BoW) - Túi từ

**💡 Ý tưởng:**  
Bag of Words là phương pháp biểu diễn văn bản kinh điển trong NLP. Ý tưởng: **bỏ qua thứ tự từ**, chỉ quan tâm **từ nào xuất hiện** và **bao nhiêu lần**. Mỗi văn bản được biểu diễn bằng một vector có chiều dài bằng kích thước từ điển, trong đó mỗi phần tử là số lần xuất hiện của từ tương ứng.

**🔧 Cách áp dụng trong dự án:**

**Bước 1 – Xây dựng từ điển chung** từ toàn bộ 40 văn bản mẫu:
```python
def build_vocabulary(self, dataset):
    vocabulary = []
    seen = set()
    for item in dataset:
        processed = self.preprocess_text(item.text)
        for token in processed.tokens:
            if token not in seen:
                seen.add(token)
                vocabulary.append(token)
    return vocabulary  # Ví dụ: ["phòng", "nâng", "cấp", "máy", "tính", ...]
```

**Bước 2 – Chuyển văn bản thành vector:**
```python
def text_to_vector(self, text_or_tokens, vocabulary):
    tokens = ...  # Tiền xử lý lấy danh sách từ
    token_counter = Counter(tokens)
    return [token_counter.get(word, 0) for word in vocabulary]
```

**Bước 3 – Xây dựng hồ sơ (profile) cho từng chủ đề:**
```python
def build_topic_profiles(self, dataset, vocabulary):
    # Gom tất cả từ của các văn bản cùng chủ đề lại
    # Tạo 1 vector tổng cho mỗi chủ đề
    grouped_tokens = defaultdict(list)
    for item in dataset:
        grouped_tokens[item.label].extend(self.preprocess_text(item.text).tokens)
    topic_profiles = {}
    for topic, tokens in grouped_tokens.items():
        topic_profiles[topic] = self.text_to_vector(tokens, vocabulary)
    return topic_profiles
```

**📌 Minh họa:**

| Từ | Công nghệ | Giáo dục | Sức khỏe | Thể thao |
|----|-----------|----------|-----------|----------|
| máy tính | 3 | 0 | 0 | 0 |
| phần mềm | 4 | 0 | 0 | 0 |
| học sinh | 0 | 5 | 0 | 0 |
| bác sĩ | 0 | 0 | 3 | 0 |
| cầu thủ | 0 | 0 | 0 | 4 |
| ... | ... | ... | ... | ... |

---

### 5.7. Cosine Similarity - Độ tương đồng Cosine

**💡 Ý tưởng:**  
Cosine Similarity đo **góc** giữa 2 vector trong không gian nhiều chiều. Nếu 2 vector chỉ về cùng một hướng (góc ≈ 0°), cosine ≈ 1 → rất giống nhau. Nếu vuông góc (góc = 90°), cosine = 0 → không liên quan.

**Công thức toán học:**

```
                    A · B              Σ(Ai × Bi)
cos(θ) = ──────────────── = ────────────────────────────
              ‖A‖ × ‖B‖     √(Σ Ai²) × √(Σ Bi²)
```

**Tại sao dùng Cosine thay vì khoảng cách Euclidean?**  
Vì Cosine Similarity không bị ảnh hưởng bởi **độ dài văn bản**. Một bài 10 từ và bài 100 từ cùng chủ đề vẫn cho cosine cao, trong khi Euclidean sẽ bị lệch do chênh lệch tần suất.

**🔧 Cách áp dụng trong dự án:**
```python
def cosine_similarity(self, vector1, vector2):
    dot_product = sum(left * right for left, right in zip(vector1, vector2))
    magnitude1 = math.sqrt(sum(value * value for value in vector1))
    magnitude2 = math.sqrt(sum(value * value for value in vector2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)
```

Hệ thống tính cosine giữa vector BoW của văn bản nhập vào và vector hồ sơ (profile) của **từng chủ đề**, thu được 4 giá trị cosine.

**📌 Ví dụ kết quả:**

| Chủ đề | Cosine Score |
|--------|-------------|
| Công nghệ | 0.3842 |
| Giáo dục | 0.0512 |
| Sức khỏe | 0.0210 |
| Thể thao | 0.0000 |

→ Văn bản gần nhất với hồ sơ "Công nghệ".

---

### 5.8. Weighted Keyword Matching - Đối sánh từ khóa có trọng số

**💡 Ý tưởng:**  
Cosine Similarity đo tổng thể, nhưng một số từ/cụm từ là **dấu hiệu cực mạnh** cho chủ đề cụ thể. Ví dụ: gặp "trí tuệ nhân tạo" gần như chắc chắn là Công nghệ, gặp "phác đồ điều trị" gần như chắc chắn là Sức khỏe. Hệ thống dùng **từ điển trọng số** để cộng thêm điểm khi phát hiện các từ khóa đặc trưng.

**🔧 Cách áp dụng trong dự án:**

Mỗi chủ đề có 2 loại từ điển:

**Keywords** (từ khóa đơn, trọng số 1.0–2.0):
```python
"Công nghệ": {
    "keywords": {
        "máy tính": 2.0, "phần mềm": 2.0, "lập trình": 2.0,
        "thuật toán": 2.0, "dữ liệu": 2.0, "ai": 2.0, ...
    }
}
```

**Strong Phrases** (cụm từ mạnh, trọng số 3.0):
```python
"Công nghệ": {
    "strong_phrases": {
        "trí tuệ nhân tạo": 3.0, "cơ sở dữ liệu": 3.0,
        "điện toán đám mây": 3.0, "bảo mật thông tin": 3.0, ...
    }
}
```

**Context Priority** – Bonus ngữ cảnh khi phát hiện **tổ hợp** từ khóa:
```python
# Nếu văn bản chứa cả "phần mềm" VÀ "hệ thống" → bonus +1.0 cho Công nghệ
# Nếu chứa "trí tuệ nhân tạo" → bonus +1.8 cho Công nghệ
```

Cách tính: duyệt từng chủ đề, kiểm tra từng từ khóa/cụm từ trong danh sách → cộng trọng số tương ứng nếu khớp.

---

### 5.9. Conflict Penalty - Phạt tín hiệu gây nhiễu

**💡 Ý tưởng:**  
Trong thực tế, một văn bản có thể chứa từ khóa của **nhiều chủ đề**. Ví dụ: *"Bác sĩ sử dụng phần mềm để quản lý bệnh nhân"* – chứa cả từ khóa Sức khỏe ("bác sĩ", "bệnh nhân") và Công nghệ ("phần mềm"). Conflict Penalty **trừ điểm** khi phát hiện tín hiệu gây nhiễu từ chủ đề khác, giúp hệ thống ưu tiên chủ đề có tín hiệu mạnh hơn.

**🔧 Cách áp dụng trong dự án:**
```python
def calculate_conflict_penalty(self, text, topic):
    # Với mỗi chủ đề "other" khác topic hiện tại:
    #   - Nếu phát hiện keyword của other mà KHÔNG trùng keyword của topic → phạt 0.5–0.75
    #   - Nếu phát hiện strong_phrase của other → phạt 1.0
    # Nếu topic hiện tại có tín hiệu mạnh (>= 3 matches) → giảm penalty xuống 60%
    # Nếu tín hiệu vừa (>= 1 match) → giảm penalty xuống 80%
```

**Cơ chế thông minh:** Penalty được **giảm nhẹ** khi chủ đề đang xét đã có đủ tín hiệu riêng → tránh trường hợp phạt quá nặng khi chủ đề chính rõ ràng nhưng có nhắc thoáng qua chủ đề khác.

---

### 5.10. Confidence Assessment - Đánh giá độ tin cậy

**💡 Ý tưởng:**  
Không chỉ đưa ra kết quả, hệ thống còn tự **đánh giá mức độ chắc chắn** của dự đoán bằng cách xem khoảng cách giữa điểm cao nhất và điểm cao thứ nhì.

**🔧 Cách áp dụng trong dự án:**
```python
def assess_confidence(self, sorted_scores):
    top_score = sorted_scores[0][1]       # Điểm cao nhất
    second_score = sorted_scores[1][1]    # Điểm cao nhì

    gap_ratio = |top - second| / max(|top|, 0.0001)

    if gap_ratio < 0.10:   return "Thấp"       # Hai chủ đề sát nút nhau
    if gap_ratio < 0.25:   return "Trung bình"  # Có khoảng cách nhưng chưa rõ ràng
    return "Cao"                                # Chủ đề chiến thắng rõ ràng
```

| Khoảng cách (gap_ratio) | Mức tin cậy | Ý nghĩa |
|--------------------------|-------------|---------|
| < 10% | **Thấp** | Văn bản đa chủ đề, kết quả chưa chắc chắn |
| 10% – 25% | **Trung bình** | Có xu hướng nhưng còn tín hiệu cạnh tranh |
| > 25% | **Cao** | Chủ đề rõ ràng, kết quả đáng tin cậy |

---

## 🧮 CÔNG THỨC TÍNH ĐIỂM TỔNG HỢP

Với mỗi chủ đề, hệ thống tính **điểm cuối cùng** bằng công thức:

```
Final_Score = Cosine_Similarity
            + Keyword_Score       (tổng trọng số từ khóa khớp)
            + Phrase_Score        (tổng trọng số cụm từ mạnh khớp)
            + Context_Bonus       (bonus khi gặp tổ hợp từ khóa đặc biệt)
            − Conflict_Penalty    (phạt tín hiệu nhiễu từ chủ đề khác)
```

Chủ đề nào có `Final_Score` **cao nhất** sẽ được chọn làm kết quả.

**Xác suất tương đối** được tính bằng cách dịch (shift) tất cả điểm về dương, sau đó chuẩn hóa về tổng = 100%:
```python
shifted = score - min_score + 0.001
percentage = (shifted / total_shifted) × 100%
```

---

## 📊 DỮ LIỆU MẪU

| Chủ đề | Số lượng văn bản | Ví dụ |
|--------|-----------------|-------|
| **Công nghệ** | 10 | *"Nhóm lập trình đang phát triển phần mềm quản lý kho bằng thuật toán tối ưu và cơ sở dữ liệu tập trung."* |
| **Giáo dục** | 10 | *"Giáo viên chuẩn bị bài giảng mới để học sinh dễ tiếp cận kiến thức trong môn khoa học tự nhiên."* |
| **Sức khỏe** | 10 | *"Bác sĩ khuyến cáo người dân khám bệnh định kỳ để phát hiện sớm triệu chứng của bệnh tim mạch."* |
| **Thể thao** | 10 | *"Huấn luyện viên điều chỉnh chiến thuật pressing để các cầu thủ kiểm soát thế trận tốt hơn."* |

**Tổng cộng:** 40 văn bản mẫu, mỗi chủ đề 10 văn bản, được gán nhãn thủ công.

---

## ▶️ CÁCH CHẠY CHƯƠNG TRÌNH

### Yêu cầu
- Python 3.8+
- Tkinter (thường có sẵn trong Python)
- (Tùy chọn) `python-docx` và `PyPDF2` để import file .docx/.pdf

### Cài đặt & Chạy
```bash
# Cài thư viện phụ trợ (tùy chọn, chỉ cần nếu import file docx/pdf)
pip install python-docx PyPDF2

# Chạy chương trình
python main.py
```

### Tính năng giao diện
1. **Nhập văn bản** trực tiếp vào ô text hoặc **import file** (.txt, .docx, .pdf)
2. Bấm **"Phân tích ngay"** → hệ thống trả về:
   - Chủ đề dự đoán + mức tin cậy
   - Bảng điểm chi tiết từng chủ đề (cosine, keyword, phrase, context, penalty)
   - Biểu đồ xác suất tương đối (bar chart)
   - Từ khóa & cụm từ đã phát hiện
   - Giải thích bằng ngôn ngữ tự nhiên
3. Xem **dữ liệu mẫu** và **ma trận Bag of Words**
4. Xem **lịch sử phân tích** (lưu tự động vào JSON)

---

## 📁 CẤU TRÚC THƯ MỤC

```
xử lý ngôn ngữ tự nhiên/
├── main.py                          # Entry point – khởi chạy ứng dụng
├── requirements.txt                 # Thư viện phụ thuộc
├── analysis_history.json            # Lịch sử phân tích (tự động tạo)
│
├── domain/                          # Tầng Domain – Entities & Config
│   ├── entities.py                  # Dataclass: TextSample, ProcessedText, TopicPrediction, ...
│   └── topic_config.py              # Cấu hình: 4 chủ đề, 62 stopwords, từ khóa + trọng số
│
├── application/                     # Tầng Application – Logic nghiệp vụ
│   ├── topic_analyzer.py            # ★ Class TopicAnalyzer – toàn bộ pipeline NLP
│   └── history_repository.py        # Interface Protocol cho lưu lịch sử
│
├── infrastructure/                  # Tầng Infrastructure – I/O
│   ├── document_reader.py           # Đọc file .txt / .docx / .pdf
│   └── json_history_repository.py   # Lưu/đọc lịch sử phân tích dạng JSON
│
├── data/                            # Tầng Data
│   └── sample_dataset.py            # 40 văn bản mẫu đã gán nhãn
│
├── presentation/                    # Tầng Presentation – Giao diện
│   └── tkinter_app.py               # GUI Tkinter: nhập liệu, hiển thị kết quả, biểu đồ
│
└── topic_analysis_core.py           # Wrapper tương thích ngược (compatibility layer)
```

---

## 🎯 TÓM TẮT ĐIỂM NỔI BẬT

| Điểm | Mô tả |
|------|-------|
| ✅ **Không dùng thư viện ML/NLP** | Toàn bộ thuật toán viết thủ công bằng Python thuần |
| ✅ **Kết hợp nhiều kỹ thuật** | BoW + Cosine + Keyword Matching + N-gram + Penalty |
| ✅ **Xử lý tiếng Việt** | Regex giữ dấu tiếng Việt, stopwords tiếng Việt |
| ✅ **Có giải thích kết quả** | Hệ thống sinh giải thích tự động bằng tiếng Việt |
| ✅ **Giao diện đầy đủ** | GUI Tkinter với biểu đồ, import file, lịch sử |
| ✅ **Clean Architecture** | Tách rõ 4 tầng: Domain, Application, Infrastructure, Presentation |
