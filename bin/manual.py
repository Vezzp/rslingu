import shlex
import subprocess
import functools
import textwrap
from pathlib import Path
from typing import Dict, Final, Literal

import typer

from . import defs
from .package import find_version
from .utils import divide, render_template, compose

__here__ = Path(__file__).resolve()

MANUAL_DPATH: Final[Path] = __here__.parents[1].joinpath("manual")
PACKAGE_MANUAL_FPATH: Final[Path] = MANUAL_DPATH.joinpath("manual.sty")


app = typer.Typer(name="manual")


@app.callback()
def callback() -> None:
    """"""
    pass


@app.command("build")
def build_handler(dev: bool = True) -> None:
    """"""
    command = shlex.join(
        [
            "pdflatex",
            "-synctex=1",
            "-interaction=nonstopmode",
            "-shell-escape",
            "manual.tex",
        ]
    )

    render_compose = compose(
        functools.partial(_render_dev_watermark, dev=dev),
        _render_morphology_color_table,
        _render_syntax_color_table,
        _render_available_pos_langs,
    )
    for chapter_fpath in MANUAL_DPATH.joinpath("_templated_chapters").glob("*.tex"):
        text = chapter_fpath.read_text()
        rendered_text = render_compose(text)
        MANUAL_DPATH.joinpath("chapters", chapter_fpath.name).write_text(rendered_text)

    subprocess.call(command, shell=True, cwd=MANUAL_DPATH)


def _render_dev_watermark(text: str, dev: bool) -> str:
    """"""
    if dev:
        print("Rendered template")
        out = render_template(
            "dev_watermark",
            textwrap.dedent(
                rf"""
                \\usepackage{{background}}
                \\backgroundsetup{{
                    position=current~page.west,
                    angle=90,
                    vshift=-5mm,
                    opacity=1,
                    scale=3,
                    contents=Черновик~версии~{find_version()},
                }}
                """
            ),
            text,
        )
    else:
        out = text

    return out


def _render_syntax_color_table(text: str) -> str:
    """"""
    return _render_color_table_impl(
        text, "morphology", "Цвета~по~умолчанию~для~морфемного~разбора"
    )


def _render_morphology_color_table(text: str) -> str:
    """"""
    return _render_color_table_impl(
        text, "syntax", "Цвета~по~умолчанию~для~синтаксического~разбора"
    )


def _render_color_table_impl(
    text: str, table_type: Literal["syntax", "morphology"], caption: str
) -> str:
    """"""
    num_cols = 2
    delimeter = " & "

    color_mapping: Dict[str, str] = getattr(defs, f"{table_type.upper()}_COLOR_MAPPING")

    q, r = divmod(len(color_mapping), num_cols)
    num_chunks = q + int(r != 0)

    rows = [delimeter.join(["Имя элемента & Код цвета"] * num_cols)]

    for color_group in divide(color_mapping.items(), num_chunks):
        group_parts = []
        for element_name, color_hex in color_group:
            group_parts.append(
                (
                    rf"{element_name} & "
                    rf"{{ \\color[HTML]{{{color_hex}}} \\textbf{{{color_hex}}} }}"
                )
            )

        rows.append(delimeter.join(group_parts))

    joint_rows = r"\\\\\\midrule\n".join(rows)
    repl = textwrap.dedent(
        rf"""
        \\renewcommand{{\\arraystretch}}{{1.125}}
        \\begin{{table}}[ht!]
            \\centering
            \\small
            \\begin{{tabular}}{{@{{}}{'l' * num_cols * 2}@{{}}}}
                \\toprule
                {joint_rows}
                \\\\\\bottomrule
            \\end{{tabular}}

            \\caption{{{caption}}}
        \\end{{table}}
        """
    )

    out = render_template(f"{table_type}_color_table", repl, text)

    return out


def _render_available_pos_langs(text: str) -> str:
    """"""
    table_content = "\n".join(
        [
            rf"{ru_name} & {en_name} \\\\\\midrule"
            for en_name, ru_name in defs.POS_LANGS.items()
        ]
    )
    repl = textwrap.dedent(
        rf"""
        \\begin{{table}}[ht!]
            \\centering
            \\begin{{tabular}}{{@{{}}ll@{{}}}}
                \\toprule
                Язык & \\manArg[язык] \\\\\\midrule
                {table_content}
                \\bottomrule
            \\end{{tabular}}
            \\caption{{Доступные языки для локализации частеречных команд}}
        \\end{{table}}
        """
    )
    out = render_template("available_pos_langs", repl, text)

    return out


if __name__ == "__main__":
    app()
