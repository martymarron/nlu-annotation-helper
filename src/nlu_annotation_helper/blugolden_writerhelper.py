# -*- coding: utf-8 -*-

import os
from pathlib import Path
from .interpretation import Interpretation

BLUGOLDEN_TEST_FILE_DIR = "fud"
BLUGOLDEN_TEST_FILE_EXT = ".txt"
BLUGOLDEN_ATTR_DELIMITER = "\t"
DEFAULT_AVAILABLE_DEVICES = ("doppler", "hendrix", "mshop", "knight", "firetv")


class BluGoldenWriterHelper:

    @classmethod
    def build_blugolden_path(cls, interp: Interpretation) -> Path:
        file_path = cls.build_file_path(interp)
        file_name = cls.build_file_name(interp)
        return Path(file_path, file_name)

    @classmethod
    def build_file_path(cls, interp: Interpretation):
        file_path = os.path.join(BLUGOLDEN_TEST_FILE_DIR, interp.domain, interp.intent)
        return file_path

    @classmethod
    def build_file_name(cls, interp: Interpretation):
        file_name = "{0}{1}".format(interp.intent, BLUGOLDEN_TEST_FILE_EXT)
        return file_name

    @classmethod
    def build_utterance_entry(cls, interp: Interpretation) -> list:
        domain = interp.domain
        intent = interp.intent
        utterance, slots = interp.get_annotated_utterance()
        return [domain, intent, cls.__get_slots_text(slots), utterance, ",".join(DEFAULT_AVAILABLE_DEVICES)]

    @staticmethod
    def __get_slots_text(slots: list):
        return "NULL" if not slots else ",".join(slots)
