import contextlib
import re
import subprocess
from pathlib import Path
import textwrap
from typing import Final, Optional

import typer

from .package import find_version

__here__ = Path(__file__).resolve()

MANUAL_DPATH: Final[Path] = __here__.parents[1].joinpath("manual")
PACKAGE_MANUAL_FPATH: Final[Path] = MANUAL_DPATH.joinpath("manual.sty")
DEV_WATERMARK_RE = re.compile(r"% template: {{ dev_watermark }}")


app = typer.Typer(name="manual")


@app.callback()
def callback() -> None:
    """"""
    pass


@app.command("build")
def build_handler(dev: bool = True) -> None:
    """"""
    if dev:
        dev_watermark = textwrap.dedent(
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
        )

        new_package_manual_content = DEV_WATERMARK_RE.sub(
            dev_watermark, PACKAGE_MANUAL_FPATH.read_text()
        )

    else:
        new_package_manual_content = None

    command = " ".join(
        [
            "pdflatex",
            # "-halt-on-error",
            # "-synctex=1",
            # "-interaction=batchmode",
            "-shell-escape",
            "manual.tex",
            "&&",
            "mv",
            "manual.pdf",
            "..",
        ]
    )

    with chcontent(PACKAGE_MANUAL_FPATH, new_package_manual_content):
        subprocess.call(command, shell=True, cwd=MANUAL_DPATH)


@contextlib.contextmanager
def chcontent(fpath: Path, new_package_manual_content: Optional[str] = None):
    """"""
    if new_package_manual_content is None:
        yield

    else:
        old_content = fpath.read_text()
        try:
            fpath.write_text(new_package_manual_content)
            yield

        finally:
            fpath.write_text(old_content)


if __name__ == "__main__":
    app()
