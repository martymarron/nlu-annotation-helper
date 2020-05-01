# -*- coding: utf-8 -*-

from pytest import raises
from nlu_annotation_helper.annotate_utterance import *


def test_detect_lang_ja():
    expected = "ja"
    actual = AnnotateUtterance.detect_lang("次")

    assert actual == expected


def test_detect_lang_en():
    expected = "en"
    actual = AnnotateUtterance.detect_lang("next")

    assert actual == expected


def test_get_instance():
    annotate_uttr = AnnotateUtterance.get_instance()

    expected = (type(AnnotateJapaneseUtterance()), type(AnnotateSpanishUtterance()))
    actual = (type(annotate_uttr), type(annotate_uttr.get_next()))

    assert actual == expected


def test_annotate_en():
    annotate_uttr = AnnotateUtterance.get_instance()

    with raises(LanguageNotSupportedError):
        annotate_uttr.annotate("Hello", {})


def test_annotate_ja():
    annotate_uttr = AnnotateJapaneseUtterance()

    expected = ("{テレビ|DeviceType}を{消して|ActionTrigger}", ["DeviceType","ActionTrigger"])
    actual = annotate_uttr.execute("テレビを消して", {"ActionTrigger": "消して", "DeviceType": "テレビ", "Appliance": "テレビ"})

    assert actual == expected


def test_annotate_es():
    annotate_uttr = AnnotateSpanishUtterance()

    expected = ("Apaga|ActionTrigger la luz|DeviceType", ['ActionTrigger', 'DeviceType'])
    actual = annotate_uttr.execute("Apaga la luz", {"ActionTrigger": "Apaga", "DeviceType": "luz", "Appliance": "luz"})

    assert actual == expected
