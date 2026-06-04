# -*- coding: utf-8 -*-
import tkinter as tk

from application.topic_analyzer import TopicAnalyzer
from data.sample_dataset import SAMPLE_DATA
from infrastructure.json_history_repository import JsonHistoryRepository
from presentation.tkinter_app import TopicSuggestionApp


def main():
    analyzer = TopicAnalyzer(SAMPLE_DATA)
    history_repository = JsonHistoryRepository()

    root = tk.Tk()
    TopicSuggestionApp(root, analyzer, history_repository)
    root.mainloop()


if __name__ == "__main__":
    main()
