from DataCollectorAbstract import DataCollectorAbstract
from requests import get
import json
import time

class DataCollectorCamera(DataCollectorAbstract):
    def __init__(self):
        self.url = "http://smartcam.uo.ncl.ac.uk:8001/camera"
        self.master_result_set = {}

    def collect(self):
        result_raw = get(self.url)
        return result_raw.text

    def process(self, data):
        timestamp = time.gmtime()
        new_items = 0
        self.master_result_set[timestamp] = data
        new_items += 1
        
        print(f"Added {new_items} new data points to master result set")
    