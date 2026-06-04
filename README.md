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

## Cấu trúc file

```text
.
├── topic_suggestion_app.py     # File chạy chính của ứng dụng
├── topic_suggestion_ui.py      # Giao diện Tkinter và xử lý thao tác người dùng
├── topic_analysis_core.py      # Logic phân tích văn bản và dự đoán chủ đề
├── requirements.txt            # Ghi chú dependency của dự án
├── analysis_history.json       # Lịch sử phân tích đã lưu
└── README.md                   # Tài liệu mô tả dự án
```

## Cách chạy dự án

Yêu cầu:

- Python 3.x
- Tkinter có sẵn trong bản Python cài đặt trên máy

Dự án không cần cài thêm thư viện ngoài.

Chạy ứng dụng bằng lệnh:

```bash
python3 topic_suggestion_app.py
```

Sau khi chạy, cửa sổ ứng dụng sẽ mở ra. Nhập một đoạn văn bản tiếng Việt ngắn rồi bấm **Phân tích chủ đề**.

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

Bộ dữ liệu mẫu được khai báo trực tiếp trong `topic_analysis_core.py`. Mỗi chủ đề có 10 văn bản mẫu, tổng cộng 40 văn bản.

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
