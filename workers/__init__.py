import threading

class DataReaderWorker(threading.Thread):
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        
        self.start()
        
    def run(self):
        pass