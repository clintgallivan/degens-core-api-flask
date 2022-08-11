from datetime import datetime as dt
import pytz
import json
import os


arr = os.listdir()
print(arr)
f = open("./src/functions/token-timeseries.json")
data = json.load(f)
# print(data)


def transform(ex_timestamp):
    asDateTime = dt.strptime(ex_timestamp, "%m-%d-%YT%H:%M:%S")
    asInt = asDateTime.timestamp()
    asRounded = int(round(asInt * 1000))
    obj = {"$date": {
        "$numberLong": str(asRounded)
    }}
    return obj


token_count = 0
for tokenObj in data:
    historical_count = 0
    for historicalItem in tokenObj["historical"]:
        ex_timestamp = historicalItem["timestamp"]
        if type(ex_timestamp) == str:
            transform(ex_timestamp)
            # print(data[token_count]["historical"][historical_count]["timestamp"])
            data[token_count]["historical"][historical_count]["timestamp"] = transform(
                ex_timestamp)
            # print(data[token_count]["historical"][historical_count]["timestamp"])
            historical_count = historical_count + 1
        else:
            historical_count = historical_count + 1
            continue
    token_count = token_count + 1

json_object = json.dumps(data, separators=(',', ':'))
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
