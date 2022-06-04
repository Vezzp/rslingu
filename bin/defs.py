from typing import Dict, TypedDict


class PoSContraction(TypedDict):
    """"""

    en_full_name: str
    ru_full_name: str
    lang_mapping: Dict[str, str]


MORPHOLOGY_COLOR_MAPPING = {
    "suffix": "7fdb6a",
    "prefix": "f44747",
    "root": "eedc31",
    "postfix": "966842",
    "ending": "0e68ce",
    "base": "990066",
}

SYNTAX_COLOR_MAPPING = {
    "subject": "673ab7",
    "predicate": "e81e62",
    "attribute": "2196f3",
    "adverbial": "009688",
    "object": "ffa500",
}


POS_LANGS = ("russian", "ukranian")


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
