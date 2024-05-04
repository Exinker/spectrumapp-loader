from abc import ABC
from typing import TypeAlias

from spectrumapp_loader.parsers import BinaryParser, Parser
from spectrumapp_loader.types import Frame


class FactoryDump:

    def __init__(self, parser: type[Parser]):
        self._parser = parser

    def create(self, data: dict, verbose: bool = False) -> 'Dump':
        return Dump(
            parser=self._parser(
                data=data,
                verbose=verbose,
            ),
        )


class AbstractDump(ABC):
    factory = FactoryDump


class BinaryDump(AbstractDump):

    def __init__(self, parser: BinaryParser):
        self._parser = parser

    @property
    def parser(self) -> BinaryParser:
        return self._parser

    def __getattr__(self, key: str) -> Frame:

        try:
            return self._parser[key]

        except AttributeError:
            raise AttributeError(f'Attribute {repr(key)} is not found!')


Dump: TypeAlias = BinaryDump
