# -*- coding: utf-8 -*-

import csv
import json
import traceback
from argparse import ArgumentParser
from logging import getLogger, INFO, StreamHandler, Formatter
from .interpretation import Interpretation
from .blugolden_writerhelper import BluGoldenWriterHelper, BLUGOLDEN_ATTR_DELIMITER

logger = getLogger(__name__)
logger.setLevel(INFO)

stream_handler = StreamHandler()
stream_handler.setLevel(INFO)
formatter = Formatter("%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def load_uttr_json(path, lang) -> list:
    """
    This function load a file written in NIF and build a list of interpretation instances.

    :param path: A path to a file.
    :param lang: A language of texts of given file.
    :return: A list of interpretation instances.
    :rtype: list
    """

    interp_list = []
    try:
        with open(path, "r") as f:
            json_obj = json.load(f)
            logger.info("start loading...: %s", path)

            for item in json_obj:
                utterance = item["utteranceText"]
                domain = item["interpretation"]["value"]["domain"]["value"]
                intent = item["interpretation"]["value"]["type"]
                slot_values = {}
                for entity_property in item["interpretation"]["value"]["entityProperties"]:
                    property_value_item = entity_property["propertyValues"][0]
                    property_value_item_surface_form = property_value_item["surfaceForm"]
                    slot_token_value_list = []
                    for token in property_value_item_surface_form["tokens"]:
                        slot_token_value_list.append(token["value"])
                        token_string = " ".join(slot_token_value_list)
                        slot_values[entity_property["name"]] = token_string.replace(" ", "")

                logger.info("load: %s, %s, %s, %s", domain, intent, utterance, slot_values)
                interp = Interpretation(domain, intent, utterance, slot_values)
                if lang:
                    interp.set_lang(lang)
                interp_list.append(interp)

    except IOError:
        print(traceback.format_exc())

    return interp_list


def save_blugoldens(interp_list: list):
    """
    This function extract an interpretation object, and save it to a file in BluGoldens format.

    A file name and path is determined by BluGoldensWriterHelper object.
    A new line for an interpretation object will be added when an intended file exists.
    The intended file and its directory will be created when it does not exist.

    :param interp_list: The list of interpretation instances to be extracted.
    :return: None.
    """

    for interp in interp_list:
        entry = BluGoldenWriterHelper.build_utterance_entry(interp)
        try:
            path_obj = BluGoldenWriterHelper.build_blugolden_path(interp)
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            path_obj.touch()

            with path_obj.open(mode="a") as f:
                logger.info("start saving...: %s", path_obj.absolute())
                writer = csv.writer(f, delimiter=BLUGOLDEN_ATTR_DELIMITER)
                writer.writerow(entry)
                logger.info("save: %s", entry)

        except IOError:
            print(traceback.format_exc())


def main():
    parser = ArgumentParser()
    parser.add_argument("--json", help="Provide path to input json.", required=True)
    parser.add_argument("--lang", help="Instruct language to interpret input json. e.g. ja, es, ...etc.")
    args = parser.parse_args()

    interp_list = load_uttr_json(args.json, args.lang)
    save_blugoldens(interp_list)


if __name__ == "__main__":
    main()
