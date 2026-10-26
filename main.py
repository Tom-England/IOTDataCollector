from time import sleep
from DataCollectorSensor import DataCollectorSensor

API_CALL_TIMEOUT = 5

def main():
    sensor_data = DataCollectorSensor()
    for i in range(1, 10):
        print("Starting Collection")
        sensor_data.CollectThenProcess()
        sleep(API_CALL_TIMEOUT)

if __name__ == "__main__":
    main()