from DataHandlerSensor import DataHandlerSensor
import json

from ai_edge_litert.compiled_model import CompiledModel, HardwareAccelerator
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

class DataHandlerSensorWithPrediction():

    def __init__(self, model, client):
        self.model = model
        self.client = client
        self.frames = {"GREEN":0, "YELLOW":0, "RED":0}
        self.generated_graph = False

    def predict(self, value):
        output_buffers = self.model.create_output_buffers(0)
        input_buffers = self.model.create_input_buffers(0)

        input_data = np.array([value], dtype=np.float32)
        input_buffers[0].write(input_data)

        self.model.run_by_index(0, input_buffers, output_buffers)

        output = output_buffers[0].read(3, np.float32)
        return output
    
    def assign_category(self, values):
        if (values[0] > values[1] and values[0] > values[2]):
            return "GREEN"
        if (values[1] > values[0] and values[1] > values[2]):
            return "YELLOW"
        if (values[2] > values[1] and values[2] > values[0]):
            return "RED"

    def get_frame(self, client, userdata, msg):
        data = json.loads(msg.payload)
        FRAMES_REQURIED = 8706
        
        for key in data.keys():
            #print(data[key])
            output = self.predict(data[key])
            category = self.assign_category(output)
            print(f"{key}: {data[key]} - {category}")
            output_obj = {key: [data[key],category]}
            self.frames[category] += 1
            self.client.publish_message("TASK5/GROUPS", output_obj)
        if sum(self.frames.values()) >= FRAMES_REQURIED and not self.generated_graph:
            self.gen_graph()
            self.generated_graph = True
    
    def gen_graph(self):
        x = list(self.frames.keys())
        y = list(self.frames.values())
        plt.bar(x, y, color=["green", "yellow", "red"])
        plt.savefig("/usr/local/source/graphs/task4_graph.jpg")

