from __future__ import annotations

import functools
import re
from typing import (
    Callable,
    Generator,
    Iterable,
    Iterator,
    Sequence,
    TypeVar,
)


def render_template(name: str, repl: str, text: str) -> str:
    rec = re.compile(rf"{{{{\s*##\s*{name}\s*}}}}")
    out = rec.sub(repl, text)

    return out


_T = TypeVar("_T")


def divide(
    iterable: Iterable[_T], num_chunks: int
) -> Generator[Iterator[_T], None, None]:
    seq = iterable if isinstance(iterable, Sequence) else tuple(iterable)
    q, r = divmod(len(seq), num_chunks)
    stop = 0
    for idx in range(1, num_chunks + 1):
        start = stop
        stop += q + int(idx <= r)
        yield iter(seq[start:stop])


def compose(*fns: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), fns, lambda x: x)
