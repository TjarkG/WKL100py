# Python Library for Weiss WKL100 Climate Chamber

WKL100py is a python library to easily control a WKL100 Climate Chamber, without having to rely on S!MPATI. It was only tested on the WKL100, but will probably work for other Chambers with a MinCon32 Controller too.

## Usage

Download the [WKL100.py](WKL100.py) File and place it in the same directory as your code.
You can then start building your own Script based on the Example below. For a more complex example, see [Example.py](Example.py)

```python
import asyncio

from WKL100 import WKL100

async def main():
    chamber = await WKL100.create('192.168.21.109')

    # read temperature
    print(f'{await chamber.get_temperature():.2f}°C')

    # set temperature
    await chamber.set_temperature(42.3)

    # turn chamber on
    await chamber.activate(True)


asyncio.run(main())
```

## Documentation of the Modbus Interface

There is no official documentation of the Modbus Interface as fare as I can tell, but I wrote down my best guess in [Modbus_Docu.md](Modbus_Docu.md)