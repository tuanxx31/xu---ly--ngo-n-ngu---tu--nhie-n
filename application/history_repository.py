# -*- coding: utf-8 -*-
from typing import Dict, List, Protocol

from domain.entities import AnalysisResult


class HistoryRepository(Protocol):
    def load_all(self) -> List[Dict]:
        pass

    def save(self, result: AnalysisResult) -> None:
        pass
