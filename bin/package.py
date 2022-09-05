from __future__ import annotations

import itertools
import re
import textwrap
from pathlib import Path

import typer

from . import defs
from .utils import compose, render_template

INPUT_RE = re.compile(r"\\input\{([\w|\.]+)\}")

app = typer.Typer(name="package")


@app.callback()
def callback() -> None:
    ...


@app.command("build")
def build_handler(
    dst_dpath: Path = typer.Option(
        ...,
        "-o",
        "--output",
        help="Directory to save package to a file named `rslingu.sty`",
    ),
) -> None:
    dst_fpath = dst_dpath.joinpath("rslingu.sty")
    dst_fpath.parent.mkdir(exist_ok=True, parents=True)

    sty_text: str = compose(_render_release_date, _render_package_version)(
        defs.PACKAGE_DPATH.joinpath("main.sty").read_text()
    )

    package_parts = []
    for line in sty_text.splitlines():
        if (match := INPUT_RE.match(line)) is None:
            package_parts.append(line)

        else:
            fname = match.group(1)
            package_parts.append(defs.PACKAGE_DPATH.joinpath(fname).read_text())

    full_package_text = compose(
        _render_color_codegen, _render_pos_codegen, _render_pos_lang_codegen
    )("\n".join(package_parts))

    dst_fpath.write_text(full_package_text)


def _render_release_date(text: str) -> str:
    out = render_template("release_date", defs.RSLINGU_DATE.strftime("%Y/%m/%d"), text)
    return out


def _render_package_version(text: str) -> str:
    out = render_template("package_version", defs.RSLINGU_VERSION, text)
    return out


def _render_color_codegen(text: str) -> str:
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

        pos_parts.append(rf"\\l_rslingu_pos_codegen_cs:n {{ {en_full_name} }}")
        pos_parts.append("")

        repl_parts.append("\n".join(pos_parts))

    out = render_template("pos_codegen", "\n".join(repl_parts), text)

    return out


def _render_pos_lang_codegen(text: str) -> str:
    langs = ",".join(defs.POS_LANGS)
    out = render_template(
        "pos_lang_codegen",
        textwrap.dedent(
            rf"""
            \\tl_const:Nn \\c__rslingu_default_lang_tl {{ russian }}
            \\seq_const_from_clist:Nn \\c__rslingu_supported_lang_seq {{ {langs} }}
        """
        ),
        text,
    )
    return out


if __name__ == "__main__":
    app()
