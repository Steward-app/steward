import threading
import time
from absl import logging

from cozify import hub, cloud
from cozify.Error import APIError

class CozifyDevices(object):
    def __init__(self, interval=10):
        self.interval = interval
        self.name = 'not connected'
        self.rooms = 'no room'
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        try:
            # Check connectivity and have it auto-renewed if it's deemed time to do so.
            cloud.ping()
            hub.ping()
            # Get and cache all devices.
            self.devicecache = hub.devices()
            self.name = hub.name(hub.default())
            rooms = []
            for device in self.devicecache:
                room = self.devicecache[device]['room']
                if room and room[0] not in rooms:
                    rooms.append(room[0])
            rooms.sort()
            self.rooms = rooms
        except APIError as e:
            if e.status_code == 401: # auth failed
                logging.warning('Auth failed, this should not happen.')
            else:
                raise # we ignore all other APIErrors and let it burn to the ground
        time.sleep(self.interval)
