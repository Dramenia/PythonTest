from pyModbusTCP.client import ModbusClient

c = None

try:
    c = ModbusClient(host='localhost',
                     port=502,
                     auto_open=True,
                     auto_close=False)
except ValueError:
    print("Error with host or port params")

while True:
    if c is None:
        exit(1)
    try:
        if c.open():
            results = c.read_holding_registers(reg_addr=0, reg_nb=1) #list of size reg_nb
    except Exception:
        print("Error accessing data.")
