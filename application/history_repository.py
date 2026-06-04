# -*- coding: utf-8 -*-
from typing import Protocol

from domain.entities import AnalysisResult


class HistoryRepository(Protocol):
    def load_all(self):
        pass

    def save(self, result: AnalysisResult) -> None:
        pass
