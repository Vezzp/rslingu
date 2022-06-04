import contextlib
import re
from pathlib import Path
from typing import Any, Generator, Iterable, Iterator, Optional, Sequence, TypeVar


@contextlib.contextmanager
def chcontent(fpath: Path, new_content: Optional[str] = None):
    """"""
    if new_content is None:
        yield

    else:
        old_content = fpath.read_text()
        try:
            fpath.write_text(new_content)
            yield

        finally:
            fpath.write_text(old_content)


def render_template(name: str, repl: str, text: str) -> str:
    """"""
    rec = re.compile(rf"% template: {{{{ {name} }}}}")
    out = rec.sub(repl, text, count=1)

    return out


_T = TypeVar("_T", bound=Any)


def divide(
    iterable: Iterable[_T], num_chunks: int
) -> Generator[Iterator[_T], None, None]:
    """"""
    seq = iterable if isinstance(iterable, Sequence) else tuple(iterable)
    q, r = divmod(len(seq), num_chunks)
    stop = 0
    for idx in range(1, num_chunks + 1):
        start = stop
        stop += q + int(idx <= r)
        yield iter(seq[start:stop])
