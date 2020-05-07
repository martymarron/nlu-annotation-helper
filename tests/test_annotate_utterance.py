# -*- coding: utf-8 -*-

from pytest import raises, fixture, mark
from nlu_annotation_helper.annotate_utterance import *


@fixture(scope="function")
def annotate_utterance():
    yield
    AnnotateUtterance.lang = None


@mark.parametrize("lang, text", [
    ("ja", "テレビを消して"),
    ("en", "go to next song")
])
@mark.usefixtures("annotate_utterance")
def test_detect_lang_no_set_lang(lang, text):
    expected = lang
    actual = AnnotateUtterance.detect_lang(text=text)

    assert actual == expected


@mark.parametrize("lang, text", [
    ("ja", "テレビを消して"),
    ("en", "turn off tv"),
    ("es", "Apaga la luz")
])
@mark.usefixtures("annotate_utterance")
def test_detect_lang_set_lang(lang, text):
    AnnotateUtterance.lang = lang

    expected = lang
    actual = AnnotateUtterance.detect_lang(text=text)

    assert actual == expected


def test_get_instance():
    annotate_uttr = AnnotateUtterance.get_instance()

    expected = (type(AnnotateJapaneseUtterance()), type(AnnotateSpanishUtterance()))
    actual = (type(annotate_uttr), type(annotate_uttr.get_next()))

    assert actual == expected


@mark.parametrize("lang, text", [
    ("en", "hello")
])
def test_annotate_unsupported_text(lang, text):
    annotate_uttr = AnnotateUtterance.get_instance(lang=lang)

    with raises(LanguageNotSupportedError):
        annotate_uttr.annotate(text, {})


@mark.parametrize("actual_args, expected", [
    (
        # Utterance with labelled tokens.
        {"uttr": "テレビ消して", "slot_values": {"ActionTrigger": "消して", "DeviceType": "テレビ", "Appliance": "テレビ"}},
        ("{テレビ|DeviceType}{消して|ActionTrigger}", ["DeviceType", "ActionTrigger"])
    ),
    (
        # Utterance with non labelled token. Note: "を" should not be labelled.
        {"uttr": "テレビを消して", "slot_values": {"ActionTrigger": "消して", "DeviceType": "テレビ", "Appliance": "テレビ"}},
        ("{テレビ|DeviceType}を{消して|ActionTrigger}", ["DeviceType","ActionTrigger"]),
    ),
    (
        # Utterance with non labelled tokens only.
        {"uttr": "止め て", "slot_values": {}},
        ("止めて", [])
    ),
    (
        # Utterance consists of only one character.
        {"uttr": "次", "slot_values": {}},
        ("次", [])
    )
])
def test_annotate_ja(actual_args, expected):
    instance = AnnotateJapaneseUtterance()
    actual = instance.execute(**actual_args)

    assert actual == expected


@mark.parametrize("actual_args, expected", [
    (
        # Utterance with labelled tokens only
        {"uttr": "Apaga la luz", "slot_values": {"ActionTrigger": "Apaga", "DeviceType": "luz", "Appliance": "luz"}},
        ("Apaga|ActionTrigger la luz|DeviceType", ['ActionTrigger', 'DeviceType'])
    )
])
def test_annotate_es(actual_args, expected):
    instance = AnnotateSpanishUtterance()
    actual = instance.execute(**actual_args)

    assert actual == expected
