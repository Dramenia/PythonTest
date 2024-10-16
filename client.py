from typing import List
from pyModbusTCP.client import ModbusClient
from multiprocessing import Queue

from workers.data_reader_worker import DataReader


def main():
    c = None
    WORKERS_NUM = 3
    input_queue = Queue()
    try:
        c = ModbusClient(host='server',
                        port=502,
                        auto_open=True,
                        auto_close=False)
    
        if c.is_open:
            regs = c.read_holding_registers(0, 1)
            if regs:
                print(f"Received data: {regs}")
            else:
                print("Failed to receive data")
        else:
            print("Failed to connect to the Modbus server")
    except ValueError:
        print("Error with host or port params")
    data_worker_threads: List[DataReader] = []
    
    for _ in range(WORKERS_NUM):
        data_worker = DataReader(input_queue=input_queue)
        data_worker_threads.append(data_worker)

    while True:
        if c is None:
            exit(1)
        try:
            if c.open():
                results = c.read_holding_registers(reg_addr=0, reg_nb=1)
                if results:
                    input_queue.put(results)
                else:
                    input_queue.put("DONE")
                    break
        except Exception:
            print("Error accessing data.")

    for i in range(len(data_worker_threads)):
        data_worker_threads[i].join()

if __name__ == '__main__':
    print("starting client")
    main()
