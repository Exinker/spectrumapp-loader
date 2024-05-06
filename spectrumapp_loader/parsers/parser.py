from abc import ABC, abstractmethod

from spectrumapp_loader.types import ActiveFrame, ConcentrationFrame, FilePath, IndexFrame, IntensityFrame, LineFrame


class AbstractParser(ABC, dict):

    def __init__(self, data: dict, verbose: bool = False, *args, **kwargs):
        self.data = data
        self.verbose = verbose

    def __missing__(self, key: str):
        attr = f'_parse_{key}'
        if hasattr(self, attr):
            self[key] = getattr(self, attr)()

            return self[key]

        raise AttributeError(f'Attribute {repr(key)} is not found!')

    @abstractmethod
    def _parse_filepath(self) -> FilePath:
        """Parse dump's filepath."""

        raise NotImplementedError

    @abstractmethod
    def _parse_filename(self) -> str:
        """Parse dump's filename."""

        raise NotImplementedError

    @abstractmethod
    def _parse_active(self) -> ActiveFrame:
        """Parse line's active dataframe.

        Returns
        -------

        Frame with concentration. Frame with index, columns are line's id.

        """

        raise NotImplementedError

    @abstractmethod
    def _parse_concentration(self) -> ConcentrationFrame:
        """Parse concentration dataframe.

        Returns
        -------

        Frame with concentration. Frame with index, columns are line's id.

        """

        raise NotImplementedError

    @abstractmethod
    def _parse_index(self) -> IndexFrame:
        """Parse index dataframe.

        Returns
        -------

        Frame with index (probe_name, parallel_name).

        """

        raise NotImplementedError

    @abstractmethod
    def _parse_intensity(self) -> IntensityFrame:
        """Parse intensity dataframe.

        Returns
        -------

        Frame with intensity. Frame with index, columns are line's id.

        """

        raise NotImplementedError

    @abstractmethod
    def _parse_line(self) -> LineFrame:
        """Parse line dataframe.

        Returns
        -------

        Frame with lines properties. Frame index is lines's id, columns are as follows:

            ==========================  =====  ===================================================
            column                      dtype  description

            id                          int    line id (in Atom's table)
            symbol                      str    chemical symbol
            wavelength                  float  wavelength
            nickname                    str    nickname (symbol + wavelength)
            database_intensity          float  database_intensity
            database_ionization_degree  int    database_ionization_degree
            is_active                   bool   usage line in calculations
            ==========================  ===================================================
        """

        raise NotImplementedError
