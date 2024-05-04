from spectrumapp_loader.parsers import BinaryParser
from spectrumapp_loader.types import Frame

from .dump import AbstractDump


class FactoryBinaryDump:

    def __init__(self, data: dict, verbose: bool = False):
        self._data = data
        self._verbose = verbose

    def create(self) -> 'BinaryDump':
        return BinaryDump(
            parser=BinaryParser(
                data=self._data,
                verbose=self._verbose,
            ),
        )


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

    @staticmethod
    def factory(*args, **kwargs) -> FactoryBinaryDump:
        return FactoryBinaryDump(*args, **kwargs)
