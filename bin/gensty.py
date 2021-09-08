import re
from pathlib import Path
from typing import Final


# ====================
# Setup
# ====================


__here__ = Path(__file__).resolve().parent

INPUT_RE = re.compile(r"\\input\{([\w|\.]+)\}")
SOURCE_DIRPATH: Final[Path] = __here__.parent.joinpath("src/")
SOURCE_FILEPATH: Final[Path] = SOURCE_DIRPATH.joinpath("main.sty")
TARGET_FILEPATH: Final[Path] = __here__.parent.joinpath("rslingu.sty")


# ====================
# Main
# ====================


def main() -> None:
    """"""
    with SOURCE_FILEPATH.open() as main_fin:
        lines = []
        for line in main_fin:
            if (match := INPUT_RE.match(line)) is None:
                lines.append(line)

            else:
                filename = match.group(1)
                with SOURCE_DIRPATH.joinpath(filename).open() as aux_fin:
                    lines.append(aux_fin.read())

    rslingu_content = "\n".join(lines)
    with TARGET_FILEPATH.open("w") as fout:
        fout.write(rslingu_content)


if __name__ == "__main__":
    main()
