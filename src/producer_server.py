from kafka import KafkaProducer
import json
import time


class ProducerServer(KafkaProducer):

    def __init__(self, input_file, topic, **kwargs):
        super().__init__(**kwargs)
        self.input_file = input_file
        self.topic = topic

    # TODO we're generating a dummy data (DONE)
    def generate_data(self):
        with open(self.input_file) as f:
            json_data = json.load(f)
            for row in json_data:
                message = self.dict_to_binary(row)
                # TODO send the correct data (DONE)
                self.send(self.topic, message)
                time.sleep(1)

    # TODO fill this in to return the json dictionary to binary (DONE)
    def dict_to_binary(self, json_dict):
        return json.dumps(json_dict).encode("utf-8")
