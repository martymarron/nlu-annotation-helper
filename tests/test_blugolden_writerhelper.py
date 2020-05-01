# -*- coding: utf-8 -*-

from nlu_annotation_helper.interpretation import Interpretation
from nlu_annotation_helper.blugolden_writerhelper import BluGoldenWriterHelper, BLUGOLDEN_TEST_FILE_DIR, \
    DEFAULT_AVAILABLE_DEVICES


def test_create_blugolden_file_name():
    interp = Interpretation("Global", "YesIntent", "はい", [])

    expected = "YesIntent.txt"
    actual = BluGoldenWriterHelper.build_file_name(interp)

    assert actual == expected


def test_create_blugolden_file_path():
    interp = Interpretation("Global", "YesIntent", "はい", [])

    expected = "{0}/Global/YesIntent".format(BLUGOLDEN_TEST_FILE_DIR)
    actual = BluGoldenWriterHelper.build_file_path(interp)

    assert actual == expected


def test_build_utterance_entry():
    interp = Interpretation("HomeAutomation", "TurnOnApplianceIntent", "テレビつけて", {"ActionTrigger":"つけて", "DeviceType":"テレビ"})

    expected = [
        "HomeAutomation",
        "TurnOnApplianceIntent",
        "DeviceType,ActionTrigger",
        "{テレビ|DeviceType}{つけて|ActionTrigger}",
        ",".join(DEFAULT_AVAILABLE_DEVICES)
    ]
    actual = BluGoldenWriterHelper.build_utterance_entry(interp)

    assert actual == expected
