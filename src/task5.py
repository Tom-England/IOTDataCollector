import pandas as pd
import numpy as np

from MQTTService import MQTTService
from DataCollator import DataCollator



def main():
    mqtt_client = MQTTService()

    dc = DataCollator(mqtt_client)

    dc.client.connect_with_message(dc.get_frame)
    dc.client.start_receive_loop("TASK5/#")



if __name__ == "__main__":
    main()