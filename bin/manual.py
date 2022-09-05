from __future__ import annotations

import enum
import shlex
import shutil
import subprocess
import textwrap
from pathlib import Path
from typing import Dict, Literal

import typer

from . import defs
from .package import build_handler as build_package_handler
from .utils import compose, divide, render_template


app = typer.Typer(name="manual")


class Engine(str, enum.Enum):
    XELATEX = "xelatex"
    PDFLATEX = "pdflatex"


@app.callback()
def callback() -> None:
    pass


@app.command("build")
def build_handler(
    dev: bool = typer.Option(
        True, "-d", "--dev", help="Whether to add development watermark"
    ),
    engine: Engine = typer.Option(
        "xelatex", "-e", "--engine", help="TeX engine to build manual with"
    ),
    dst_dpath: Path = typer.Option(
        defs.MANUAL_DPATH,
        "-o",
        "--output",
        resolve_path=True,
        help="Path to store artifacts of package's manual",
    ),
) -> None:
    command = shlex.join(
        [
            engine.value,
            "-synctex=1",
            "-interaction=nonstopmode",
            "-shell-escape",
            "manual.tex",
        ]
    )

    dst_dpath = dst_dpath.joinpath("manual")
    dst_dpath.mkdir(parents=True, exist_ok=True)

    shutil.copy2(defs.MANUAL_DPATH.joinpath("manual.tex"), dst_dpath)
    shutil.copytree(
        defs.MANUAL_DPATH.joinpath("fonts"),
        dst_dpath.joinpath("fonts"),
        dirs_exist_ok=True,
    )

    build_package_handler(dst_dpath=dst_dpath)

    src_sty_fpath = defs.MANUAL_DPATH.joinpath("manual.sty")
    dst_sty_fpath = dst_dpath.joinpath(src_sty_fpath.relative_to(defs.MANUAL_DPATH))
    dst_sty_fpath.write_text(_render_dev_watermark(src_sty_fpath.read_text(), dev=dev))

    render_manual = compose(
        _render_morphology_color_table,
        _render_syntax_color_table,
        _render_available_pos_langs,
    )
    for src_chapter_fpath in defs.MANUAL_DPATH.joinpath("chapters").glob("*.tex"):
        rendered_text = render_manual(src_chapter_fpath.read_text())
        dst_chapter_fpath = dst_dpath.joinpath(
            src_chapter_fpath.relative_to(defs.MANUAL_DPATH)
        )
        dst_chapter_fpath.parent.mkdir(parents=True, exist_ok=True)
        dst_chapter_fpath.write_text(rendered_text)

    subprocess.call(command, shell=True, cwd=dst_dpath)


def _render_dev_watermark(text: str, dev: bool) -> str:
    if dev:
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
                    contents=Черновик~версии~{defs.RSLINGU_VERSION},
                }}
                """
            ),
            text,
        )
    else:
        out = text

    return out


def _render_syntax_color_table(text: str) -> str:
    return _render_color_table_impl(
        text, "morphology", "Цвета~по~умолчанию~для~морфемного~разбора"
    )


def _render_morphology_color_table(text: str) -> str:
    return _render_color_table_impl(
        text, "syntax", "Цвета~по~умолчанию~для~синтаксического~разбора"
    )


def _render_color_table_impl(
    text: str, table_type: Literal["syntax", "morphology"], caption: str
) -> str:
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
                Язык & \\rsArg[язык] \\\\\\midrule
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
