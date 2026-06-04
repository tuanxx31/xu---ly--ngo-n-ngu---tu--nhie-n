# -*- coding: utf-8 -*-


def main():
    try:
        import tkinter as tk
        from presentation.tkinter_app import TopicSuggestionApp
    except ModuleNotFoundError as error:
        if error.name in {"_tkinter", "tkinter"}:
            raise SystemExit(
                "Python hiện tại thiếu Tkinter. Hãy chạy bằng Python có Tkinter "
                "(ví dụ: /opt/homebrew/bin/python3 main.py) hoặc cài python-tk "
                "đúng phiên bản Python đang dùng."
            ) from error
        raise

    from application.topic_analyzer import TopicAnalyzer
    from data.sample_dataset import SAMPLE_DATA
    from infrastructure.document_reader import DocumentReader
    from infrastructure.json_history_repository import JsonHistoryRepository

    analyzer = TopicAnalyzer(SAMPLE_DATA)
    history_repository = JsonHistoryRepository()
    document_reader = DocumentReader()

    root = tk.Tk()
    TopicSuggestionApp(
        root,
        analyzer=analyzer,
        history_repository=history_repository,
        document_reader=document_reader,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
