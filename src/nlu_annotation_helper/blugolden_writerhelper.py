# -*- coding: utf-8 -*-

import os
from pathlib import Path
from .interpretation import Interpretation

BLUGOLDEN_TEST_FILE_DIR = "fud"
BLUGOLDEN_TEST_FILE_EXT = ".txt"
BLUGOLDEN_ATTR_DELIMITER = "\t"
DEFAULT_AVAILABLE_DEVICES = ("doppler", "hendrix", "mshop", "knight", "firetv")


class BluGoldenWriterHelper:
    """
    This class provides helper functions to extract interpretation instances.
    Interpretation instances is saved to a text file in BluGoldens format.
    """

    @classmethod
    def build_blugolden_path(cls, interp: Interpretation) -> Path:
        """
        Build a Path object from a given interpretation instance.
        :param interp:
        :return:
        """
        file_path = cls.build_file_path(interp)
        file_name = cls.build_file_name(interp)
        return Path(file_path, file_name)

    @classmethod
    def build_file_path(cls, interp: Interpretation):
        """
        Build a path string from a given interpretation instance.
        :param interp:
        :return:
        """
        file_path = os.path.join(BLUGOLDEN_TEST_FILE_DIR, interp.domain, interp.intent)
        return file_path

    @classmethod
    def build_file_name(cls, interp: Interpretation):
        """
        Build a file name string from a given interpretation instance.
        :param interp:
        :return:
        """
        file_name = "{0}{1}".format(interp.intent, BLUGOLDEN_TEST_FILE_EXT)
        return file_name

    @classmethod
    def build_utterance_entry(cls, interp: Interpretation) -> list:
        """
        Extract a given interpretation instance to a list.

        :param interp:
        :return:
        """
        domain = interp.domain
        intent = interp.intent
        utterance, slots = interp.get_annotated_utterance()
        return [domain, intent, cls.__get_slots_text(slots), utterance, ",".join(DEFAULT_AVAILABLE_DEVICES)]

    @staticmethod
    def __get_slots_text(slots: list):
        return "NULL" if not slots else ",".join(slots)
