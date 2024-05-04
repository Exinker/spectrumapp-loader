from abc import ABC, abstractmethod

from spectrumapp_loader.dumps import Dump
from spectrumapp_loader.types import FilePath


class AbstractLoader(ABC):

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    @abstractmethod
    def load(self, filepath: FilePath) -> Dump:
        raise NotImplementedError
