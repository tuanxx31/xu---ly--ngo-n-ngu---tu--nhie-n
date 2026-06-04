# -*- coding: utf-8 -*-
import tkinter as tk
from collections import Counter
from tkinter import filedialog, messagebox, scrolledtext, ttk

from application.topic_analyzer import TopicAnalyzer
from data.sample_dataset import SAMPLE_DATA
from domain.topic_config import APP_TITLE, MIN_WORDS_REQUIRED, TOPICS
from infrastructure.document_reader import DocumentReader
from infrastructure.json_history_repository import JsonHistoryRepository


class TopicSuggestionApp:
    """Giao diện Tkinter cho hệ thống gợi ý chủ đề bài viết ngắn."""

    COLORS = {
        "bg": "#f4f7fb",
        "surface": "#ffffff",
        "surface_2": "#f8fafc",
        "primary": "#2563eb",
        "primary_dark": "#1d4ed8",
        "text": "#0f172a",
        "muted": "#64748b",
        "border": "#e2e8f0",
        "success": "#16a34a",
        "warning": "#f59e0b",
        "danger": "#dc2626",
    }

    TOPIC_COLORS = {
        "Công nghệ": "#2563eb",
        "Giáo dục": "#7c3aed",
        "Sức khỏe": "#16a34a",
        "Thể thao": "#f97316",
    }

    def __init__(self, root, analyzer=None, history_repository=None, document_reader=None):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1320x860")
        self.root.minsize(1160, 760)
        self.root.configure(bg=self.COLORS["bg"])

        self.analyzer = analyzer or TopicAnalyzer(SAMPLE_DATA)
        self.history_repository = history_repository or JsonHistoryRepository()
        self.document_reader = document_reader or DocumentReader()
        self.dataset = self.analyzer.dataset
        self.vocabulary = self.analyzer.vocabulary
        self.basic_report = self.analyzer.build_basic_python_report()
        self.placeholder_text = "Ví dụ: Học sinh tham gia lớp học trực tuyến và xem bài giảng online để ôn thi cuối kỳ..."

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()
        self.build_layout()
        self.insert_placeholder()

    def configure_styles(self):
        c = self.COLORS
        self.style.configure("App.TFrame", background=c["bg"])
        self.style.configure("Card.TFrame", background=c["surface"], relief="flat")
        self.style.configure("Soft.TFrame", background=c["surface_2"], relief="flat")
        self.style.configure("Title.TLabel", background=c["bg"], foreground=c["text"], font=("Segoe UI", 24, "bold"))
        self.style.configure("Subtitle.TLabel", background=c["bg"], foreground=c["muted"], font=("Segoe UI", 10))
        self.style.configure("CardTitle.TLabel", background=c["surface"], foreground=c["text"], font=("Segoe UI", 13, "bold"))
        self.style.configure("Body.TLabel", background=c["surface"], foreground=c["muted"], font=("Segoe UI", 10))
        self.style.configure("Metric.TLabel", background=c["surface_2"], foreground=c["text"], font=("Segoe UI", 16, "bold"))
        self.style.configure("MetricSmall.TLabel", background=c["surface_2"], foreground=c["muted"], font=("Segoe UI", 9))
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 10), background=c["primary"], foreground="#ffffff", borderwidth=0)
        self.style.map("Primary.TButton", background=[("active", c["primary_dark"]), ("pressed", c["primary_dark"])])
        self.style.configure("Ghost.TButton", font=("Segoe UI", 10), padding=(14, 10), background=c["surface_2"], foreground=c["text"], borderwidth=0)
        self.style.map("Ghost.TButton", background=[("active", "#eef2ff"), ("pressed", "#e0e7ff")])
        self.style.configure("TNotebook", background=c["surface"], borderwidth=0)
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=(16, 9))

    def build_layout(self):
        main = ttk.Frame(self.root, style="App.TFrame", padding=22)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main, style="App.TFrame")
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="Gợi ý chủ đề bài viết ngắn", style="Title.TLabel").pack(anchor="w")

        content = ttk.Frame(main, style="App.TFrame")
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=7)
        content.columnconfigure(1, weight=5)
        content.rowconfigure(0, weight=1)

        left = ttk.Frame(content, style="App.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        right = ttk.Frame(content, style="App.TFrame")
        right.grid(row=0, column=1, sticky="nsew")

        self.build_input_card(left)
        self.build_result_card(left)
        self.build_dashboard(right)

    def card(self, parent, padding=16):
        frame = tk.Frame(parent, bg=self.COLORS["surface"], bd=0, highlightthickness=1, highlightbackground=self.COLORS["border"])
        frame.pack(fill="both", expand=False, pady=(0, 14))
        inner = ttk.Frame(frame, style="Card.TFrame", padding=padding)
        inner.pack(fill="both", expand=True)
        return inner

    def build_input_card(self, parent):
        card = self.card(parent)
        ttk.Label(card, text="1. Nhập văn bản cần phân loại", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text="Nhập tối thiểu 5 từ. Hệ thống sẽ xử lý văn bản, tính điểm và đưa ra chủ đề phù hợp nhất.", style="Body.TLabel").pack(anchor="w", pady=(3, 10))

        self.input_text = scrolledtext.ScrolledText(card, wrap="word", height=8, font=("Segoe UI", 11), bg="#ffffff", fg=self.COLORS["text"], insertbackground=self.COLORS["primary"], relief="flat", bd=1, padx=12, pady=12)
        self.input_text.pack(fill="x")
        self.input_text.bind("<FocusIn>", self.on_input_focus_in)
        self.input_text.bind("<FocusOut>", self.on_input_focus_out)

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Phân tích ngay", command=self.analyze_text, style="Primary.TButton").pack(side="left")
        ttk.Button(actions, text="Import file", command=self.import_document, style="Ghost.TButton").pack(side="left", padx=8)
        ttk.Button(actions, text="Xóa", command=self.clear_content, style="Ghost.TButton").pack(side="left", padx=8)
        ttk.Button(actions, text="Dữ liệu mẫu + Bag of Words", command=self.show_sample_data, style="Ghost.TButton").pack(side="left", padx=8)
        ttk.Button(actions, text="Lịch sử", command=self.show_history, style="Ghost.TButton").pack(side="left", padx=8)

    def build_result_card(self, parent):
        card = self.card(parent, padding=0)
        top = ttk.Frame(card, style="Card.TFrame", padding=(16, 14, 16, 0))
        top.pack(fill="x")
        ttk.Label(top, text="2. Kết quả phân tích", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(top, text="Kết quả được trình bày theo dạng báo cáo để dễ đưa vào phần bảo vệ bài.", style="Body.TLabel").pack(anchor="w", pady=(3, 10))

        self.result_text = scrolledtext.ScrolledText(card, wrap="word", font=("Consolas", 10), bg=self.COLORS["surface_2"], fg=self.COLORS["text"], relief="flat", padx=14, pady=14)
        self.result_text.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.set_result_text("Kết quả sẽ hiển thị ở đây sau khi bạn bấm 'Phân tích ngay'.")

    def build_dashboard(self, parent):
        card = self.card(parent)
        ttk.Label(card, text="Tổng quan", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, text="Các thông tin quan trọng của hệ thống và biểu đồ xác suất sẽ nằm tại đây.", style="Body.TLabel").pack(anchor="w", pady=(3, 12))

        stats = ttk.Frame(card, style="Card.TFrame")
        stats.pack(fill="x")
        topic_counts = Counter(item.label for item in self.dataset)
        per_topic = min(topic_counts.values()) if topic_counts else 0
        metrics = [("Văn bản mẫu", len(self.dataset)), ("Chủ đề", len(TOPICS)), ("Từ điển", len(self.vocabulary)), ("Mỗi chủ đề", per_topic)]
        for i, (name, value) in enumerate(metrics):
            box = ttk.Frame(stats, style="Soft.TFrame", padding=12)
            box.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 8, 0))
            stats.columnconfigure(i, weight=1)
            ttk.Label(box, text=str(value), style="Metric.TLabel").pack(anchor="w")
            ttk.Label(box, text=name, style="MetricSmall.TLabel").pack(anchor="w")

        ttk.Label(card, text="Biểu đồ xác suất", style="CardTitle.TLabel").pack(anchor="w", pady=(18, 8))
        self.chart_canvas = tk.Canvas(card, height=230, bg=self.COLORS["surface"], highlightthickness=0)
        self.chart_canvas.pack(fill="x")
        self.draw_empty_chart()

        ttk.Label(card, text="Quy trình thuật toán", style="CardTitle.TLabel").pack(anchor="w", pady=(14, 8))
        self.pipeline_text = tk.Text(card, height=10, wrap="word", bg=self.COLORS["surface_2"], fg=self.COLORS["text"], relief="flat", padx=12, pady=12, font=("Segoe UI", 10))
        self.pipeline_text.pack(fill="both", expand=True)
        self.pipeline_text.insert("1.0", self.build_algorithm_report())
        self.pipeline_text.configure(state="disabled")

    def build_algorithm_report(self):
        return "\n".join([
            "Bước 1: Chuẩn hóa văn bản: chuyển về chữ thường, xóa dấu câu, xóa khoảng trắng thừa.",
            "Bước 2: Tách từng tiếng theo khoảng trắng, tạo cụm 2-3 từ và loại bỏ stopwords cơ bản.",
            "Bước 3: Tạo Bag of Words: đếm tần suất từ xuất hiện trong từng chủ đề.",
            "Bước 4: Biểu diễn văn bản nhập vào thành vector theo từ điển chung.",
            "Bước 5: Tính Cosine Similarity giữa văn bản nhập và hồ sơ từng chủ đề.",
            "Bước 6: Cộng điểm từ khóa, cụm từ đặc trưng và điểm ngữ cảnh.",
            "Bước 7: Trừ penalty nếu văn bản có tín hiệu gây nhiễu từ chủ đề khác.",
            "Bước 8: Chọn chủ đề có điểm cuối cùng cao nhất và hiển thị xác suất tương đối.",
        ])

    def draw_empty_chart(self):
        self.chart_canvas.delete("all")
        self.chart_canvas.create_text(12, 20, anchor="w", text="Chưa có dữ liệu phân tích", fill=self.COLORS["muted"], font=("Segoe UI", 11, "bold"))
        y = 58
        for topic in TOPICS:
            self.chart_canvas.create_text(12, y, anchor="w", text=topic, fill=self.COLORS["text"], font=("Segoe UI", 10))
            self.chart_canvas.create_rectangle(110, y - 8, 420, y + 8, fill="#e2e8f0", outline="")
            y += 38

    def draw_probability_chart(self, prediction):
        self.chart_canvas.delete("all")
        self.chart_canvas.update_idletasks()
        width = max(self.chart_canvas.winfo_width(), 460)
        left, right = 115, width - 58
        y = 38
        self.chart_canvas.create_text(12, 14, anchor="w", text=f"Dự đoán: {prediction.predicted_topic} • Tin cậy: {prediction.confidence}", fill=self.COLORS["text"], font=("Segoe UI", 11, "bold"))
        for topic, _score in prediction.scores:
            percent = prediction.relative_percentages.get(topic, 0.0)
            color = self.TOPIC_COLORS.get(topic, self.COLORS["primary"])
            bar_width = int((right - left) * percent / 100)
            self.chart_canvas.create_text(12, y, anchor="w", text=topic, fill=self.COLORS["text"], font=("Segoe UI", 10))
            self.chart_canvas.create_rectangle(left, y - 9, right, y + 9, fill="#e2e8f0", outline="")
            self.chart_canvas.create_rectangle(left, y - 9, left + bar_width, y + 9, fill=color, outline="")
            self.chart_canvas.create_text(right + 8, y, anchor="w", text=f"{percent:.1f}%", fill=self.COLORS["text"], font=("Segoe UI", 10, "bold"))
            y += 42

    def insert_placeholder(self):
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", self.placeholder_text)
        self.input_text.configure(fg=self.COLORS["muted"])

    def on_input_focus_in(self, _event):
        if self.input_text.get("1.0", "end").strip() == self.placeholder_text:
            self.input_text.delete("1.0", "end")
            self.input_text.configure(fg=self.COLORS["text"])

    def on_input_focus_out(self, _event):
        if not self.input_text.get("1.0", "end").strip():
            self.insert_placeholder()

    def get_input_content(self):
        content = self.input_text.get("1.0", "end").strip()
        return "" if content == self.placeholder_text else content

    def set_result_text(self, content):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", content)
        self.result_text.configure(state="disabled")

    def import_document(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file văn bản cần phân loại",
            filetypes=[
                ("Tài liệu hỗ trợ", "*.txt *.docx *.pdf"),
                ("Text file", "*.txt"),
                ("Word file", "*.docx"),
                ("PDF file", "*.pdf"),
                ("Tất cả file", "*.*"),
            ],
        )
        if not file_path:
            return

        try:
            content = self.document_reader.read(file_path)
        except Exception as error:
            messagebox.showerror(
                "Không import được file",
                f"Không thể đọc nội dung file.\n\nChi tiết lỗi:\n{error}",
            )
            return

        if not content.strip():
            messagebox.showwarning(
                "File không có nội dung",
                "Không trích xuất được văn bản từ file này. Nếu là PDF scan dạng ảnh thì chương trình không đọc được vì chưa dùng OCR.",
            )
            return

        self.input_text.configure(state="normal", fg=self.COLORS["text"])
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", content.strip())
        self.set_result_text(
            "Đã import nội dung file thành công.\n"
            "Bạn có thể kiểm tra/chỉnh sửa nội dung trong ô nhập rồi bấm 'Phân tích ngay'."
        )

    def analyze_text(self):
        input_content = self.get_input_content()
        if not input_content:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập nội dung bài viết trước khi phân tích.")
            return
        processed = self.analyzer.preprocess_text(input_content)
        if len(processed.raw_tokens) < MIN_WORDS_REQUIRED:
            messagebox.showwarning("Văn bản quá ngắn", f"Vui lòng nhập ít nhất {MIN_WORDS_REQUIRED} từ để phân tích chính xác hơn.")
            return

        result = self.analyzer.analyze(input_content)
        prediction = result.prediction
        self.set_result_text(self.build_result_content(result))
        self.draw_probability_chart(prediction)
        self.history_repository.save(result)

    def build_result_content(self, result):
        prediction = result.prediction
        processed = prediction.processed
        score_lines, keyword_lines, phrase_lines = [], [], []
        for topic, final_score in prediction.scores:
            detail = prediction.score_breakdown[topic]
            percent = prediction.relative_percentages.get(topic, 0.0)
            score_lines.append(f"- {topic:<9}: {percent:>6.2f}% | final={final_score:.4f} | cosine={detail.cosine_score:.4f} | keyword={detail.keyword_score:.2f} | phrase={detail.phrase_score:.2f} | context={detail.context_bonus:.2f} | penalty={detail.conflict_penalty:.2f}")
            keyword_lines.append(f"- {topic}: {', '.join(detail.keyword_matches) if detail.keyword_matches else 'Không phát hiện rõ'}")
            phrase_lines.append(f"- {topic}: {', '.join(detail.phrase_matches) if detail.phrase_matches else 'Không phát hiện rõ'}")
        warning_text = prediction.ambiguity_warning or "Không có cảnh báo đáng kể."
        competing_topic = prediction.scores[1][0] if len(prediction.scores) > 1 else "Không có"
        return "\n".join([
            "KẾT QUẢ PHÂN TÍCH CHỦ ĐỀ", "",
            f"Chủ đề dự đoán cuối cùng : {prediction.predicted_topic}",
            f"Mức độ tin cậy          : {prediction.confidence}",
            f"Chủ đề cạnh tranh       : {competing_topic}",
            f"Số từ trong văn bản     : {len(processed.raw_tokens)}", "",
            "BẢNG ĐIỂM / XÁC SUẤT TỪNG CHỦ ĐỀ", *score_lines, "",
            "TỪ KHÓA PHÁT HIỆN", *keyword_lines, "",
            "CỤM TỪ ĐẶC TRƯNG", *phrase_lines, "",
            f"CẢNH BÁO: {warning_text}", "",
            "TIỀN XỬ LÝ VĂN BẢN",
            f"- Văn bản sau chuẩn hóa: {processed.cleaned_text}",
            f"- Tách từ bằng khoảng trắng: {processed.raw_tokens}",
            f"- Cụm 2-3 từ tạo bởi extract_phrases(): {processed.phrases[:20]}",
            f"- Sau bỏ stopwords: {processed.tokens}", "",
            "GIẢI THÍCH", result.explanation,
        ])

    def clear_content(self):
        self.insert_placeholder()
        self.set_result_text("Kết quả sẽ hiển thị ở đây sau khi bạn bấm 'Phân tích ngay'.")
        self.draw_empty_chart()

    def build_bow_matrix(self, max_terms=18):
        topic_token_counts = {topic: Counter() for topic in TOPICS}
        global_counter = Counter()
        for item in self.dataset:
            tokens = self.analyzer.preprocess_text(item.text).tokens
            topic_token_counts[item.label].update(tokens)
            global_counter.update(tokens)
        top_terms = [term for term, _ in global_counter.most_common(max_terms)]
        header = f"{'Từ':<18}" + "".join(f"{topic:^12}" for topic in TOPICS)
        lines = ["MA TRẬN BAG OF WORDS RÚT GỌN", header, "-" * len(header)]
        for term in top_terms:
            row = f"{term:<18}" + "".join(f"{topic_token_counts[topic].get(term, 0):^12}" for topic in TOPICS)
            lines.append(row)
        return "\n".join(lines)

    def show_sample_data(self):
        window = tk.Toplevel(self.root)
        window.title("Dữ liệu mẫu và Bag of Words")
        window.geometry("1120x760")
        window.configure(bg=self.COLORS["bg"])
        frame = ttk.Frame(window, style="App.TFrame", padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Dữ liệu mẫu, báo cáo Python và ma trận Bag of Words", style="Title.TLabel").pack(anchor="w", pady=(0, 12))
        text_widget = scrolledtext.ScrolledText(frame, wrap="word", font=("Consolas", 10), bg="#ffffff", fg=self.COLORS["text"], relief="flat", padx=14, pady=14)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", self.build_sample_data_view())
        text_widget.configure(state="disabled")

    def build_sample_data_view(self):
        topic_counts = Counter(item.label for item in self.dataset)
        lines = [self.basic_report, "", self.build_bow_matrix(), "", "THỐNG KÊ DATASET THEO CHỦ ĐỀ"]
        lines.extend(f"- {topic}: {topic_counts.get(topic, 0)} văn bản" for topic in TOPICS)
        lines.extend(["", "DANH SÁCH VĂN BẢN MẪU THEO NHÃN", ""])
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
        window.configure(bg=self.COLORS["bg"])
        frame = ttk.Frame(window, style="App.TFrame", padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Lịch sử phân tích", style="Title.TLabel").pack(anchor="w", pady=(0, 12))
        text_widget = scrolledtext.ScrolledText(frame, wrap="word", font=("Consolas", 10), bg="#ffffff", fg=self.COLORS["text"], relief="flat", padx=14, pady=14)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", self.build_history_view(history))
        text_widget.configure(state="disabled")

    def build_history_view(self, history):
        lines = []
        for index, item in enumerate(reversed(history), start=1):
            predicted_topic = item.get("predicted_topic", item.get("predicted_label", "Không có dữ liệu"))
            confidence = item.get("confidence", "Không có dữ liệu")
            warning = item.get("ambiguity_warning") or item.get("comment") or "Không có"
            explanation = item.get("explanation") or item.get("comment") or "Không có"

            lines.append(f"Lần phân tích {index}")
            lines.append(f"- Văn bản gốc: {item.get('input_text', '')}")
            lines.append(f"- Văn bản làm sạch: {item.get('cleaned_text', '')}")
            lines.append(f"- Chủ đề dự đoán: {predicted_topic}")
            lines.append(f"- Mức độ tin cậy: {confidence}")
            lines.append(f"- Cảnh báo: {warning}")
            for score in item.get("scores", []):
                lines.append(self.format_history_score(score))
            lines.append(f"- Sau bỏ stopwords: {item.get('tokens', [])}")
            lines.append(f"- Giải thích: {explanation}")
            lines.append("")
        return "\n".join(lines)

    def format_history_score(self, score):
        topic = score.get("topic", score.get("label", "Không rõ"))
        if "final_score" not in score:
            raw_score = score.get("score", 0.0)
            return f"- {topic}: score={raw_score:.4f}"

        return (
            f"- {topic}: final={score['final_score']:.4f}, "
            f"cosine={score.get('cosine_score', 0.0):.4f}, "
            f"keyword={score.get('keyword_score', 0.0):.2f}, "
            f"phrase={score.get('phrase_score', 0.0):.2f}, "
            f"context={score.get('context_bonus', 0.0):.2f}, "
            f"penalty={score.get('conflict_penalty', 0.0):.2f}"
        )
