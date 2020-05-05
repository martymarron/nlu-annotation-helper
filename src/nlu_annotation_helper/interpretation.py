# -*- coding: utf-8 -*-

from logging import getLogger, INFO, DEBUG, StreamHandler
from .annotate_utterance import AnnotateUtterance


class Interpretation:
    """
    Interpretation class describes an interpretation object of BINF.

    Attributes:
        domain(str): Domain name.
        intent(str): Intent name.
        utterance(str): Utterance text. This is a plain text.
        slot_values(dic): Pairs of label and token.
            e.g. label and tokens for "Turn on the light."
            {
                "Alliance": "light",
                "DeviceType": "light",
                "ActionTrigger": "turn",
                "ActionTrigger": "on"
            }
        lang(str): Language code. This indicate the language of given utterance.
    """

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

    def get_annotated_utterance(self) -> (str, list):
        """
        This function returns an annotated utterance.

        The intended text to be annotated is an utterance attribute of an interpretation instance.

        Note: If the value of intent attribute is "PhaticIntent", returned utterance is not annotated.
        Since the slot_value attribute is not a pair of label and token if "PhaticIntent"

        :return:
        :rtype: str, list
        """
        if self.intent in ["PhaticIntent"]:
            return self.utterance.replace(" ", ""), []
        else:
            return self.__annotate()

    def __annotate(self):
        annotate_uttr = AnnotateUtterance.get_instance(lang=self.lang)
        return annotate_uttr.annotate(uttr=self.utterance, slot_values=self.slotValues)
