from copy import deepcopy
from itertools import islice, tee
from typing import Any, Iterable


def partition(it: Iterable[Any], i: int) -> tuple[Iterable[Any], Iterable[Any]]:
    "Partition an iterable at an index `i`."
    it1, it2 = tee(deepcopy(it))
    return islice(it1, 0, i, 1), islice(it2, i, None, 1)


def to_tm_string(it: Iterable[str]) -> str:
    ret = "".join(it)
    return ret if ret else "⊔"


def to_dfa_string(it: Iterable[str]) -> str:
    ret = "".join(it)
    return ret if ret else "λ"
