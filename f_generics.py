from ast import Str
from functools import partial, reduce, singledispatch
from typing import Any, Callable, Iterable
from collections.abc import Sequence


@singledispatch
def fcompose(*funcs):
    """Compose 'funcs' into single pipeline."""
    return partial(reduce, lambda arg, func: func(arg), funcs)

@fcompose.register
def starfcompose(funcs: Sequence):
    return partial(reduce, lambda arg, func: func(arg), funcs)




    