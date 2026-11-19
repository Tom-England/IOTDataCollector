from ai_edge_litert.compiled_model import CompiledModel, HardwareAccelerator
import pandas as pd
import numpy as np

from MQTTService import MQTTService
from DataHandlerSensorWithPrediction import DataHandlerSensorWithPrediction



def main():


    mqtt_client = MQTTService()
    model = CompiledModel.from_file("output.tflite", HardwareAccelerator.CPU)

    dh_sensor = DataHandlerSensorWithPrediction(model,mqtt_client)

    dh_sensor.client.connect_with_message(dh_sensor.get_frame)
    dh_sensor.client.start_receive_loop("SENSOR")



if __name__ == "__main__":
    main()