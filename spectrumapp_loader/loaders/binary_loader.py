import pickle

from spectrumapp_loader.dumps import BinaryDump
from spectrumapp_loader.types import FilePath

from .loader import AbstractLoader


class BinaryLoader(AbstractLoader):
    """Loader for dumps from [ExternalDumper.exe](https://github.com/Exinker/external-dumper)."""

    def __init__(self, verbose: bool = False):
        super().__init__(verbose=verbose)

    def load(self, filepath: FilePath) -> BinaryDump:
        assert filepath.endswith('.pkl'), '`BinaryLoader` supports only .pkl files!'

        with open(filepath, 'rb') as file:
            data = pickle.load(file)

        return BinaryDump.factory(
            data=data,
            verbose=self.verbose,
        ).create()
