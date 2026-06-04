# -*- coding: utf-8 -*-
import tkinter as tk
from collections import Counter
from tkinter import messagebox, scrolledtext, ttk

from application.topic_analyzer import TopicAnalyzer
from data.sample_dataset import SAMPLE_DATA
from domain.topic_config import APP_TITLE, MIN_WORDS_REQUIRED, TOPICS
from infrastructure.json_history_repository import JsonHistoryRepository


class TopicSuggestionApp:
    def __init__(self, root, analyzer=None, history_repository=None):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1280x820")
        self.root.minsize(1160, 760)
        self.root.configure(bg="#edf3f8")

        self.analyzer = analyzer or TopicAnalyzer(SAMPLE_DATA)
        self.history_repository = history_repository or JsonHistoryRepository()
        self.dataset = self.analyzer.dataset
        self.vocabulary = self.analyzer.vocabulary
        self.basic_report = self.analyzer.build_basic_python_report()
        self.placeholder_text = "Nhập nội dung bài viết ngắn..."

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()
        self.build_layout()
        self.insert_placeholder()

    def configure_styles(self):
        self.style.configure("Main.TFrame", background="#edf3f8")
        self.style.configure("Card.TLabelframe", background="#f9fbfd", borderwidth=1, relief="solid")
        self.style.configure("Card.TLabelframe.Label", background="#f9fbfd", foreground="#17324d", font=("Segoe UI", 12, "bold"))
        self.style.configure("Title.TLabel", background="#edf3f8", foreground="#12344d", font=("Segoe UI", 22, "bold"))
        self.style.configure("SubTitle.TLabel", background="#edf3f8", foreground="#4b6278", font=("Segoe UI", 10))
        self.style.configure("Info.TLabel", background="#f9fbfd", foreground="#23445f", font=("Segoe UI", 10))
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=10)
        self.style.configure("Secondary.TButton", font=("Segoe UI", 10), padding=10)

    def build_layout(self):
        main_frame = ttk.Frame(self.root, style="Main.TFrame", padding=18)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text=APP_TITLE, style="Title.TLabel").pack(anchor="center", pady=(0, 6))
        ttk.Label(
            main_frame,
            text="Phân loại bằng Bag of Words + Cosine Similarity + Keyword Weighting + Phrase Matching + Conflict Penalty",
            style="SubTitle.TLabel",
        ).pack(anchor="center", pady=(0, 14))

        content_frame = ttk.Frame(main_frame, style="Main.TFrame")
        content_frame.pack(fill="both", expand=True)
        content_frame.columnconfigure(0, weight=5)
        content_frame.columnconfigure(1, weight=4)
        content_frame.rowconfigure(0, weight=1)

        left_frame = ttk.Frame(content_frame, style="Main.TFrame")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        right_frame = ttk.Frame(content_frame, style="Main.TFrame")
        right_frame.grid(row=0, column=1, sticky="nsew")

        self.build_input_section(left_frame)
        self.build_result_section(left_frame)
        self.build_overview_section(right_frame)

    def build_input_section(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Khu vực nhập văn bản", style="Card.TLabelframe", padding=14)
        input_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(
            input_frame,
            text="Nhập nội dung bài viết ngắn để hệ thống phân tích chủ đề, đo độ tin cậy và phát hiện tín hiệu gây nhầm lẫn.",
            style="Info.TLabel",
        ).pack(anchor="w", pady=(0, 10))

        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            wrap="word",
            height=11,
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#1f2933",
            insertbackground="#12344d",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.input_text.pack(fill="x")
        self.input_text.bind("<FocusIn>", self.on_input_focus_in)
        self.input_text.bind("<FocusOut>", self.on_input_focus_out)

        button_frame = ttk.Frame(input_frame, style="Main.TFrame")
        button_frame.pack(fill="x", pady=(12, 0))

        buttons = [
            ("Phân tích chủ đề", self.analyze_text, "Primary.TButton"),
            ("Xóa nội dung", self.clear_content, "Secondary.TButton"),
            ("Xem dữ liệu mẫu", self.show_sample_data, "Secondary.TButton"),
            ("Xem lịch sử", self.show_history, "Secondary.TButton"),
            ("Thoát", self.root.destroy, "Secondary.TButton"),
        ]

        for index, (label, command, style_name) in enumerate(buttons):
            ttk.Button(button_frame, text=label, command=command, style=style_name).grid(
                row=0, column=index, padx=4, sticky="ew"
            )
            button_frame.columnconfigure(index, weight=1)

    def build_result_section(self, parent):
        result_frame = ttk.LabelFrame(parent, text="Kết quả phân tích", style="Card.TLabelframe", padding=14)
        result_frame.pack(fill="both", expand=True)

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap="word",
            font=("Consolas", 10),
            bg="#fefefe",
            fg="#1b2631",
            relief="flat",
            padx=10,
            pady=10,
        )
        self.result_text.pack(fill="both", expand=True)
        self.set_result_text("Kết quả sẽ hiển thị tại đây sau khi bạn phân tích văn bản.")

    def build_overview_section(self, parent):
        overview_frame = ttk.LabelFrame(parent, text="Tổng quan hệ thống", style="Card.TLabelframe", padding=14)
        overview_frame.pack(fill="both", expand=True)

        overview_text = scrolledtext.ScrolledText(
            overview_frame,
            wrap="word",
            font=("Segoe UI", 10),
            bg="#fefefe",
            fg="#22313f",
            relief="flat",
            padx=10,
            pady=10,
        )
        overview_text.pack(fill="both", expand=True)
        overview_text.insert("1.0", self.build_overview_message())
        overview_text.configure(state="disabled")

    def build_overview_message(self):
        topic_counts = Counter(item.label for item in self.dataset)
        return "\n".join([
            "THÔNG TIN DỰ ÁN",
            "",
            f"- Tổng số văn bản mẫu: {len(self.dataset)}",
            f"- Số chủ đề hỗ trợ: {len(TOPICS)}",
            f"- Phân bố dataset: {', '.join(f'{topic}={topic_counts.get(topic, 0)}' for topic in TOPICS)}",
            f"- Kích thước từ điển sau khi bỏ stopwords: {len(self.vocabulary)} từ",
            "",
            "THÀNH PHẦN THUẬT TOÁN",
            "- Chuẩn hóa văn bản, xóa dấu câu, bỏ stopwords",
            "- Bag of Words + Cosine Similarity",
            "- Keyword Weighting cho từ khóa đặc trưng",
            "- Phrase Matching cho cụm từ 2-3 từ",
            "- Conflict Penalty để giảm nhầm lẫn liên chủ đề",
            "- Context Bonus cho các ngữ cảnh mạnh như học trực tuyến, khám bệnh, trí tuệ nhân tạo, trận đấu",
            "",
            "QUY TẮC CẢNH BÁO",
            "- Nếu điểm cao nhất và điểm thứ hai chênh lệch dưới 10%, hệ thống báo kết quả chưa thật sự chắc chắn",
        ])

    def insert_placeholder(self):
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", self.placeholder_text)
        self.input_text.configure(fg="#7f8c8d")

    def on_input_focus_in(self, _event):
        current_text = self.input_text.get("1.0", "end").strip()
        if current_text == self.placeholder_text:
            self.input_text.delete("1.0", "end")
            self.input_text.configure(fg="#1f2933")

    def on_input_focus_out(self, _event):
        current_text = self.input_text.get("1.0", "end").strip()
        if not current_text:
            self.insert_placeholder()

    def get_input_content(self):
        content = self.input_text.get("1.0", "end").strip()
        if content == self.placeholder_text:
            return ""
        return content

    def set_result_text(self, content):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", content)
        self.result_text.configure(state="disabled")

    def analyze_text(self):
        input_content = self.get_input_content()
        if not input_content:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập nội dung bài viết trước khi phân tích.")
            return

        processed = self.analyzer.preprocess_text(input_content)
        if len(processed.raw_tokens) < MIN_WORDS_REQUIRED:
            messagebox.showwarning(
                "Văn bản quá ngắn",
                f"Vui lòng nhập ít nhất {MIN_WORDS_REQUIRED} từ để hệ thống phân tích chính xác hơn.",
            )
            return

        result = self.analyzer.analyze(input_content)
        self.set_result_text(self.build_result_content(result))
        self.history_repository.save(result)

    def build_result_content(self, result):
        prediction = result.prediction
        processed = prediction.processed
        score_lines = []
        keyword_lines = []
        phrase_lines = []
        conflict_lines = []

        for topic, final_score in prediction.scores:
            detail = prediction.score_breakdown[topic]
            relative_percent = prediction.relative_percentages.get(topic, 0.0)
            score_lines.append(
                f"- {topic}: final={final_score:.4f} | tỷ lệ={relative_percent:.2f}% | cosine={detail.cosine_score:.4f} | "
                f"keyword={detail.keyword_score:.2f} | phrase={detail.phrase_score:.2f} | "
                f"context={detail.context_bonus:.2f} | penalty={detail.conflict_penalty:.2f}"
            )
            keyword_lines.append(
                f"- {topic}: {', '.join(detail.keyword_matches) if detail.keyword_matches else 'Không phát hiện rõ'}"
            )
            phrase_lines.append(
                f"- {topic}: {', '.join(detail.phrase_matches) if detail.phrase_matches else 'Không phát hiện rõ'}"
            )
            conflict_lines.append(
                f"- {topic}: {'; '.join(detail.conflict_details[:4]) if detail.conflict_details else 'Không có tín hiệu nhiễu mạnh'}"
            )

        warning_text = prediction.ambiguity_warning if prediction.ambiguity_warning else "Không có cảnh báo đáng kể."
        competing_topic = prediction.scores[1][0] if len(prediction.scores) > 1 else "Không có"

        return "\n".join([
            "KẾT QUẢ PHÂN TÍCH CHỦ ĐỀ",
            "",
            f"Chủ đề dự đoán cuối cùng: {prediction.predicted_topic}",
            f"Mức độ tin cậy: {prediction.confidence}",
            f"Chủ đề cạnh tranh gần nhất: {competing_topic}",
            f"Số từ trong văn bản: {len(processed.raw_tokens)}",
            "",
            "Điểm của cả 4 chủ đề:",
            *score_lines,
            "",
            "Từ khóa phát hiện được:",
            *keyword_lines,
            "",
            "Cụm từ đặc trưng phát hiện được:",
            *phrase_lines,
            "",
            "Tín hiệu gây nhiễu theo từng chủ đề:",
            *conflict_lines,
            "",
            f"Cảnh báo nếu có khả năng nhầm lẫn: {warning_text}",
            "",
            f"Văn bản sau chuẩn hóa: {processed.cleaned_text}",
            f"Danh sách từ sau khi tách cơ bản: {processed.raw_tokens}",
            f"Danh sách từ sau khi bỏ stopwords: {processed.tokens}",
            "",
            "Giải thích vì sao hệ thống chọn chủ đề đó:",
            result.explanation,
        ])

    def clear_content(self):
        self.insert_placeholder()
        self.set_result_text("Kết quả sẽ hiển thị tại đây sau khi bạn phân tích văn bản.")

    def show_sample_data(self):
        window = tk.Toplevel(self.root)
        window.title("Dữ liệu mẫu")
        window.geometry("1040x740")
        window.configure(bg="#edf3f8")

        frame = ttk.Frame(window, style="Main.TFrame", padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="DỮ LIỆU MẪU VÀ BÁO CÁO PYTHON CƠ BẢN", style="Title.TLabel").pack(
            anchor="center", pady=(0, 10)
        )

        text_widget = scrolledtext.ScrolledText(
            frame,
            wrap="word",
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#22313f",
            relief="flat",
            padx=10,
            pady=10,
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", self.build_sample_data_view())
        text_widget.configure(state="disabled")

    def build_sample_data_view(self):
        topic_counts = Counter(item.label for item in self.dataset)
        lines = [
            self.basic_report,
            "\nTHỐNG KÊ DATASET THEO CHỦ ĐỀ",
            *(f"- {topic}: {topic_counts.get(topic, 0)} văn bản" for topic in TOPICS),
            "\nDANH SÁCH VĂN BẢN MẪU THEO NHÃN",
            "",
        ]
        for index, item in enumerate(self.dataset, start=1):
            lines.append(f"{index}. [{item.label}] {item.text}")
        return "\n".join(lines)

    def show_history(self):
        history = self.history_repository.load_all()
        if not history:
            messagebox.showinfo("Lịch sử trống", "Chưa có lịch sử phân tích nào được lưu.")
            return

        window = tk.Toplevel(self.root)
        window.title("Lịch sử phân tích")
        window.geometry("1040x740")
        window.configure(bg="#edf3f8")

        frame = ttk.Frame(window, style="Main.TFrame", padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="LỊCH SỬ PHÂN TÍCH", style="Title.TLabel").pack(anchor="center", pady=(0, 10))

        text_widget = scrolledtext.ScrolledText(
            frame,
            wrap="word",
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#22313f",
            relief="flat",
            padx=10,
            pady=10,
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", self.build_history_view(history))
        text_widget.configure(state="disabled")

    def build_history_view(self, history):
        lines = []
        for index, item in enumerate(reversed(history), start=1):
            lines.append(f"Lần phân tích {index}")
            lines.append(f"- Văn bản gốc: {item['input_text']}")
            lines.append(f"- Văn bản làm sạch: {item['cleaned_text']}")
            lines.append(f"- Chủ đề dự đoán: {item['predicted_topic']}")
            lines.append(f"- Mức độ tin cậy: {item['confidence']}")
            lines.append(f"- Cảnh báo: {item['ambiguity_warning'] if item['ambiguity_warning'] else 'Không có'}")
            for score in item["scores"]:
                lines.append(
                    f"- {score['topic']}: final={score['final_score']:.4f}, cosine={score['cosine_score']:.4f}, "
                    f"keyword={score['keyword_score']:.2f}, phrase={score['phrase_score']:.2f}, "
                    f"context={score['context_bonus']:.2f}, penalty={score['conflict_penalty']:.2f}"
                )
            lines.append(f"- Danh sách từ: {item['tokens']}")
            lines.append(f"- Giải thích: {item['explanation']}")
            lines.append("")
        return "\n".join(lines)
