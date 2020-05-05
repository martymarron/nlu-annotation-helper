# -*- coding: utf-8 -*-

from logging import getLogger, StreamHandler, DEBUG, Formatter
from abc import abstractmethod
from langdetect import detect


class AnnotateUtterance:
    """
    A AnnotateUtterance is a command class which annotates a given text.

    This class is an abstract. This abstract class provides an interface of an annotation command.
    A user enables to execute an annotation through this class.

    Multiple language can be processed by this class.
    Any subclass of this class implements actual annotation processes for each languages.
    If an subclass for specific language does not exist, LanguageNotSupportedError will be raised.

    Attributes:
        lang(str): The lang is used for language detection for given texts.
        singleton_instance(AnnotateUtterance): The singleton_instance stores instances of subclasses.
    """

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
        """
        Returns an instance of AnnotateUtterance. This instance is singleton.

        Given lang parameter is stored as class variable of AnnotateUtterance.
        The value of lang parameter will persists until the user replace obviously.
        The lang value parameter will affect the behavior of :func:`annotate`

        :param lang: The lang indicates a language which a returned instance will handle.
                    If lang is not given, an instance will detect a language of text automatically. Optional.
        :return: An instance of AnnotateUtterance.
        """
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
        """
        Annotate a text which is given as :param:`uttr`.

        This function returns an annotated text in BluGoldens format like following.
        Given text: Turn on the light.
        Annotated text: Turn|ActionTrigger on|ActionTrigger the light|Appliance.
        In addition, used label is returned as list.

        The value of slot_values parameter must include labels and tokens as follows.
            code-block:: python
                {
                    "ActionTrigger": "Turn",
                    "ActionTrigger: "on",
                    "Appliance": "light",
                    "DeviceType": "light"
                }
        If same token appears in multiple labels, first one will probably be applied.

        Chain of responsibility:
            AnnotationUtterance has a linked list of its subclasses.
            This function delegates actual annotation process to subclasses of AnnotationUtterance.

        This detect language of given text and assign right subclass to process.
        If right subclass does not exists, this function will raise :class:'LanguageNotSupportedError'.

        :param uttr: The uttr is a plain text to be annotated.
        :param slot_values: The slot_value is a dictionary object which stores labels and tokens as pairs of key and value.
        :return annotated_text, label_list: The annotated_text is an annotated text. The label_text is a list of used labels.
        :rtype: str, list

        """
        lang = self.detect_lang(uttr)
        if self.can_annotate(lang):
            return self.execute(uttr, slot_values)
        elif self._next:
            self._next.annotate(uttr, slot_values)
        else:
            raise LanguageNotSupportedError

    @staticmethod
    def detect_lang(text: str) -> str:
        """
        Detect a language of given text and returns language code.
        Returned language code follows `ISO 639-1 <https://www.iso.org/iso-639-language-codes.html>`_.

        If :attribute:'AnnotateUtterance.lang' has been set, this function returns the value of it.
        If :attribute:'AnnotateUtterance.lang' has not been set,
        this function detect a language by using `detectlang <https://pypi.org/project/detectlanguage/>`_ package.

        :param text: The text parameter to be detected a language.
        :return: The language code of given text.
        :rtype: str
        """
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
        """
        Determine whether given lang can be processed by this class or not.

        This is an abstract method.
        Any subclass of AnnotateUtterance implements this method to determine that given language can be processed by itself.

        :param lang: The lang parameter provides target language to be annotated.
        :return: Return whether the given lang can be processed or not.
        :rtype: bool
        """
        pass

    @abstractmethod
    def execute(self, uttr: str, slot_values: dict) -> (str, list):
        """
        Annotate given text by using given slot values.

        This is an abstract method.
        Any subclass of AnnotateUtterance implements this method to process an intended language.

        :param uttr: The uttr parameter to be annotated.
        :param slot_values: slot_values: The slot_value is a dictionary object which stores labels and tokens as pairs of key and value.
        :return annotated_text, label_list: The annotated_text is an annotated text. The label_text is a list of used labels.
        :rtype: str, list
        """
        pass


class AnnotateJapaneseUtterance(AnnotateUtterance):
    """
    AnnotateJapaneseUtterance provides annotation process for Japanese.
    """

    def __init__(self):
        super().__init__()

    def can_annotate(self, lang: str) -> bool:
        """
        Determine whether given lang can be processed by AnnotateJapaneseUtterance.

        Return true if the value of given lang parameter is "ja".

        :param lang:
        :return:
        """
        self._logger.debug("%s == ja = %s", lang, lang == "ja")
        return lang == "ja"

    def execute(self, uttr: str, slot_values: dict) -> (str, list):
        """
        Annotate given Japanese text.

        :param uttr: The uttr parameter provides text to be annotated.
        :param slot_values: The slot_values parameter provides pairs of label and token.
        :return:
        """
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
    """
    AnnotateJapaneseUtterance provides annotation process for Spanish.
    """

    def __init__(self):
        super().__init__()

    def can_annotate(self, lang: str) -> bool:
        """
        Determine whether given lang can be processed by AnnotateJapaneseUtterance.

        Return true if the value of given lang parameter is "es".

        :param lang:
        :return:
        """
        self._logger.debug("%s == es = %s", lang, lang == "es")
        return lang == "es"

    def execute(self, uttr: str, slot_values: dict) -> (str, list):
        """
         Annotate given Spanish text.

         :param uttr: The uttr parameter provides text to be annotated.
         :param slot_values: The slot_values parameter provides pairs of label and token.
         :return:
        """
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
    """
    LanguageNotSupportedError class is an error class.

    This error is raised when any subclass of AnnotateUtterance does not support annotation process for an given language.
    The user can implement any subclass of AnnotateUtterance if he/she want to expand language support.
    """

    def __init__(self):
        pass
