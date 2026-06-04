# 📝 ĐÁNH GIÁ ĐỒ ÁN THEO RUBRIC CHẤM ĐIỂM

---

## 3.1. Phần 1: Kiến thức lập trình Python cơ bản — 2 điểm

| Tiêu chí                                                      | Điểm tối đa | Đánh giá | Điểm dự kiến | Minh chứng trong code                                                                                                                                                                                                                    |
| --------------------------------------------------------------- | :-------------: | :---------: | :--------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Khai báo hoặc nhập được dữ liệu đầu vào              |       0.5       |  ✅ Đạt  |  **0.5**  | `SAMPLE_DATA` khai báo 40 TextSample trong [sample_dataset.py](file:///Users/tuna/Downloads/xử lý ngôn ngữ tư nhiên/data/sample_dataset.py). Nhập dữ liệu từ người dùng qua ô text Tkinter + import file .txt/.docx/.pdf |
| Sử dụng được biến, kiểu dữ liệu, danh sách, chuỗi    |       0.5       |  ✅ Đạt  |  **0.5**  | Dùng `list` (vocabulary, tokens), `dict` (TOPIC_CONFIG, topic_profiles), `set` (STOPWORDS, seen), `str` (text processing), `Counter`, `defaultdict`, `dataclass` (TextSample, ProcessedText...)                            |
| Có sử dụng vòng lặp, điều kiện và hàm                 |       0.5       |  ✅ Đạt  |  **0.5**  | Vòng lặp `for` khắp nơi (build_vocabulary, extract_phrases...), điều kiện `if/elif` (assess_confidence, apply_context_priority), hàm/method (20+ method trong TopicAnalyzer)                                                  |
| Chương trình chạy được và có kết quả đúng cơ bản |       0.5       |  ✅ Đạt  |  **0.5**  | Chạy `python main.py` → mở GUI → nhập văn bản → ra kết quả phân loại đúng                                                                                                                                                 |

> **Tổng Phần 1: 2.0 / 2.0** ✅

---

## 3.2. Phần 2: Bài toán ứng dụng xử lý ngôn ngữ tự nhiên — 3 điểm

| Tiêu chí                                                                | Điểm tối đa | Đánh giá | Điểm dự kiến | Minh chứng trong code                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------- | :-------------: | :---------: | :--------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Có bộ dữ liệu mẫu phù hợp với bài toán                          |       0.5       |  ✅ Đạt  |  **0.5**  | 40 câu mẫu, 4 chủ đề × 10 câu/chủ đề, mỗi câu là một đoạn văn tiếng Việt tự nhiên đã gán nhãn → [sample_dataset.py](file:///Users/tuna/Downloads/xử lý ngôn ngữ tư nhiên/data/sample_dataset.py)                                                                                                   |
| Tiền xử lý được văn bản: chữ thường, xóa dấu câu, tách từ |       0.5       |  ✅ Đạt  |  **0.5**  | `normalize_text()` → chữ thường; `clean_text()` → xóa dấu câu bằng regex; `tokenize()` → tách từ; `remove_stopwords()` → bỏ 62 từ dừng → [topic_analyzer.py dòng 30–72](file:///Users/tuna/Downloads/xử lý ngôn ngữ tư nhiên/application/topic_analyzer.py#L30-L72)                               |
| Biểu diễn được văn bản dưới dạng có thể tính toán           |       0.5       |  ✅ Đạt  |  **0.5**  | Bag of Words:`build_vocabulary()` tạo từ điển, `text_to_vector()` chuyển text → vector tần suất, `build_topic_profiles()` tạo hồ sơ chủ đề → [topic_analyzer.py dòng 74–109](file:///Users/tuna/Downloads/xử lý ngôn ngữ tư nhiên/application/topic_analyzer.py#L74-L109)                             |
| Tính được điểm hoặc xác suất cho từng nhóm/lớp                |       0.5       |  ✅ Đạt  |  **0.5**  | Cosine Similarity + Keyword Score + Phrase Score cho 4 chủ đề, xác suất tương đối (%) bằng `calculate_relative_percentages()` → [topic_analyzer.py dòng 258–298](file:///Users/tuna/Downloads/xử lý ngôn ngữ tư nhiên/application/topic_analyzer.py#L258-L298)                                                |
| Dự đoán được kết quả phân loại phù hợp                        |       0.5       |  ✅ Đạt  |  **0.5**  | `predict_topic()` → sắp xếp điểm giảm dần → chọn chủ đề cao nhất → [topic_analyzer.py dòng 258–298](file:///Users/tuna/Downloads/xử lý ngôn ngữ tư nhiên/application/topic_analyzer.py#L258-L298)                                                                                                          |
| In kết quả rõ ràng, dễ kiểm tra                                     |       0.5       |  ✅ Đạt  |  **0.5**  | GUI hiển thị: chủ đề dự đoán, mức tin cậy, bảng điểm chi tiết từng chủ đề, biểu đồ bar chart xác suất, từ khóa/cụm từ phát hiện, giải thích bằng tiếng Việt → [tkinter_app.py dòng 280–308](file:///Users/tuna/Downloads/xử lý ngôn ngữ tư nhiên/presentation/tkinter_app.py#L280-L308) |

> **Tổng Phần 2: 3.0 / 3.0** ✅

---

## 3.3. Báo cáo và trả lời câu hỏi — 5 điểm

| Tiêu chí                                                        | Điểm tối đa |     Đánh giá     | Điểm dự kiến | Ghi chú                                                                                                                                                                                                      |
| ----------------------------------------------------------------- | :-------------: | :-----------------: | :---------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Báo cáo mô tả được bài toán, dữ liệu và cách xử lý |       1.0       |      ✅ Đạt      |   **1.0**   | README_NLP.md mô tả đầy đủ: bài toán (Text Classification), dữ liệu (40 mẫu × 4 chủ đề), cách xử lý (10 kỹ thuật NLP chi tiết), công thức chấm điểm, ví dụ minh họa xuyên suốt |
| Trả lời được các câu hỏi                                  |       4.0       | ⏳ Phụ thuộc bạn | **? / 4.0** | Phần này do bạn trả lời trực tiếp khi bảo vệ. Xem gợi ý bên dưới                                                                                                                                |

> **Tổng Phần 3: 1.0 + ? / 5.0**

---

## 📊 TỔNG KẾT ĐIỂM DỰ KIẾN

| Phần                          | Điểm tối đa |      Điểm dự kiến      |
| ------------------------------ | :-------------: | :------------------------: |
| Phần 1 – Python cơ bản     |       2.0       |      **2.0 ✅**      |
| Phần 2 – Bài toán NLP      |       3.0       |      **3.0 ✅**      |
| Phần 3 – Báo cáo           |       1.0       |      **1.0 ✅**      |
| Phần 3 – Trả lời câu hỏi |       4.0       | **Phụ thuộc bạn** |
| **TỔNG**                | **10.0** |  **6.0 + (0–4.0)**  |

> ### 🎯 Phần code + báo cáo: **6.0 / 6.0 — Đạt tối đa**
>
> Dự án đáp ứng **100% tiêu chí** về code và báo cáo. Phần còn lại (4 điểm) phụ thuộc vào việc bạn **trả lời câu hỏi** khi bảo vệ.

---

## 🗣 CÂU HỎI GV CÓ THỂ HỎI + GỢI Ý TRẢ LỜI

### ❓ "Cosine Similarity là gì? Tại sao dùng nó?"

> Cosine Similarity đo góc giữa 2 vector. Nếu 2 vector cùng hướng thì cosine = 1 (giống nhau), vuông góc thì = 0 (không liên quan). Em dùng nó vì Cosine không bị ảnh hưởng bởi độ dài văn bản — bài 10 từ và 100 từ cùng chủ đề vẫn cho cosine tương đương, trong khi Euclidean sẽ bị lệch.

### ❓ "Bag of Words hoạt động thế nào?"

> Em xây dựng từ điển chung từ 40 câu mẫu. Mỗi văn bản được chuyển thành vector, mỗi vị trí là số lần xuất hiện của từ tương ứng trong từ điển. Ví dụ: nếu từ điển có ["máy", "tính", "bác", "sĩ"] thì câu "máy tính máy tính" sẽ thành vector [2, 2, 0, 0]. Thứ tự từ bị bỏ qua, chỉ quan tâm tần suất.

### ❓ "Tại sao cần bỏ stopwords?"

> Stopwords là các từ xuất hiện ở mọi văn bản như "là", "và", "của", "có"... Chúng không giúp phân biệt chủ đề. Nếu giữ lại, vector sẽ bị "pha loãng" — các từ quan trọng bị giảm tỷ trọng, Cosine Similarity sẽ kém chính xác.

### ❓ "N-gram là gì? Dùng để làm gì?"

> N-gram là chuỗi N từ liên tiếp. Em dùng 2-gram, 3-gram, 4-gram để bắt các cụm từ có ý nghĩa mà từ đơn không thể diễn tả, ví dụ "trí tuệ nhân tạo" (4-gram) rõ ràng thuộc Công nghệ, nhưng từng từ "trí", "tuệ", "nhân", "tạo" thì không rõ. Cũng giúp bù trừ hạn chế của việc tách từ đơn giản khi tiếng Việt có nhiều từ ghép.

### ❓ "Conflict Penalty là gì? Tại sao cần?"

> Khi văn bản chứa từ khóa của nhiều chủ đề (ví dụ "Bác sĩ dùng phần mềm quản lý bệnh nhân" — vừa Sức khỏe vừa Công nghệ), nếu không xử lý thì cả 2 chủ đề đều được cộng điểm và dễ sai. Conflict Penalty trừ điểm khi phát hiện tín hiệu nhiễu từ chủ đề khác. Nếu chủ đề chính đã có nhiều tín hiệu riêng thì penalty được giảm nhẹ (chỉ 60%) để tránh phạt quá tay.

### ❓ "Công thức tính điểm cuối cùng?"

> `Final_Score = Cosine_Similarity + Keyword_Score + Phrase_Score + Context_Bonus − Conflict_Penalty`. Tính cho cả 4 chủ đề, chủ đề nào có điểm cao nhất thì là kết quả dự đoán.

### ❓ "Tại sao không dùng TF-IDF?"

> Em chỉ dùng BoW đơn giản vì đề yêu cầu không dùng thư viện có sẵn. Tuy nhiên em bù trừ bằng cách thêm weighted keywords và conflict penalty — thực chất đây là cách thủ công để làm điều tương tự TF-IDF: tăng trọng số từ quan trọng, giảm ảnh hưởng từ phổ biến.

### ❓ "Mức tin cậy tính như thế nào?"

> Em tính tỷ lệ khoảng cách giữa điểm cao nhất và điểm cao nhì. Nếu chênh < 10% → Thấp (2 chủ đề gần bằng nhau), 10–25% → Trung bình, > 25% → Cao. Điều này giúp người dùng biết kết quả có đáng tin hay không.

### ❓ "Chương trình có hạn chế gì?"

> - Tách từ bằng khoảng trắng nên chưa xử lý tốt từ ghép tiếng Việt (đã bù trừ bằng N-gram)
> - Bộ dữ liệu nhỏ (40 câu) nên khả năng tổng quát hóa có giới hạn
> - Chỉ phân loại 4 chủ đề, muốn thêm chủ đề mới cần bổ sung dữ liệu và từ khóa thủ công

---

## ✅ KIỂM TRA QUY ĐỊNH CHUNG

| Quy định                                                                                                          |                  Trạng thái                  |
| ------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------: |
| Không dùng thư viện NLP/ML (sklearn, nltk, underthesea, pyvi, gensim)                                           |  ✅ Đạt — chỉ dùng Python thuần + regex  |
| Chỉ dùng thành phần cơ bản Python (chuỗi, danh sách, từ điển, tập hợp, vòng lặp, hàm, điều kiện) |                    ✅ Đạt                    |
| Chương trình chạy được với bộ dữ liệu nhỏ tự chuẩn bị                                                | ✅ Đạt — 40 câu mẫu khai báo trực tiếp |
| File mã nguồn Python                                                                                              |                    ✅ Đạt                    |
| Báo cáo có mô tả bài toán, dữ liệu, các bước xử lý, kết quả                                         |           ✅ Đạt — README_NLP.md           |

> [!IMPORTANT]
> Báo cáo yêu cầu **< 10 trang, in 2 mặt, có trang bìa**. README_NLP.md hiện đủ nội dung nhưng bạn cần **chuyển sang file Word/PDF** và thêm trang bìa (tên đồ án, tên thành viên, lớp, GVHD) trước khi nộp.
>
