from collections.abc import Sequence
from typing import overload

import numpy as np


@overload
def hex2int(values: Sequence[bytes], dtype: type[bool]) -> Sequence[bool]: ...
@overload
def hex2int(values: Sequence[bytes], dtype: type[int]) -> Sequence[int]: ...
def hex2int(values, dtype=int):
    """Transform `bytes` to `bool` or `int` (by default) optionally."""

    return np.array(
        list(map(lambda x: int.from_bytes(x, byteorder='little'), values)),
        dtype=dtype,
    )
