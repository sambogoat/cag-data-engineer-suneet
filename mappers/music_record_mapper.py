from abc import ABC

import pandas as pd

from .validating_mapper import ValidatingMapper

class MusicRecordMapper(ValidatingMapper, ABC):

    def validated_map(self, df: pd.DataFrame) -> pd.DataFrame:
        # Implement logic here
        
        return df

    def __init__(self, input_schema, output_schema):
        super().__init__(input_schema=input_schema, output_schema=output_schema)
