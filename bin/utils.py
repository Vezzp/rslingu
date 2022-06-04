import contextlib
import re
from pathlib import Path
from typing import Optional


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


def render_template(name: str, repl: str, text: str) -> str:
    """"""
    rec = re.compile(rf"% template: {{{{ {name} }}}}")
    out = rec.sub(repl, text, count=1)

    return out
