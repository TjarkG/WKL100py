import asyncio
import time

from WKL100 import WKL100


async def main():
    chamber = await WKL100.create('192.168.1.187')

    # read number of operating hours
    print(f'Chamber Runtime = {await chamber.get_runtime():.2f}h')

    # set temperature and humidity
    await chamber.set_target(42.3, 30)

    # turn chamber on
    await chamber.activate(True, True)

    # read and print temperature
    for i in range(10):
        time.sleep(1)
        print(f'{await chamber.get_temperature():.2f}°C, {await chamber.get_humidity():.2f}%')

    # turn chamber off
    await chamber.activate(False, False)


if __name__ == '__main__':
    asyncio.run(main())