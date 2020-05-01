# -*- coding: utf-8 -*-

from nlu_annotation_helper import Interpretation


def test_get_annotated_utterance_with_labeled_tokens_only():
    domain = "HomeAutomation"
    intent = "TurnOffApplianceIntent"
    utterance = "テレビ 消し て"
    slot_values = {
        "ActionTrigger": "消して",
        "DeviceType": "テレビ",
        "Appliance": "テレビ"
    }
    interp = Interpretation(domain, intent, utterance, slot_values)

    expected = ("{テレビ|DeviceType}{消して|ActionTrigger}", ["DeviceType", "ActionTrigger"])
    actual = interp.get_annotated_utterance()

    assert actual == expected


def test_get_annotated_utterance_with_non_labaled_token():
    domain = "HomeAutomation"
    intent = "TurnOffApplianceIntent"
    utterance = "テレビ を 消し て"
    slot_values = {
        "ActionTrigger": "消して",
        "DeviceType": "テレビ",
        "Appliance": "テレビ"
    }
    interp = Interpretation(domain, intent, utterance, slot_values)

    expected = ("{テレビ|DeviceType}を{消して|ActionTrigger}", ["DeviceType", "ActionTrigger"])
    actual = interp.get_annotated_utterance()

    assert actual == expected


def test_get_annotated_utterance_with_non_labeled_token_only():
    domain = "Global"
    intent = "StopIntent"
    utterance = "止め て"
    slot_values = {}
    interp = Interpretation(domain, intent, utterance, slot_values)

    expected = ("止めて", [])
    actual = interp.get_annotated_utterance()

    assert actual == expected


def test_get_annotated_utterance_with_non_labeled_one_character_token():
    domain = "Global"
    intent = "NextIntent"
    utterance = "次"
    slot_values = {}
    interp = Interpretation(domain, intent, utterance, slot_values)

    expected = ("次", [])
    actual = interp.get_annotated_utterance()

    assert actual == expected


def test_get_annotated_utteranc_with_phaticintent():
    domain = "Global"
    intent = "PhaticIntent"
    utterance = "お やすみ"
    slot_values = {"Greeting": "おやすみ"}
    interp = Interpretation(domain, intent, utterance, slot_values)

    expected = ("おやすみ", [])
    actual = interp.get_annotated_utterance()

    assert actual == expected
