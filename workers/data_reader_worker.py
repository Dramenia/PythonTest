import os

from dotenv import load_dotenv
from multiprocessing import Queue
from threading import Thread

from services.db_service import PostgresService

load_dotenv()

class DataReader(Thread):
    def __init__(self, input_queue: Queue, **kwargs) -> None:
        print('initalized')
        super().__init__(**kwargs)
        self.input_queue = input_queue
        self.database = PostgresService(table_name=os.environ.get("DEVICE_DATA_TABLE"))
        self.start()

    def run(self):
        print("running")
        while True:
            val = self.input_queue.get()
            if val == "DONE":
                break
            self.database.insert_data(value=val)
