from typing import TypeAlias

import pandas as pd


# --------        frames        --------
ActiveFrame: TypeAlias = pd.DataFrame
ConcentrationFrame: TypeAlias = pd.DataFrame
IndexFrame: TypeAlias = pd.DataFrame
IntensityFrame: TypeAlias = pd.DataFrame
LineFrame: TypeAlias = pd.DataFrame
ProbeFrame: TypeAlias = pd.DataFrame

Frame: TypeAlias = ActiveFrame | ConcentrationFrame | IndexFrame | IntensityFrame | LineFrame | ProbeFrame


# --------        others        --------
FilePath: TypeAlias = str
