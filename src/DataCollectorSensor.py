from DataCollectorAbstract import DataCollectorAbstract
from requests import get
import json


class DataCollectorSensor(DataCollectorAbstract):
    def __init__(self):
        self.url = "http://smartcam.uo.ncl.ac.uk:8001/sensor"
        self.master_result_set = {}

    def collect(self):
        result_raw = get(self.url)
        result_json = json.loads(result_raw.text)
        result_set = []
        for result in result_json:
            #print(result.keys())
            if (result["Variable"] == "PM2.5"):
                result_set.append(result)
        return result_set

    def process(self, data):
        new_items = 0
        outliers = 0 
        existing_timestamps = list(self.master_result_set.keys())
        for datum in data:
            if datum["Timestamp"] not in existing_timestamps:
                if (datum["Value"] > int(50)):
                    print(f"Detected Outlier for timestamp: {datum["Timestamp"]}")
                    print(datum)
                    outliers += 1
                    continue
                self.master_result_set[datum["Timestamp"]] = datum["Value"]
                new_items += 1
        
        print(f"Added {new_items} new data points to master result set")
        print(f"Detected {outliers} unusual data points to exclude")
    
    def flush(self):
        self.master_result_set.clear()
