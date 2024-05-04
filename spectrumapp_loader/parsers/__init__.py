from typing import TypeAlias

from .binary_parser import BinaryParser


__all__ = [
    'BinaryParser',
    'Parser',
]


Parser: TypeAlias = BinaryParser
