# Python ETL Interview

## Prerequisites
- Python 3
- Jupyterlab

## Install dependencies
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

python3 -m ipykernel install --user --name=testenv
```

## Run main
```jupyter-lab main.ipynb```

## Goal
The aim of this task is to write an ETL mapper in music_record_mapper.py that transform the input.json into the expected-output.json. The schema definition is in data/schemas/output-schema.json 


## ETL Requirements
- Transform input data to pass output schema validation
- Transform record release date to UNIX timestamp
- Transform song duration to seconds
- Filter out records with genre that is not specified in output schema
- Determine record type
    - SINGLE - Only 1 song
    - EP - More than 1 song & Total song duration of record is less than 30 minutes
    - ALBUM - More than 1 song & Total song duration of record is equal or more than 30 minutes
- Implement MusicRecordMapper to transform the data