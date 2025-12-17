import asyncio
import struct
import time
from typing import List

from pymodbus import FramerType
from pymodbus.client import AsyncModbusTcpClient


# convert float to two register values
def float_to_regs(temp: float) -> List[int]:
    float_bytes = bytes(struct.pack(">f", temp))
    return [float_bytes[2] << 8 | float_bytes[3], float_bytes[0] << 8 | float_bytes[1]]


# convert two register values to float
def reg_to_float(reg: List[int]) -> float:
    float_bytes = reg[1].to_bytes(2, byteorder='big') + reg[0].to_bytes(2, byteorder='big')
    return struct.unpack('>f', float_bytes)[0]


class WKL100:
    def __init__(self):
        self.client = None

    @classmethod
    async def create(cls, address: str):
        self = cls()
        self.client = AsyncModbusTcpClient(address, port=8000, framer=FramerType.RTU)
        await self.client.connect()
        return self

    async def _write(self, register: int, data: List[int]) -> None:
        data_rev = [(x >> 8) & 0xFF | (x << 8) & 0xFF00 for x in data]
        await self.client.write_registers(register, data_rev)

    async def _read(self, register: int, n: int) -> List[int]:
        result = await self.client.read_input_registers(register, count=n)
        return [(x >> 8) & 0xFF | (x << 8) & 0xFF00 for x in result.registers]

    # turn climate chamber on or off
    async def activate(self, active: bool) -> None:
        if active:
            await self._write(32769, [0, 0, 0, 0, 1, 0, 0, 0])
        else:
            await self._write(32769, [0, 0, 0, 0, 0, 0, 0, 0])

    # set target temperature in °C
    async def set_temperature(self, temp: float) -> None:
        t_val = float_to_regs(temp)
        await self._write(32776,
                          t_val + [0x0000, 0xc2a0, 0x0000, 0x433e, 0x0001, 0x0000, 0x4248, 0x0000, 0x0000, 0x0000,
                                   0x42c8,
                                   0x0002])

    # read temperature
    async def get_temperature(self) -> float:
        temp_regs = await self._read(32770, 4)
        return reg_to_float(temp_regs[0:2])

async def test_wkl100():
    chamber = await WKL100.create('139.6.69.109')

    # set temperature
    await chamber.set_temperature(42.3)

    # turn chamber on
    await chamber.activate(True)

    # read and print temperature
    for i in range(10):
        time.sleep(1)
        print(await chamber.get_temperature())

    # turn chamber off
    await chamber.activate(False)

if __name__ == '__main__':
    asyncio.run(test_wkl100())
