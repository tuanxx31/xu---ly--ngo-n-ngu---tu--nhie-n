# 🧠 Phân loại chủ đề bài viết tiếng Việt bằng kỹ thuật NLP

---

> ## 📣 BÁO CÁO NHANH
>
> Dự án của em xây dựng một **hệ thống phân loại chủ đề văn bản tiếng Việt**, giải quyết bài toán **Text Classification** — nhận vào một đoạn văn bản bất kỳ và tự động xác định nó thuộc chủ đề nào trong 4 chủ đề: **Công nghệ, Giáo dục, Sức khỏe, Thể thao**.
>
> Toàn bộ thuật toán được **viết thủ công bằng Python thuần**, không sử dụng bất kỳ thư viện Machine Learning hay NLP có sẵn nào (không scikit-learn, không NLTK, không spaCy).
>
> **Quy trình xử lý** gồm 3 giai đoạn chính:
>
> - **Tiền xử lý:** Chuẩn hóa chữ thường → Làm sạch ký tự đặc biệt (regex hỗ trợ dấu tiếng Việt) → Tách từ theo khoảng trắng → Loại bỏ 62 từ dừng tiếng Việt → Trích xuất cụm N-gram (2, 3, 4 từ) để bắt các từ ghép như "trí tuệ nhân tạo", "phác đồ điều trị".
> - **Biểu diễn & so sánh:** Dùng **Bag of Words** chuyển văn bản thành vector tần suất từ, rồi tính **Cosine Similarity** giữa vector đó với hồ sơ (profile) của 4 chủ đề đã xây từ 40 câu mẫu.
> - **Chấm điểm tổng hợp:** Kết hợp Cosine Similarity + điểm từ khóa có trọng số + điểm cụm từ đặc trưng + bonus ngữ cảnh − phạt tín hiệu nhiễu (Conflict Penalty). Chủ đề có tổng điểm cao nhất là kết quả dự đoán. Hệ thống còn tự đánh giá **mức độ tin cậy** (Cao / Trung bình / Thấp) dựa trên khoảng cách điểm giữa chủ đề nhất và nhì, đồng thời sinh **giải thích** tự động bằng tiếng Việt.
>
> **Công thức:** `Final_Score = Cosine + Keyword + Phrase + Context − Penalty`

---

## 1. Giới thiệu dự án

Hệ thống nhận vào một đoạn văn bản tiếng Việt bất kỳ, sau đó **tự động xác định chủ đề** của đoạn văn đó thuộc 1 trong 4 nhóm:

| Chủ đề               | Ví dụ văn bản                                                                                    |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| 🖥**Công nghệ** | *"Lập trình viên sử dụng Python để xây dựng API kết nối cơ sở dữ liệu."*            |
| 📚**Giáo dục**  | *"Giáo viên chuẩn bị bài giảng mới để học sinh tiếp cận kiến thức."*                 |
| 🏥**Sức khỏe**  | *"Bác sĩ khuyến cáo người dân khám bệnh định kỳ để phát hiện sớm triệu chứng."* |
| ⚽**Thể thao**   | *"Huấn luyện viên điều chỉnh chiến thuật để cầu thủ kiểm soát thế trận."*          |

**Điểm đặc biệt:** Toàn bộ thuật toán được viết thủ công bằng Python thuần — **không dùng bất kỳ thư viện Machine Learning hay NLP có sẵn** nào (không scikit-learn, không NLTK, không spaCy).

---

## 2. Bài toán đang giải quyết

|                                  |                                                          |
| -------------------------------- | -------------------------------------------------------- |
| **Tên bài toán**        | Phân loại văn bản (Text Classification)              |
| **Đầu vào**             | Một đoạn văn bản tiếng Việt (≥ 5 từ)            |
| **Đầu ra**               | Chủ đề phù hợp nhất + mức tin cậy + giải thích |
| **Số lớp**               | 4 (Công nghệ, Giáo dục, Sức khỏe, Thể thao)       |
| **Dữ liệu huấn luyện** | 40 câu mẫu đã gán nhãn (10 câu/chủ đề)         |

---

## 3. Tổng quan quy trình xử lý

```
  Văn bản người dùng nhập vào
              │
              ▼
  ┌───────────────────────────┐
  │   TIỀN XỬ LÝ VĂN BẢN    │  Chuẩn hóa → Làm sạch → Tách từ → Bỏ stopwords → Tạo N-gram
  └─────────────┬─────────────┘
                ▼
  ┌───────────────────────────┐
  │   BIỂU DIỄN VĂN BẢN     │  Bag of Words: chuyển text thành vector số
  └─────────────┬─────────────┘
                ▼
  ┌───────────────────────────┐
  │   CHẤM ĐIỂM TỪNG CHỦ ĐỀ │  Cosine Similarity + Keyword Score + Phrase Score + Context − Penalty
  └─────────────┬─────────────┘
                ▼
  ┌───────────────────────────┐
  │   KẾT QUẢ DỰ ĐOÁN       │  Chủ đề điểm cao nhất → kết quả + xác suất + giải thích
  └───────────────────────────┘
```

---

## 4. Chi tiết các kỹ thuật NLP sử dụng

---

### 4.1. Chuẩn hóa văn bản (Text Normalization)

**Ý tưởng:** Cùng một từ có thể viết nhiều kiểu khác nhau — "Công Nghệ", "CÔNG NGHỆ", "công nghệ". Nếu không chuẩn hóa, máy sẽ coi đây là 3 từ khác nhau. Bước này đưa tất cả về **một dạng thống nhất** bằng cách chuyển toàn bộ thành chữ thường.

**Cách hoạt động:**

```
"  Trí Tuệ NHÂN TẠO  "  →  "trí tuệ nhân tạo"
```

- Chuyển hoa → thường (`lower`)
- Xóa khoảng trắng thừa đầu/cuối (`strip`)

**Tại sao cần thiết?** Nếu bỏ qua bước này, từ "Bác Sĩ" trong dữ liệu mẫu sẽ không khớp với "bác sĩ" trong văn bản người dùng nhập → hệ thống mất khả năng nhận diện.

---

### 4.2. Làm sạch văn bản (Text Cleaning)

**Ý tưởng:** Văn bản thật luôn chứa "rác" — dấu câu (. , ! ?), ký tự đặc biệt (@, #, $), dấu gạch dưới, khoảng trắng nhiều lần. Những thứ này không giúp phân loại chủ đề nên cần loại bỏ, chỉ **giữ lại chữ cái và dấu tiếng Việt**.

**Cách hoạt động:**

```
"Lập trình Python (v3.12), @AI!"  →  "lập trình python v3 12 ai"
```

- Dùng regex loại bỏ mọi ký tự không phải chữ/số/khoảng trắng
- Regex được thiết kế **riêng cho tiếng Việt**: giữ lại toàn bộ nguyên âm có dấu (à, á, ạ, ả, ã, â, ă, ơ, ư, đ, ...)
- Gộp nhiều khoảng trắng liên tiếp thành 1

**Tại sao cần thiết?** Nếu không làm sạch, dấu câu sẽ "dính" vào từ (ví dụ `"bệnh."` ≠ `"bệnh"`) khiến đối sánh từ khóa thất bại.

---

### 4.3. Tách từ (Tokenization)

**Ý tưởng:** Máy tính không hiểu chuỗi văn bản dạng câu. Để xử lý, ta cần **tách câu thành danh sách các đơn vị nhỏ nhất** gọi là token. Đây là bước nền tảng — tất cả các kỹ thuật phía sau đều làm việc trên danh sách token, không phải trên chuỗi gốc.

**Cách hoạt động:**

```
"lập trình python xây dựng api"  →  ["lập", "trình", "python", "xây", "dựng", "api"]
```

Hệ thống dùng phương pháp **tách theo khoảng trắng** (whitespace tokenization) — đơn giản nhất, không phụ thuộc thư viện bên ngoài.

**Hạn chế và cách bù trừ:** Tiếng Việt có nhiều **từ ghép** — "học sinh" là 1 từ nhưng bị tách thành 2 token ("học", "sinh"). Hệ thống bù trừ bằng kỹ thuật **N-gram** (mục 4.5) — tự động tạo cụm 2–4 từ liên tiếp để "ghép lại" các từ ghép.

---

### 4.4. Loại bỏ từ dừng (Stopword Removal)

**Ý tưởng:** Trong bất kỳ ngôn ngữ nào, có một nhóm từ xuất hiện **rất nhiều ở mọi văn bản** mà không mang ý nghĩa phân loại: "là", "và", "của", "có", "trong", "một", "những"... Đây gọi là **stopwords** (từ dừng). Giữ chúng lại chỉ tạo nhiễu — chúng xuất hiện đều ở cả 4 chủ đề nên không giúp phân biệt được gì.

**Cách hoạt động:**

```
["bác", "sĩ", "khuyến", "cáo", "người", "dân", "khám", "bệnh", "để", "phát", "hiện"]
                                                                    ↑
                                                             stopword "để" bị loại
→  ["bác", "sĩ", "khuyến", "cáo", "người", "dân", "khám", "bệnh", "phát", "hiện"]
```

Hệ thống sử dụng **62 từ dừng tiếng Việt** được chọn thủ công, bao gồm các từ chức năng phổ biến nhất.

**Tại sao cần thiết?**

- Giảm kích thước vector biểu diễn → tính toán nhanh hơn
- Tăng tỷ trọng cho các từ **thật sự quan trọng** (bác sĩ, lập trình, cầu thủ...)
- Cải thiện chất lượng Cosine Similarity vì vector không bị "pha loãng" bởi từ vô nghĩa

---

### 4.5. Trích xuất N-gram (N-gram Extraction)

**Ý tưởng:** Nhiều khái niệm quan trọng chỉ có ý nghĩa khi đọc **nhiều từ liên tiếp**. Từ đơn lẻ "trí", "tuệ", "nhân", "tạo" không cho biết chủ đề gì, nhưng ghép lại thành **"trí tuệ nhân tạo"** thì chắc chắn thuộc Công nghệ. N-gram bắt được những tín hiệu ngữ nghĩa mạnh mà tokenization đơn thuần bỏ lỡ.

**N-gram là gì?** Là chuỗi N từ liên tiếp nhau trong văn bản:

- **2-gram (bigram):** "bác sĩ", "bài giảng", "trận đấu"
- **3-gram (trigram):** "trí tuệ nhân", "bài giảng online", "phác đồ điều"
- **4-gram:** "trí tuệ nhân tạo", "bảo mật thông tin"

**Cách hoạt động:**

Từ câu `"trí tuệ nhân tạo rất mạnh"`, hệ thống tạo ra:

| Loại  | Các N-gram                                                                |
| ------ | -------------------------------------------------------------------------- |
| 2-gram | "trí tuệ", "tuệ nhân", "nhân tạo", "tạo rất", "rất mạnh"         |
| 3-gram | "trí tuệ nhân", "tuệ nhân tạo", "nhân tạo rất", "tạo rất mạnh" |
| 4-gram | "trí tuệ nhân tạo", "tuệ nhân tạo rất", "nhân tạo rất mạnh"    |

Các N-gram này được đối sánh với danh sách **cụm từ đặc trưng** (strong phrases) đã định nghĩa cho mỗi chủ đề. Nếu khớp → cộng điểm mạnh (trọng số 3.0).

**Ví dụ cụm từ đặc trưng từng chủ đề:**

| Chủ đề   | Cụm từ mạnh                                                                  |
| ----------- | ------------------------------------------------------------------------------- |
| Công nghệ | trí tuệ nhân tạo, cơ sở dữ liệu, điện toán đám mây, an ninh mạng |
| Giáo dục  | học trực tuyến, bài giảng online, phương pháp giảng dạy               |
| Sức khỏe  | phác đồ điều trị, bác sĩ chuyên khoa, khám bệnh định kỳ           |
| Thể thao   | đội hình thi đấu, chiến thuật pressing, sân vận động                 |

---

### 4.6. Bag of Words (BoW) — Biểu diễn văn bản bằng vector

**Ý tưởng:** Máy tính không hiểu chữ, chỉ hiểu số. **Bag of Words** chuyển văn bản thành một **vector số** bằng cách: xây dựng một từ điển chung, rồi với mỗi văn bản, đếm **số lần xuất hiện** của từng từ trong từ điển. Thứ tự từ bị bỏ qua — chỉ quan tâm "từ nào có" và "bao nhiêu lần".

**Cách hoạt động — 3 bước:**

**Bước 1:** Gom tất cả từ (đã bỏ stopwords) từ 40 văn bản mẫu → tạo **từ điển chung** (vocabulary).

```
Từ điển: ["phòng", "nâng", "cấp", "máy", "tính", "phần", "mềm", "lập", "trình", ...]
```

**Bước 2:** Với mỗi văn bản, tạo vector có chiều = số từ trong từ điển. Mỗi vị trí = số lần từ đó xuất hiện.

```
Văn bản: "lập trình phần mềm lập trình"
                                        máy  tính  phần  mềm  lập  trình  ...
Vector:                             [    0,    0,    1,    1,    2,    2,  ...]
```

**Bước 3:** Gom vector của tất cả văn bản cùng chủ đề → tạo **hồ sơ chủ đề** (topic profile) — đại diện cho "khuôn mặt" của chủ đề đó trong không gian từ.

**Minh họa dạng bảng (rút gọn):**

| Từ         | Công nghệ | Giáo dục | Sức khỏe | Thể thao |
| ----------- | :---------: | :--------: | :--------: | :-------: |
| máy tính  |      3      |     0     |     0     |     0     |
| phần mềm  |      4      |     0     |     0     |     0     |
| lập trình |      3      |     0     |     0     |     0     |
| học sinh   |      0      |     5     |     0     |     0     |
| bài giảng |      0      |     4     |     0     |     0     |
| bác sĩ    |      0      |     0     |     3     |     0     |
| bệnh viện |      0      |     0     |     2     |     0     |
| cầu thủ   |      0      |     0     |     0     |     4     |
| trận đấu |      0      |     0     |     0     |     3     |

Nhìn vào bảng thấy rõ: mỗi chủ đề có "vùng" từ riêng. Khi văn bản mới xuất hiện, hệ thống sẽ xem nó giống "vùng" nào nhất.

---

### 4.7. Cosine Similarity — Đo độ tương đồng giữa văn bản và chủ đề

**Ý tưởng:** Sau khi có vector BoW của văn bản đầu vào và vector hồ sơ của 4 chủ đề, ta cần đo **mức độ giống nhau** giữa chúng. Cosine Similarity đo **góc** giữa 2 vector:

- Góc nhỏ (cùng hướng) → cosine ≈ 1 → **rất giống**
- Vuông góc → cosine = 0 → **không liên quan**

**Công thức:**

```
                      A · B                  Σ (Aᵢ × Bᵢ)
cos(θ)  =  ─────────────────  =  ─────────────────────────────
               ‖A‖ × ‖B‖        √(Σ Aᵢ²)  ×  √(Σ Bᵢ²)
```

Trong đó:

- `A · B` = tích vô hướng (nhân từng phần tử tương ứng rồi cộng lại)
- `‖A‖` = độ dài vector A (căn bậc 2 của tổng bình phương)

**Tại sao dùng Cosine mà không dùng Euclidean (khoảng cách thông thường)?**

Cosine **không bị ảnh hưởng bởi độ dài văn bản**. Ví dụ: bài 10 từ về Công nghệ và bài 100 từ về Công nghệ sẽ cho cosine tương tự nhau (vì cùng hướng), nhưng khoảng cách Euclidean sẽ rất xa (vì tần suất chênh lệch lớn).

**Ví dụ kết quả:**

```
Văn bản: "Nhóm lập trình phát triển phần mềm bằng thuật toán tối ưu"

Cosine với Công nghệ : 0.3842  ← cao nhất → gần nhất
Cosine với Giáo dục  : 0.0512
Cosine với Sức khỏe  : 0.0210
Cosine với Thể thao  : 0.0000
```

---

### 4.8. Chấm điểm từ khóa có trọng số (Weighted Keyword Scoring)

**Ý tưởng:** Cosine Similarity đo tổng thể dựa trên tần suất từ, nhưng có những từ/cụm từ là **dấu hiệu cực mạnh** cho 1 chủ đề cụ thể. Gặp "phác đồ điều trị" thì gần như chắc chắn là Sức khỏe. Gặp "sân vận động" thì gần như chắc chắn là Thể thao. Hệ thống bổ sung thêm điểm dựa trên **danh sách từ khóa có trọng số** đã thiết kế riêng cho từng chủ đề.

**Cách hoạt động:**

Mỗi chủ đề có 2 loại danh sách:

**① Từ khóa (keywords)** — trọng số 1.0 đến 2.0:

```
Công nghệ: máy tính (2.0), phần mềm (2.0), internet (1.0), dữ liệu (2.0), ...
Sức khỏe:  bác sĩ (2.0), thuốc (2.0), điều trị (2.0), dinh dưỡng (2.0), ...
```

**② Cụm từ mạnh (strong phrases)** — trọng số 3.0:

```
Công nghệ: "trí tuệ nhân tạo" (3.0), "cơ sở dữ liệu" (3.0), ...
Thể thao:  "huấn luyện viên" (3.0), "đội hình thi đấu" (3.0), ...
```

Khi phân tích, hệ thống duyệt qua văn bản → nếu tìm thấy từ khóa/cụm từ nào → **cộng trọng số tương ứng** vào điểm.

**③ Context Bonus (điểm cộng ngữ cảnh):**

Khi phát hiện **tổ hợp từ khóa đặc biệt** cùng xuất hiện, hệ thống cộng thêm bonus:

| Chủ đề   | Điều kiện                                           | Bonus |
| ----------- | ------------------------------------------------------ | ----- |
| Công nghệ | Chứa "trí tuệ nhân tạo" hoặc "cơ sở dữ liệu" | +1.8  |
| Công nghệ | Chứa cả "phần mềm" VÀ "hệ thống"                | +1.0  |
| Giáo dục  | Chứa "học trực tuyến" hoặc "bài giảng online"   | +1.8  |
| Sức khỏe  | Chứa cả "bác sĩ" VÀ "bệnh viện"                 | +1.0  |
| Thể thao   | Chứa "trận đấu" hoặc "ghi bàn"                   | +1.8  |

---

### 4.9. Phạt tín hiệu nhiễu (Conflict Penalty)

**Ý tưởng:** Một văn bản thực tế có thể chứa từ khóa của **nhiều chủ đề** cùng lúc. Ví dụ:

> *"Bác sĩ sử dụng **phần mềm** để quản lý **bệnh nhân**"*
>
> - "bác sĩ", "bệnh nhân" → Sức khỏe
> - "phần mềm" → Công nghệ

Nếu không xử lý, cả 2 chủ đề đều được cộng điểm và kết quả có thể bị sai. **Conflict Penalty** giải quyết bằng cách: khi chấm điểm cho chủ đề A, nếu phát hiện văn bản chứa từ khóa đặc trưng của chủ đề B, C, D → **trừ điểm** (penalty).

**Cách hoạt động:**

```
Đang chấm điểm cho "Sức khỏe":
  → Tìm thấy "phần mềm" thuộc Công nghệ mà KHÔNG thuộc Sức khỏe
  → Phạt: -0.5 điểm (hoặc -0.75 nếu trọng số ≥ 2.0)
  → Tìm thấy "cơ sở dữ liệu" (cụm từ mạnh) thuộc Công nghệ
  → Phạt: -1.0 điểm
```

**Cơ chế thông minh — giảm nhẹ penalty:**

- Nếu chủ đề đang xét có **≥ 3 tín hiệu riêng** → penalty chỉ tính 60% (vì chủ đề chính đã rõ, không sợ nhiễu)
- Nếu có **≥ 1 tín hiệu** → penalty tính 80%
- Nếu không có tín hiệu riêng → penalty tính nguyên 100%

Điều này tránh trường hợp phạt quá nặng khi chủ đề chính rõ ràng nhưng có nhắc thoáng qua chủ đề khác.

---

### 4.10. Đánh giá độ tin cậy (Confidence Assessment)

**Ý tưởng:** Hệ thống không chỉ trả lời "chủ đề là gì" mà còn tự đánh giá **"kết quả có đáng tin không"** bằng cách xem **khoảng cách** giữa điểm của chủ đề cao nhất và chủ đề cao thứ nhì. Nếu 2 chủ đề điểm sát nhau → kết quả không chắc chắn.

**Cách hoạt động:**

```
gap_ratio = |điểm_cao_nhất − điểm_cao_nhì| / |điểm_cao_nhất|
```

| Khoảng cách |      Mức tin cậy      | Ý nghĩa                                                                  |
| ------------- | :---------------------: | -------------------------------------------------------------------------- |
| < 10%         |    🔴**Thấp**    | Hai chủ đề điểm gần bằng nhau — văn bản mang tính đa chủ đề |
| 10% – 25%    | 🟡**Trung bình** | Có xu hướng rõ nhưng vẫn còn tín hiệu cạnh tranh                 |
| > 25%         |     🟢**Cao**     | Chủ đề chiến thắng vượt trội — kết quả đáng tin               |

**Ví dụ:**

```
Công nghệ: 8.50 điểm  ← cao nhất
Giáo dục : 1.20 điểm  ← cao nhì

gap = |8.50 − 1.20| / 8.50 = 85.9%  →  Mức tin cậy: 🟢 Cao
```

---

## 5. Công thức tính điểm tổng hợp

Toàn bộ hệ thống chấm điểm cho **mỗi chủ đề** được gói trong 1 công thức:

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  Final_Score  =  Cosine_Similarity                                   │
│               +  Keyword_Score        (tổng trọng số từ khóa khớp)   │
│               +  Phrase_Score         (tổng trọng số cụm từ khớp)    │
│               +  Context_Bonus        (bonus tổ hợp từ đặc biệt)    │
│               −  Conflict_Penalty     (phạt tín hiệu từ chủ đề khác)│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

→ Tính cho tất cả 4 chủ đề → Chủ đề nào **Final_Score cao nhất** → kết quả dự đoán.

**Xác suất tương đối:** Điểm 4 chủ đề được dịch (shift) về dương rồi chuẩn hóa về tổng = 100% để hiển thị dạng biểu đồ phần trăm.

---

## 6. Ví dụ minh họa toàn bộ quy trình

### Đầu vào

> *"Lập trình viên sử dụng Python để xây dựng API kết nối cơ sở dữ liệu với nền tảng thương mại điện tử."*

### Bước 1–4: Tiền xử lý

| Giai đoạn   | Kết quả                                                                                                                                                                                             |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chuẩn hóa   | `"lập trình viên sử dụng python để xây dựng api kết nối cơ sở dữ liệu với nền tảng thương mại điện tử"`                                                                     |
| Làm sạch    | `"lập trình viên sử dụng python để xây dựng api kết nối cơ sở dữ liệu với nền tảng thương mại điện tử"`                                                                     |
| Tách từ     | `["lập", "trình", "viên", "sử", "dụng", "python", "để", "xây", "dựng", "api", "kết", "nối", "cơ", "sở", "dữ", "liệu", "với", "nền", "tảng", "thương", "mại", "điện", "tử"]` |
| Bỏ stopwords | `["lập", "trình", "viên", "sử", "dụng", "python", "xây", "dựng", "api", "kết", "nối", "cơ", "sở", "dữ", "liệu", "nền", "tảng", "thương", "mại", "điện", "tử"]`                 |

### Bước 5: Trích N-gram

Một số N-gram quan trọng được tạo ra:

- `"cơ sở"`, `"sở dữ"`, `"dữ liệu"` (2-gram)
- `"cơ sở dữ"`, `"sở dữ liệu"` (3-gram)
- `"cơ sở dữ liệu"` (4-gram) → **khớp strong_phrases Công nghệ!**

### Bước 6–7: Chấm điểm

| Thành phần          |   Công nghệ   |   Giáo dục   |   Sức khỏe   |   Thể thao   |
| --------------------- | :-------------: | :------------: | :------------: | :------------: |
| Cosine Similarity     |      0.38      |      0.05      |      0.02      |      0.00      |
| Keyword Score         |      +8.0      |      0.0      |      0.0      |      0.0      |
| Phrase Score          |      +6.0      |      0.0      |      0.0      |      0.0      |
| Context Bonus         |      +1.8      |      0.0      |      0.0      |      0.0      |
| Conflict Penalty      |      −0.0      |     −0.0     |     −0.0     |     −0.0     |
| **Final Score** | **16.18** | **0.05** | **0.02** | **0.00** |

### Kết quả

```
Chủ đề dự đoán : Công nghệ
Mức tin cậy    : 🟢 Cao
Từ khóa phát hiện : lập trình, python, api, dữ liệu, cơ sở dữ liệu, ...
Cụm từ đặc trưng  : cơ sở dữ liệu
```

---

## 7. Tóm tắt

| Kỹ thuật NLP        | Vai trò                             | Kết quả đầu ra                                   |
| --------------------- | ------------------------------------ | ---------------------------------------------------- |
| Text Normalization    | Chuẩn hóa đầu vào               | Văn bản chữ thường, không thừa khoảng trắng |
| Text Cleaning         | Loại bỏ ký tự rác               | Chỉ còn chữ cái + dấu tiếng Việt              |
| Tokenization          | Tách câu thành từ                | Danh sách token                                     |
| Stopword Removal      | Bỏ từ vô nghĩa                   | Danh sách token sạch                               |
| N-gram Extraction     | Bắt cụm từ đặc trưng           | Cụm 2, 3, 4 từ liên tiếp                         |
| Bag of Words          | Biểu diễn text → vector           | Vector tần suất từ                                |
| Cosine Similarity     | Đo giống/khác giữa vector        | Điểm tương đồng 0–1                           |
| Keyword Scoring       | Cộng điểm từ khóa đặc thù    | Keyword score + Phrase score                         |
| Conflict Penalty      | Phạt tín hiệu nhiễu              | Trừ điểm khi nhầm lẫn chủ đề                 |
| Confidence Assessment | Đánh giá chất lượng dự đoán | Mức Cao / Trung bình / Thấp                       |

**Tất cả kỹ thuật kết hợp** thành 1 pipeline hoàn chỉnh: từ đoạn văn bản thô → tiền xử lý → biểu diễn số → chấm điểm → dự đoán chủ đề + giải thích.
