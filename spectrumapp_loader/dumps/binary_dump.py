import numpy as np
import pandas as pd

from spectrumapp_loader.types import ActiveFrame, ConcentrationFrame, Frame, IndexFrame, LineFrame
from spectrumapp_loader.utils import hex2int

from .dump import AbstractDump


class BinaryDumpParser(dict):

    def __init__(self, data: dict, verbose: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = data
        self.verbose = verbose

    def __missing__(self, key: str):
        attr = f'_parse_{key}'
        if hasattr(self, attr):
            self[key] = getattr(self, attr)()

            return self[key]

        raise AttributeError(f'Attribute {repr(key)} is not found!')

    def _parse_active(self) -> ActiveFrame:
        '''Parse line's active dataframe.

        Returns
        -------

        Frame with concentration. Frame with index, columns are line's id.

        '''

        # парсим данные
        def _parse_parallel(probe: dict):
            frame = pd.DataFrame()

            if 'Parallel' in probe.keys():
                for parallel in probe['Parallel']:
                    parallel_name = parallel['ParallelName']

                    keys = []
                    values = []
                    for column in parallel['Column']:
                        keys.append(column['ColumnID'])
                        values.append(column['Active'])

                    frame.loc[parallel_name, keys] = hex2int(values, dtype=bool)

                frame['probe_name'] = probe['ProbeName']
                frame['parallel_name'] = frame.index
                frame = frame.set_index(['probe_name', 'parallel_name'])

            else:
                probe_name = probe['ProbeName']
                raise KeyError(f'Проба \"{probe_name}\" не содержит параллельных!')

            return frame

        frame = pd.DataFrame()
        for probe in self.data['Probe']:

            try:
                frame = pd.concat([frame, _parse_parallel(probe)])

            except KeyError as error:
                if self.verbose:
                    print(error)

        # удалим все столбцы не из списка линий
        frame = frame.drop(
            columns=[column for column in frame.columns if column not in self['line'].index],
            axis=1,
        )

        return frame

    def _parse_concentration(self) -> ConcentrationFrame:
        '''Parse concentration dataframe.

        Returns
        -------

        Frame with concentration. Frame with index, columns are line's id.

        '''

        def _parse_parallel(probe: dict):
            frame = pd.DataFrame()

            if 'Parallel' in probe.keys():
                for parallel in probe['Parallel']:
                    parallel_name = parallel['ParallelName']

                    keys = []
                    values = []
                    for column in parallel['Column']:
                        keys.append(column['ColumnID'])
                        values.append(column['Concentration'])

                    frame.loc[parallel_name, keys] = values

                    break  # у параллельных проб одинаковые концентрации, поэтому хватит и первой параллельной!

                frame['probe_name'] = probe['ProbeName']
            else:
                probe_name = probe['ProbeName']
                raise KeyError(f'Проба \"{probe_name}\" не содержит параллельных!')

            return frame

        frame = pd.DataFrame()
        for probe in self.data['Probe']:

            try:
                frame = pd.concat([frame, _parse_parallel(probe)])

            except KeyError as error:
                if self.verbose:
                    print(error)

        frame['probe_name'] = frame['probe_name'].astype(str)
        frame = frame.set_index('probe_name')

        # удалим все столбцы не из списка линий
        mask = [column not in self['line'].index for column in frame.columns]
        frame = frame.drop(columns=frame.columns[mask], axis=1)

        frame.columns = self['line'].loc[frame.columns, 'symbol']

        # выкинем повторяющиеся chemical elements
        elements = tuple(self['line']['symbol'].unique())

        column = []
        for element in elements:
            column.append([i for i, column in enumerate(frame.columns) if column == element][0])

        frame = frame.iloc[:, column]

        #
        return frame

    def _parse_index(self) -> IndexFrame:
        '''Parse index dataframe.

        Returns
        -------

        Frame with index (probe_name, parallel_name).

        '''

        # парсим данные
        rows = []
        for probe in self.data['Probe']:
            try:
                if 'Parallel' in probe.keys():
                    for parallel in probe['Parallel']:
                        row = (
                            probe['ProbeName'],
                            parallel['ParallelName'],
                        )
                        rows.append(row)

            except KeyError as error:
                if self.verbose:
                    print(f'probe: {probe}\n', error)

        #
        frame = pd.DataFrame(
            rows,
            columns=['probe_name', 'parallel_name'],
        )
        frame = frame.set_index(['probe_name', 'parallel_name'], drop=False)

        return frame

    def _parse_intensity(self) -> Frame:
        '''Parse intensity dataframe.

        Returns
        -------

        Frame with intensity. Frame with index, columns are line's id.

        '''

        # парсим данные
        def _parse_parallel(probe: dict):
            frame = pd.DataFrame()

            if 'Parallel' in probe.keys():
                for parallel in probe['Parallel']:
                    parallel_name = parallel['ParallelName']

                    keys = []
                    values = []
                    for column in parallel['Column']:
                        keys.append(column['ColumnID'])
                        values.append(column['Intensity'])

                    frame.loc[parallel_name, keys] = values

                frame['probe_name'] = probe['ProbeName']
                frame['parallel_name'] = frame.index
                frame = frame.set_index(['probe_name', 'parallel_name'])

            else:
                probe_name = probe['ProbeName']
                raise KeyError(f'Проба \"{probe_name}\" не содержит параллельных!')

            return frame

        frame = pd.DataFrame()
        for probe in self.data['Probe']:

            try:
                frame = pd.concat([frame, _parse_parallel(probe)])

            except KeyError as error:
                if self.verbose:
                    print(error)

        # удалим все столбцы не из списка линий
        frame = frame.drop(
            columns=[column for column in frame.columns if column not in self['line'].index],
            axis=1,
        )

        #
        return frame

    def _parse_line(self) -> LineFrame:
        '''Parse line dataframe.

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
        '''

        # парсим данные
        rows = []
        for line in self.data['Columns'][0]['Column']:
            row = (
                line['ColumnID'],
                line['ElementShortName'],
                line['Wavelength'],
                f"{line['ElementShortName']} {line['Wavelength']}",
                line['DatabaseIntensity'],
                line['DatabaseIonizationDegree'],
                False,
            )
            rows.append(row)

        frame = pd.DataFrame(
            rows,
            columns=['id', 'symbol', 'wavelength', 'nickname', 'database_intensity', 'database_ionization_degree', 'is_active'],
        )
        frame = frame.set_index(['id'], drop=False)

        # fillna
        frame.loc[frame['database_intensity'] == -1, 'database_intensity'] = np.NaN
        frame.loc[frame['database_ionization_degree'] == 0, 'database_ionization_degree'] = np.NaN

        #
        return frame


class FactoryBinaryDump:

    def __init__(self, data: dict, verbose: bool = False):
        self._data = data
        self._verbose = verbose

    def create(self) -> 'BinaryDump':
        return BinaryDump(
            parser=BinaryDumpParser(
                data=self._data,
                verbose=self._verbose,
            ),
        )


class BinaryDump(AbstractDump):

    def __init__(self, parser: BinaryDumpParser):
        self._parser = parser

    @property
    def parser(self) -> BinaryDumpParser:
        return self._parser

    def __getattr__(self, key: str) -> Frame:

        try:
            return self._parser[key]

        except AttributeError:
            raise AttributeError(f'Attribute {repr(key)} is not found!')

    @staticmethod
    def factory(*args, **kwargs) -> FactoryBinaryDump:
        return FactoryBinaryDump(*args, **kwargs)
