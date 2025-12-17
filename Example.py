import asyncio
import time

from WKL100 import WKL100


async def main():
    chamber = await WKL100.create('139.6.69.109')

    # read number of operating hours
    print(f'Chamber Runtime = {await chamber.get_runtime():.2f}h')

    # set temperature
    await chamber.set_temperature(42.3)

    # turn chamber on
    await chamber.activate(True)

    # read and print temperature
    for i in range(10):
        time.sleep(1)
        print(f'{await chamber.get_temperature():.2f}°C, {await chamber.get_humidity():.2f}%')

    # turn chamber off
    await chamber.activate(False)


if __name__ == '__main__':
    asyncio.run(main())