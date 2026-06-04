# Hệ thống gợi ý chủ đề bài viết ngắn

Dự án này là một ứng dụng Python có giao diện Tkinter dùng để phân tích và gợi ý chủ đề cho một đoạn văn bản tiếng Việt ngắn.

Ứng dụng hỗ trợ 4 chủ đề:

- Công nghệ
- Giáo dục
- Sức khỏe
- Thể thao

Người dùng nhập nội dung bài viết, hệ thống sẽ xử lý văn bản, chấm điểm từng chủ đề và đưa ra chủ đề phù hợp nhất kèm mức độ tin cậy.

## Dự án dùng để làm gì?

Dự án minh họa cách xây dựng một hệ thống xử lý ngôn ngữ tự nhiên cơ bản bằng Python, không dùng thư viện bên ngoài. Các chức năng chính gồm:

- Chuẩn hóa văn bản tiếng Việt.
- Làm sạch dấu câu và ký tự không cần thiết.
- Tách từ cơ bản theo khoảng trắng.
- Loại bỏ stopwords tiếng Việt.
- Biểu diễn văn bản bằng Bag of Words.
- Tính độ tương đồng Cosine Similarity giữa văn bản nhập và từng nhóm chủ đề.
- Tăng điểm cho từ khóa và cụm từ đặc trưng.
- Giảm điểm khi phát hiện tín hiệu gây nhầm lẫn giữa nhiều chủ đề.
- Hiển thị giải thích vì sao hệ thống chọn chủ đề đó.
- Lưu lịch sử phân tích vào file JSON.

## Kiến trúc dự án

Dự án đã được tổ chức lại theo Clean Architecture ở mức vừa phải để dễ báo cáo và dễ chia nhiệm vụ. Ý tưởng chính là tách giao diện, xử lý nghiệp vụ, dữ liệu và lưu trữ thành các phần riêng.

```text
.
├── domain/
│   ├── entities.py                  # Các entity/dataclass dùng chung
│   └── topic_config.py              # Chủ đề, stopwords, từ khóa, trọng số
├── application/
│   ├── topic_analyzer.py            # Use case phân tích và dự đoán chủ đề
│   └── history_repository.py        # Interface/cổng lưu lịch sử
├── infrastructure/
│   ├── json_history_repository.py   # Lưu và đọc lịch sử bằng file JSON
│   └── document_reader.py           # Đọc file .txt, .docx, .pdf để import văn bản
├── data/
│   └── sample_dataset.py            # Bộ dữ liệu mẫu
├── presentation/
│   └── tkinter_app.py               # Giao diện Tkinter
├── main.py                          # File chạy chính, lắp các thành phần lại với nhau
├── topic_suggestion_app.py          # Wrapper tương thích, gọi lại main.py
├── topic_analysis_core.py           # Wrapper tương thích với cách import cũ
├── topic_suggestion_ui.py           # Wrapper tương thích với cách import cũ
├── requirements.txt
├── analysis_history.json
└── README.md
```

### Trách nhiệm từng tầng

- `domain`: chứa các đối tượng và quy tắc ổn định nhất của bài toán như `TextSample`, `ProcessedText`, `TopicPrediction`, danh sách chủ đề, stopwords và trọng số từ khóa.
- `application`: chứa logic xử lý chính. `TopicAnalyzer` nhận văn bản, tiền xử lý, chấm điểm và trả về kết quả phân tích.
- `infrastructure`: chứa chi tiết kỹ thuật bên ngoài nghiệp vụ. Hiện tại là đọc/ghi lịch sử bằng JSON và đọc nội dung file `.txt`, `.docx`, `.pdf`.
- `data`: chứa bộ dữ liệu mẫu dùng để tạo từ điển và hồ sơ chủ đề.
- `presentation`: chứa giao diện Tkinter, chỉ gọi use case và repository, không tự xử lý thuật toán.

Luồng phụ thuộc chính:

```text
presentation -> application -> domain
infrastructure -> application/domain
data -> domain
main.py -> lắp tất cả thành app chạy được
```

## Gợi ý phân chia nhiệm vụ nhóm

- Thành viên 1: phụ trách `domain/topic_config.py` và `data/sample_dataset.py`, bổ sung dữ liệu mẫu, stopwords, từ khóa và trọng số.
- Thành viên 2: phụ trách `application/topic_analyzer.py`, giải thích thuật toán Bag of Words, Cosine Similarity, Keyword Weighting, Phrase Matching, Context Bonus và Conflict Penalty.
- Thành viên 3: phụ trách `presentation/tkinter_app.py`, trình bày giao diện, nhập văn bản, hiển thị kết quả, xem dữ liệu mẫu và lịch sử.
- Thành viên 4: phụ trách `infrastructure/json_history_repository.py` và `infrastructure/document_reader.py`, giải thích cách lưu lịch sử vào `analysis_history.json` và cách import file văn bản.
- Khi báo cáo tổng thể, dùng `main.py` để giải thích cách các phần được khởi tạo và kết nối với nhau.

## Cách chạy dự án

Yêu cầu:

- Python 3.x
- Tkinter có sẵn trong bản Python cài đặt trên máy
- `python-docx` và `PyPDF2` nếu muốn dùng chức năng import Word/PDF

Các thư viện trong `requirements.txt` chỉ dùng để đọc tài liệu, không phải thư viện NLP/ML.

Cài thư viện hỗ trợ import file:

```bash
pip install -r requirements.txt
```

Chạy ứng dụng bằng lệnh:

```bash
python3 main.py
```

Sau khi chạy, cửa sổ ứng dụng sẽ mở ra. Nhập một đoạn văn bản tiếng Việt ngắn rồi bấm **Phân tích ngay**.

Lệnh cũ vẫn chạy được:

```bash
python3 topic_suggestion_app.py
```

## Cách hệ thống hoạt động

Luồng xử lý chính:

1. Người dùng nhập văn bản.
2. Hệ thống chuẩn hóa chữ thường và làm sạch văn bản.
3. Văn bản được tách thành danh sách từ.
4. Các stopwords phổ biến được loại bỏ.
5. Hệ thống tạo vector Bag of Words dựa trên bộ dữ liệu mẫu.
6. Mỗi chủ đề được chấm điểm bằng nhiều thành phần:
   - Cosine Similarity
   - Keyword Weighting
   - Phrase Matching
   - Context Bonus
   - Conflict Penalty
7. Chủ đề có điểm cuối cùng cao nhất được chọn làm kết quả dự đoán.
8. Kết quả, điểm chi tiết và phần giải thích được hiển thị trên giao diện.

## Bộ dữ liệu mẫu

Bộ dữ liệu mẫu được khai báo trong `data/sample_dataset.py`. Mỗi chủ đề có 10 văn bản mẫu, tổng cộng 40 văn bản.

Các văn bản này được dùng để:

- Xây dựng từ điển Bag of Words.
- Tạo hồ sơ vector cho từng chủ đề.
- Làm cơ sở so sánh với văn bản người dùng nhập.

## Lịch sử phân tích

Mỗi lần phân tích thành công, kết quả được lưu vào:

```text
analysis_history.json
```

File này chứa văn bản gốc, văn bản đã làm sạch, danh sách từ sau xử lý, chủ đề dự đoán, mức độ tin cậy, điểm từng chủ đề và phần giải thích.

Trong giao diện, người dùng có thể bấm **Xem lịch sử** để xem lại các lần phân tích trước.

## Ghi chú

Đây là dự án học tập về xử lý ngôn ngữ tự nhiên cơ bản. Hệ thống chưa dùng mô hình học máy phức tạp hoặc thư viện NLP chuyên dụng, nên kết quả phụ thuộc nhiều vào bộ dữ liệu mẫu, danh sách từ khóa và quy tắc chấm điểm được viết sẵn.
