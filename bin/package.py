import re
from pathlib import Path
from typing import Final, Optional

import typer

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

    DST_FPATH.write_text("\n".join(content_parts))


def find_version() -> str:
    """"""
    out = VERSION_RE.findall(SRC_DPATH.joinpath("main.sty").read_text())[0][-1]
    return out


def change_version(version: str) -> None:
    """"""
    SRC_FPATH.write_text(
        VERSION_RE.sub(rf"\g<exp> {{ {version} }}", SRC_FPATH.read_text())
    )


if __name__ == "__main__":
    app()
