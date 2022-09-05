from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import dotenv

dotenv.load_dotenv()

if (RSLINGU_VERSION_ := os.getenv("RSLINGU_VERSION")) is None:
    raise RuntimeError(f"`RSLINGU_VERSION` is not specified")
else:
    RSLINGU_VERSION = RSLINGU_VERSION_


if (RSLINGU_DATE_ := os.getenv("RSLINGU_DATE")) is None:
    raise RuntimeError(f"`RSLINGU_DATE` env is not specified")
else:
    RSLINGU_DATE = datetime.strptime(RSLINGU_DATE_, "%Y-%m-%d")


SRC_DPATH = Path(__file__).absolute().parent.parent.joinpath("src")
PACKAGE_DPATH = SRC_DPATH.joinpath("package")
assert PACKAGE_DPATH.exists()

MANUAL_DPATH = SRC_DPATH.joinpath("manual")
assert MANUAL_DPATH.exists()


class PoSContraction(TypedDict):
    """"""

    en_full_name: str
    ru_full_name: str
    lang_mapping: dict[str, str]


MORPHOLOGY_COLOR_MAPPING = {
    "suffix": "7FDB6A",
    "prefix": "F44747",
    "root": "EEDC31",
    "postfix": "966842",
    "ending": "0E68CE",
    "base": "990066",
}

SYNTAX_COLOR_MAPPING = {
    "subject": "673AB7",
    "predicate": "E81E62",
    "attribute": "2196F3",
    "adverbial": "009688",
    "object": "FFA500",
}


POS_LANGS = {"russian": "русский", "ukranian": "украинский"}


POS_CONTRACTIONS = [
    PoSContraction(
        en_full_name="noun",
        ru_full_name="существительное",
        lang_mapping={"russian": "сущ.", "ukranian": "ім."},
    ),
    PoSContraction(
        en_full_name="verb",
        ru_full_name="глагол",
        lang_mapping={"russian": "глаг.", "ukranian": "дієсл."},
    ),
    PoSContraction(
        en_full_name="adjective",
        ru_full_name="прилагательное",
        lang_mapping={"russian": "прил.", "ukranian": "прикм."},
    ),
    PoSContraction(
        en_full_name="adverb",
        ru_full_name="наречие",
        lang_mapping={"russian": "нареч.", "ukranian": "присл."},
    ),
    PoSContraction(
        en_full_name="preposition",
        ru_full_name="предлог",
        lang_mapping={"russian": "предлог", "ukranian": "прийм."},
    ),
    PoSContraction(
        en_full_name="conjunction",
        ru_full_name="союз",
        lang_mapping={"russian": "союз", "ukranian": "спол."},
    ),
    PoSContraction(
        en_full_name="pronoun",
        ru_full_name="местоимение",
        lang_mapping={"russian": "мест.", "ukranian": "займ."},
    ),
    PoSContraction(
        en_full_name="particle",
        ru_full_name="частица",
        lang_mapping={"russian": "част.", "ukranian": "част."},
    ),
    PoSContraction(
        en_full_name="numeral",
        ru_full_name="числительное",
        lang_mapping={"russian": "числ.", "ukranian": "числ."},
    ),
    PoSContraction(
        en_full_name="interjection",
        ru_full_name="междометие",
        lang_mapping={"russian": "междом.", "ukranian": "вигук"},
    ),
    PoSContraction(
        en_full_name="participle",
        ru_full_name="причастие",
        lang_mapping={"russian": "прич.", "ukranian": "дієприкм."},
    ),
    PoSContraction(
        en_full_name="transgressive",
        ru_full_name="деепричастие",
        lang_mapping={"russian": "дееприч.", "ukranian": "дієприсл."},
    ),
]

for pos_contraction in POS_CONTRACTIONS:
    if len(diff := set(POS_LANGS).difference(pos_contraction["lang_mapping"])) != 0:
        raise ValueError(
            f"{pos_contraction['en_full_name']} contraction not found for {diff}"
        )
