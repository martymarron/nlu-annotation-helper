# -*- coding: utf-8 -*-

from nlu_annotation_helper import Interpretation
from nlu_annotation_helper import AnnotateUtterance


def test_get_annotated_utterance_with_any_intent(mocker):
    dummy_annotated_result = ("annotated text", ["label"])
    mocker.patch.object(AnnotateUtterance, "annotate", return_value=dummy_annotated_result)

    intent = "TurnOffApplianceIntent"
    interp = Interpretation(domain="", intent=intent, utterance="", slot_values={})

    expected = dummy_annotated_result
    actual = interp.get_annotated_utterance()

    assert actual == expected


def test_get_annotated_utteranc_with_phaticintent():
    domain = "Global"
    intent = "PhaticIntent"
    utterance = "お やすみ"
    slot_values = {"Greeting": "おやすみ"}
    interp = Interpretation(domain, intent, utterance, slot_values)
    interp.set_lang("ja")

    expected = ("おやすみ", [])
    actual = interp.get_annotated_utterance()

    assert actual == expected
