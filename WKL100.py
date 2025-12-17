import struct
from typing import List

from pymodbus import FramerType
from pymodbus.client import AsyncModbusTcpClient


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

    # convert float to two register values
    @staticmethod
    def float_to_regs(temp: float) -> List[int]:
        float_bytes = bytes(struct.pack(">f", temp))
        return [float_bytes[2] << 8 | float_bytes[3], float_bytes[0] << 8 | float_bytes[1]]

    # convert two register values to float
    @staticmethod
    def reg_to_float(reg: List[int]) -> float:
        float_bytes = reg[1].to_bytes(2, byteorder='big') + reg[0].to_bytes(2, byteorder='big')
        return struct.unpack('>f', float_bytes)[0]

    # turn climate chamber on or off
    async def activate(self, active: bool) -> None:
        if active:
            await self._write(32769, [0, 0, 0, 0, 1, 0, 0, 0])
        else:
            await self._write(32769, [0, 0, 0, 0, 0, 0, 0, 0])

    # set target temperature in °C
    async def set_temperature(self, temp: float) -> None:
        t_val = self.float_to_regs(temp)
        await self._write(32776,
                          t_val + [0x0000, 0xc2a0, 0x0000, 0x433e, 0x0001, 0x0000, 0x4248, 0x0000, 0x0000, 0x0000,
                                   0x42c8,
                                   0x0002])

    # read temperature in °C
    async def get_temperature(self) -> float:
        temp_regs = await self._read(32770, 4)
        return self.reg_to_float(temp_regs[0:2])

    # read humidity in %rh
    async def get_humidity(self) -> float:
        temp_regs = await self._read(32770, 4)
        return self.reg_to_float(temp_regs[2:4])

    # read chamber runtime in hours
    async def get_runtime(self) -> float:
        runtime_regs = await self._read(32800, 2)
        return self.reg_to_float(runtime_regs)

