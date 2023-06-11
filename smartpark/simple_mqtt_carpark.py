
from datetime import datetime

import random
import mqtt_device
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage
from config_parser import parse_config

class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        self.client.loop_forever()
        self._temperature = None

    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        return self._temperature

    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value

        
    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M')
        print(
            (
                f"TIME: {readable_time}, "
                + f"SPACES: {self.available_spaces}, "
                + f"TEMPC: {self.temperature}"
            )
        )
        message = (
            f"TIME: {readable_time}, "
            + f"SPACES: {self.available_spaces}, "
            + f"TEMPC: {self.temperature}"
        )
        self.client.publish('display', message)

    def on_car_entry(self):
        self.total_cars += 1
        self._publish_event()



    def on_car_exit(self):
        self.total_cars -= 1
        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
        # TODO: Extract temperature from payload
        self.temperature = random.choice(range(10, 25))
        if 'exit' in payload:
            self.on_car_exit()
        else:
            self.on_car_entry()


if __name__ == '__main__':
    # config = {'name': "YT-park",
    #           'total-spaces': 130,
    #           'total-cars': 0,
    #           'location': 'L306',
    #           'topic-root': "lot",
    #           'broker': 'localhost',
    #           'port': 1883,
    #           'topic-qualifier': 'entry',
    #           'is_stuff': False
    #           }
    # TODO: Read config from file
    config1 = parse_config()
    car_park = CarPark(config1)
    print("Carpark initialized")
    print("Carpark initialized")
