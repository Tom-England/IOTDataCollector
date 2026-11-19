import json, io, time, os
from ultralytics import YOLO
from PIL import Image
import numpy

class DataHandlerCamera:
    def __init__(self, client):
        self.frames = {}
        self.client = client
    
    def get_frame(self, client, userdata, msg):
        data = json.loads(msg.payload)
        for key in data.keys():
            self.frames[key] = data[key]
            print("Got frame")
            bio = io.BytesIO(bytes(data[key]))
            img = Image.open(bio)

            count = self.identify(img, key)
            print("Loading image")
            annotated_image_data = self.load_image(key)
            print(f"Loaded {len(annotated_image_data["image"])} bytes")
            print("Sending")
            data_to_send = {key: {"image": annotated_image_data["image"], "count": count}}
            self.client.publish_message("TASK5/IMAGE", data_to_send)
            print("Deleting image")
            self.clean_up_image(key)

    def identify(self, image, save_name):
        # Load a pretrained YOLO11n model
        model = YOLO("yolo11n.pt")

        # Run inference on the sample image
        # classes used to only identify vehicles
        results = model(image,classes=[1,2,3,5,7])

        # Display the annotated results
        results[0].save(f"{save_name}.jpeg")
        return len(results[0].boxes.xyxy) # Count of identified vehicles

    def load_image(self, save_name):
        img = Image.open(f"{save_name}.jpeg")
        byte_arr = io.BytesIO()
        img.save(byte_arr, format='jpeg')
        byte_arr = byte_arr.getvalue()
        return {"image": list(byte_arr)}

    def clean_up_image(self,save_name):
        os.remove(f"{save_name}.jpeg")