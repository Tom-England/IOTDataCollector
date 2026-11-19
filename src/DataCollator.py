import json, io, os, requests
from math import floor
from PIL import Image

class Post():
    def __init__(self):
        self.image = None
        self.group = None 
        self.sent_to_dashboard = False
    
    def set_image(self, image):
        self.image = image
        data = list(self.image.values())[0]["image"]
        bio = io.BytesIO(bytes(data))
        img = Image.open(bio)
        img.save("current_image.jpeg")
    
    def set_group(self, group):
        self.group = group

    def send_to_dashboard(self):
        timestamp = list(self.group.keys())[0]
        value = self.group[timestamp][0]
        print(self.group[timestamp])
        quality = self.group[timestamp][1]
        with open("current_image.jpeg", "rb") as f:
            r = requests.post("http://dashboard.cloud.ncl.ac.uk:8000/api/records",
                data={"timestamp": floor(int(timestamp)/1000), "value": float(value), "predicted_quality": quality},
                files={"image": f})
            print(r.json())
    
    def needs_to_send(self):
        return not self.sent_to_dashboard

    def needs(self):
        if self.image == None:
            return "IMAGE"
        if self.group == None:
            return "GROUP"
        else:
            return None

class DataCollator():
    def __init__(self, client):
        self.client = client
        self.grouping_buffer = None
        self.current_post = None

    def get_frame(self, client, userdata, msg):
        #print(msg.topic)
        data = json.loads(msg.payload)
        if msg.topic == "TASK5/IMAGE":
            self.handle_image(data)
        else:
            self.handle_groups(data)
        self.try_send_post()

    def handle_image(self, data):
        ts = list(data.keys())[0]
        print(data[ts]["count"])
        if data[ts]["count"] < 5:
            return

        # Is there a post already started?
        if self.current_post == None:
            # Create a new image
            self.current_post = Post()
            
        # Update or set the image data
        self.current_post.set_image(data)

        # Grab buffered grouping data if any available then clear the buffer
        if self.grouping_buffer != None:
            self.current_post.set_group(self.grouping_buffer)
            self.grouping_buffer = None

        keys = list(data.keys())
        print(f"time: {keys[0]}, vehicles: {data[keys[0]]["count"]}")


    def handle_groups(self, data):
        if self.current_post != None and self.current_post.needs() == "GROUP":
            # Created post has image already and needs group data
            self.current_post.set_group(data)
        else:
            # Current post either already has group data and needs sending
            # or current post somehow doesn't have an image so it'll handle groupings
            # on next handle_image call anyway so just buffer the data for now
            self.grouping_buffer = data

    def try_send_post(self):
        p = self.current_post
        if p == None:
            return
        print(f"Needs sending?: {p.needs_to_send()}, Requires: {p.needs()}")
        if p.needs_to_send() and p.needs() == None:
            # post needs nothing and is requires sending
            print("ATTEMPTING SEND!!!")
            p.send_to_dashboard()
        # Clear out post
        self.current_post = None


