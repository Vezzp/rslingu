import itertools
import re
from pathlib import Path
from typing import Final, Optional

import typer

from . import defs
from .utils import render_template

__here__ = Path(__file__).resolve()

INPUT_RE = re.compile(r"\\input\{([\w|\.]+)\}")
SRC_DPATH: Final[Path] = __here__.parents[1].joinpath("src")
SRC_FPATH: Final[Path] = SRC_DPATH.joinpath("main.sty")
DST_FPATH: Final[Path] = __here__.parents[1].joinpath("rslingu.sty")
VERSION_RE = re.compile(
    r"(?P<exp>\\tl_const:Nn\s*\\c_rslingu_version_tl)\s*\{\s*(?P<ver>[\.\d]+)\s*\}"
)


version_app = typer.Typer(name="version")

app = typer.Typer(name="package")
app.add_typer(version_app)


@version_app.command("show")
def version_show_handler() -> None:
    """"""
    typer.echo(find_version())


@version_app.command("change")
def version_change_handler(version: str) -> None:
    """"""
    change_version(version)


@app.command("build")
def build_handler(version: Optional[str] = None) -> None:
    """"""
    if version is not None:
        change_version(version)

    content_parts = []
    for line in SRC_FPATH.read_text().splitlines():
        if (match := INPUT_RE.match(line)) is None:
            content_parts.append(line)

        else:
            fname = match.group(1)
            content_parts.append(SRC_DPATH.joinpath(fname).read_text())

    text = "\n".join(content_parts)
    text = _render_color_codegen(text)
    text = _render_pos_codegen(text)

    DST_FPATH.write_text(text)


def find_version() -> str:
    """"""
    out = VERSION_RE.findall(SRC_DPATH.joinpath("main.sty").read_text())[0][-1]
    return out


def change_version(version: str) -> None:
    """"""
    SRC_FPATH.write_text(
        VERSION_RE.sub(rf"\g<exp> {{ {version} }}", SRC_FPATH.read_text())
    )


def _render_color_codegen(text: str) -> str:
    """"""
    out = render_template(
        "color_codegen",
        "\n".join(
            (
                rf"\\g__rslingu_color_codegen_cs:nn {{ {name:10} }} {{ {hexcolor:6} }}"
                for name, hexcolor in itertools.chain(
                    defs.SYNTAX_COLOR_MAPPING.items(),
                    defs.MORPHOLOGY_COLOR_MAPPING.items(),
                )
            )
        ),
        text,
    )
    return out


def _render_pos_codegen(text: str) -> str:
    """"""
    repl_parts = []
    for pos_contraction in defs.POS_CONTRACTIONS:
        en_full_name = pos_contraction["en_full_name"]

        pos_parts = [f"% {pos_contraction['ru_full_name'].capitalize()}"]
        for lang, contraction in pos_contraction["lang_mapping"].items():
            pos_part = (
                r"\\l_set_pos_acr_codegen_cs:nnn "
                f"{{ {en_full_name:13} }} {{ {lang:8} }} {{ {contraction:10} }}"
            )
            pos_parts.append(pos_part)

        pos_parts.append(
            rf"\\l_rslingu_syntax_make_speech_part_cmd_cs:n {{ {en_full_name} }}"
        )
        pos_parts.append("")

        repl_parts.append("\n".join(pos_parts))

    out = render_template("pos_codegen", "\n".join(repl_parts), text)

    return out


if __name__ == "__main__":
    app()
