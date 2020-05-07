# -*- coding: utf-8 -*-

from logging import getLogger, StreamHandler, DEBUG, Formatter
from abc import abstractmethod
from langdetect import detect


class AnnotateUtterance:

    _logger = getLogger(__name__)
    _logger.setLevel(DEBUG)

    _stream_handler = StreamHandler()
    _stream_handler.setLevel(DEBUG)
    _stream_handler.setFormatter(
        Formatter("%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"))
    _logger.addHandler(_stream_handler)

    lang: str = None
    singleton_instance = None

    def __init__(self):
        self._next: AnnotateUtterance = None

    @classmethod
    def get_instance(cls, lang: str = None):
        if cls.singleton_instance is None:
            cls.singleton_instance = cls.__initialize()

        if lang:
            cls.lang = lang

        return cls.singleton_instance

    @staticmethod
    def __initialize():
        instance: AnnotateUtterance = AnnotateJapaneseUtterance()
        instance.set_next(AnnotateSpanishUtterance())
        return instance

    def annotate(self, uttr: str, slot_values: dict) -> (str, list):
        lang = self.detect_lang(uttr)
        if self.can_annotate(lang):
            return self.execute(uttr, slot_values)
        elif self._next:
            self._next.annotate(uttr, slot_values)
        else:
            raise LanguageNotSupportedError

    @staticmethod
    def detect_lang(text: str) -> str:
        if AnnotateUtterance.lang:
            detect_lang = AnnotateUtterance.lang
        else:
            detect_lang = detect(text)
        return detect_lang

    def set_next(self, instance):
        self._next: AnnotateUtterance = instance
        return self._next

    def get_next(self):
        return self._next

    @abstractmethod
    def can_annotate(self, lang: str) -> bool:
        pass

    @abstractmethod
    def execute(self, uttr: str, slot_values: dict) -> (str, list):
        pass


class AnnotateJapaneseUtterance(AnnotateUtterance):

    def __init__(self):
        super().__init__()

    def can_annotate(self, lang: str) -> bool:
        self._logger.debug("%s == ja = %s", lang, lang == "ja")
        return lang == "ja"

    def execute(self, uttr: str, slot_values: dict) -> (str, list):
        annotated_tokens = []
        labels = []

        striped_uttr_array = list(uttr.replace(" ", ""))
        i = 0
        j = 0
        self._logger.debug("target: %s", striped_uttr_array)
        while i < len(striped_uttr_array):
            self._logger.debug("i: %s", i)
            matched_token = None
            for label in slot_values:
                token_array = list(slot_values[label].replace(" ", ""))
                self._logger.debug("pattern: %s", token_array)
                find_match = True
                for j in range(len(token_array)):
                    if i+j > len(striped_uttr_array):
                        find_match = False
                        break

                    self._logger.debug("%s == %s", striped_uttr_array[i+j], token_array[j])
                    if striped_uttr_array[i+j] != token_array[j]:
                        find_match = False
                        break

                    self._logger.debug("find_match: %s", find_match)

                if find_match:
                    matched_token = "".join(token_array)
                    self._logger.debug("matched_token: %s", matched_token)
                    break

            if matched_token is not None:
                annotated_tokens.append("{{{0}|{1}}}".format(matched_token, label))
                labels.append(label)
                self._logger.debug("annotated_tokens: %s", annotated_tokens)
                self._logger.debug("i + j = i : %s + %s = %s", i, j, i+j)
                i += j + 1
            else:
                annotated_tokens.append(striped_uttr_array[i])
                i += 1

        return "".join(annotated_tokens), labels


class AnnotateSpanishUtterance(AnnotateUtterance):

    def __init__(self):
        super().__init__()

    def can_annotate(self, lang: str) -> bool:
        self._logger.debug("%s == es = %s", lang, lang == "es")
        return lang == "es"

    def execute(self, uttr: str, slot_values: dict) -> (str, list):
        self._logger.debug("Target: %s", uttr)
        self._logger.debug("Slot values: %s", slot_values.keys())

        annotated_tokens = []
        labels = []

        for token in uttr.split(" "):
            find_match = False
            for k, v in slot_values.items():
                if v == token:
                    label = k
                    annotated_tokens.append("{0}|{1}".format(token, label))
                    labels.append(label)
                    find_match = True
                    break
            if find_match is False:
                annotated_tokens.append(token)

        return " ".join(annotated_tokens), labels


class LanguageNotSupportedError(Exception):

    def __init__(self):
        pass
