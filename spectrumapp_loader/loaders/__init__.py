from typing import TypeAlias

from .binary_loader import BinaryLoader


__all__ = [
    'BinaryLoader',
    'Loader',
]


Loader: TypeAlias = BinaryLoader
