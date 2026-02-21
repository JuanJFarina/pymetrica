from collections.abc import Callable
from cProfile import Profile
from functools import wraps
from io import StringIO
from pstats import SortKey, Stats
from typing import ParamSpecArgs, ParamSpecKwargs, TypeVar

from .logging import log

profiler = Profile()

T = TypeVar("T")


def run_profiler(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: ParamSpecArgs, **kwargs: ParamSpecKwargs) -> T:
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        temp_output = StringIO()
        stats = Stats(profiler, stream=temp_output).sort_stats(SortKey.CUMULATIVE)
        stats.print_stats(7)
        log.debug(temp_output.getvalue())
        return result

    return wrapper
