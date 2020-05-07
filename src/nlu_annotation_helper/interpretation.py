# -*- coding: utf-8 -*-

from logging import getLogger, INFO, DEBUG, StreamHandler
from .annotate_utterance import AnnotateUtterance


class Interpretation:

    _logger = getLogger(__name__)
    _logger.setLevel(DEBUG)

    _stream_handler = StreamHandler()
    _stream_handler.setLevel(DEBUG)
    _logger.addHandler(_stream_handler)

    def __init__(self, domain: str, intent: str, utterance: str, slot_values: dict):

        self.domain = domain
        self.intent = intent
        self.utterance = utterance
        self.slotValues = slot_values
        self.slots = []

        self.lang = None

    def set_lang(self, lang: str = None):
        self.lang = lang

    def get_annotated_utterance(self):
        if self.intent in ["PhaticIntent"]:
            return self.utterance.replace(" ", ""), []
        else:
            return self.__annotate()

    def __annotate(self):
        annotate_uttr = AnnotateUtterance.get_instance(lang=self.lang)
        return annotate_uttr.annotate(uttr=self.utterance, slot_values=self.slotValues)
