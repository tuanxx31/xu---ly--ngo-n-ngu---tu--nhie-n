# -*- coding: utf-8 -*-
"""
Compatibility facade for the old UI module name.

The Tkinter presentation code now lives in presentation/tkinter_app.py.
"""
from presentation.tkinter_app import TopicSuggestionApp


__all__ = ["TopicSuggestionApp"]
