import fileinput
import json
import pandas as pd
import numpy as np
import datetime
import time 

input_filelocation = "<filelocation>"

with open(input_filelocation + 'input.json', 'r') as f:
    d = json.load(f)
    
df = pd.json_normalize(d)

df = df.drop('songs', 1)


df2 = pd.json_normalize(d,'songs','artist')
df2['artist'] = df2.artist.map(lambda x: x['name'])


df3=df2.merge(df, left_on='artist', right_on='artist.name',how="inner")
df3 = df3.drop('artist.name',1)
df3 = df3.rename(index=str, columns={"record.name": "record_name", "record.genre": "genre", "record.release_date": "release_date"})
df3[["release_date"]] = df3[["release_date"]].apply(pd.to_datetime)
#Transform record release date to UNIX timestamp
df3['epochtime'] = df3.release_date.map(lambda x: (x - pd.Timestamp("1970-01-01")).total_seconds())
#Transform song duration to seconds
df3["duration_min"] = df3["duration"].str.split(':').str[0]
df3["duration_sec"] = df3["duration"].str.split(':').str[1]
df3["duration_converted"] = df3.apply(lambda x: int(x.duration_min) * 60 + int(x.duration_sec), axis=1)



#Filter out records with genre that is not specified in output schema 
df3 = df3.loc[df3['genre'].isin(['ROCK','POP','DANCE'])]

group_df = df3.groupby('record_name').agg(song_duration=('duration_converted', 'sum'), song_count=('duration_converted', 'count')).reset_index()
final_df = df3.merge(group_df)

#Determine record type

conditions  = [ final_df['song_count'] == 1, (final_df['song_count'] > 1) & (final_df['song_duration'] < 1800), (final_df['song_count'] > 1) & (final_df['song_duration'] > 1800) ]
choices     = [ 'SINGLE', 'EP', 'ALBUM' ]

final_df['record_type'] = np.select(conditions, choices, default=np.nan)



json_output = final_df.to_json(orient = "records")
print(json_output)