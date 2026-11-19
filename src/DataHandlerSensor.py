import json, io, time, os
from datetime import datetime
import matplotlib.pyplot as plt
from ml_engine import MLPredictor
import pandas as pd
FRAMES_REQURIED = 100#8706

class DataHandlerSensor:
    def __init__(self, client):
        self.frames = {}
        self.sets = []
        self.client = client
    
    def get_frame(self, client, userdata, msg):
        data = json.loads(msg.payload)
        self.frames = self.frames | data
        self.sets.append(list(data.keys()))
        keys = len(self.frames.keys())
        print(f"Frames contains {keys} keys")
        if keys >= FRAMES_REQURIED:
            self.process()
            #self.frames = {}
            #self.sets = []

    def process(self):
        keys = list(self.frames.keys())
        keys.sort()
        keys_to_validate = keys[-2:]
        valid = True
        if self.frames[keys_to_validate[0]] == 2.925 and self.frames[keys_to_validate[1]] == 3.295:
            valid = True
        if valid:
            print("Validation Passed")
            avg_values = self.avg_over_ten_minutes()
            self.pretty_print_avg_values(avg_values)
            self.display_graph(avg_values)
            self.predict(avg_values)

        else:
            print("Not valid")
            print(self.frames[keys_to_validate[0]])
            print(self.frames[keys_to_validate[1]])
        
    def avg_over_ten_minutes(self):
        values = {}
        for set_of_timestamps in self.sets:
            set_of_timestamps.sort()
            avg_value = 0
            for timestamp in set_of_timestamps:
                avg_value += self.frames[timestamp]
            avg_value = avg_value / len(set_of_timestamps)
            values[set_of_timestamps[0]] = avg_value

        return values

    def prettify_time(self, timestamp):
        return datetime.utcfromtimestamp(int(timestamp)/1000).strftime("%Y-%m-%d %H:%M:%S")

    def pretty_print_avg_values(self, avg_values):
        for key in avg_values.keys():
            pretty_time = self.prettify_time(key)
            print(f"{pretty_time}: {avg_values[key]}")
    
    def display_graph(self, avg_values):
        sorted_keys = list(avg_values.keys())
        sorted_keys.sort()
        x = [self.prettify_time(ts) for ts in sorted_keys]
        y = [avg_values[key] for key in sorted_keys]
        df = pd.DataFrame({"Times" : x, "Avg Values": y})
        print("Drawing graph")
        df.plot(x="Times", y="Avg Values", kind="line", title='Task 3')
        plt.xticks(rotation=20)
        print("Saving")
        plt.savefig("/usr/local/source/graphs/task3output.jpg")
        plt.close()

    def predict(self, avg_values):
        sorted_keys = list(avg_values.keys())
        sorted_keys.sort()
        panda_data_frame_data = {"Timestamp": [self.prettify_time(ts) for ts in sorted_keys], "Value": [avg_values[key] for key in sorted_keys]}
        pm25_df = pd.DataFrame(data=panda_data_frame_data)
        predictor = MLPredictor(pm25_df)
        predictor.train()
        forecast = predictor.predict()

        fig = predictor.plot_result(forecast)
        fig.savefig("/usr/local/source/graphs/task3output_prediction.jpg")