from pyModbusTCP.server import DataBank, ModbusServer
import random


class LocalDataBank(DataBank):
    """A custom ModbusServerDataBank for override get_holding_registers method."""

    def __init__(self):
        super().__init__(virtual_mode=True)

    def get_holding_registers(self, address, number=1, srv_info=None):
        """Get virtual holding registers."""
        v_regs_d = list()
        v_regs_d.append(random.randrange(start=10, stop=200))
        try:
            print(f"sending value: {v_regs_d}")
            return v_regs_d
        except KeyError:
            return


if __name__ == '__main__':
    # init modbus server and start it
    server = ModbusServer(host='0.0.0.0', port=502, data_bank=LocalDataBank())
    print("starting server")
    server.start()
