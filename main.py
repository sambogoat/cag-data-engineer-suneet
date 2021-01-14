import pandas as pd

from os.path import abspath
from mappers.music_record_mapper import MusicRecordMapper

mapper = MusicRecordMapper(abspath('./data/schemas/input-schema.json'), abspath('./data/schemas/output-schema.json'))

output = mapper.map(pd.read_json(abspath('./data/input.json'), typ="series"))
expected_output = pd.read_json(abspath('./data/expected-output.json'), typ="series")

print(output.eq(expected_output))