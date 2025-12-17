# Weiss WKL100 Modbus Interface Documentation

## Interfaces

This Documentation is only concerned with the Ethernet Interface of the WKL100, the Serial Interface might be similar (
not tested yet). On the Ethernet Interface, two connections are established between the S!MPATI Software and the Climate
Chamber.
With both, the Climate Chamber is the Server and the PC the client.

### Port 9094

On Port 9094, the Climate Chamber allways send the following Data:

```
0x0000003f0000000000020300000000000011132c01000100000000033100
```

Which is acknowledged by the PC with a `0x00`.
Protocol and Purpose of this are unknown.

### Port 8000

This is the main Modbus RTU over TCP Interface. The PC sends either Modbus Message ID 4 or 10, which are then answered
by the climate chamber. The Device ID used is allways 1. Responses may be split across multiple TCP Packets.

Reading and writing is only possible for certain combinations of start address and number of registers, as described in
the Register Map. Sometimes, registers may seem to overlap due to this.

Data is Transmitted LSB first most of the time (exceptions are noted in the register map),
both inside Registers and when splitting data across multiple registers.
This will require changing the byteorder before sending
and after receiving when using a library since the standard for Modbus is MSB first.

Example: The Float `3704.6042` becomes `0x456789ab` when encoded in IEEE-754 Floating Point.
On the bus, it is transmitted as `ab896745`,
making it appear as `[0xab89, 0x6745]` with a standard Modbus Implementation.

## Register Map

### Read

#### Chamber Runtime

- Start Address: 32800
- Number of Registers: 2

| Register | Meaning                         |
|----------|---------------------------------|
| 0-1      | Float: Chamber runtime in hours |

#### Temperature and Humidity Measurements

- Start Address: 32770
- Number of Registers: 4

| Register | Meaning                  |
|----------|--------------------------|
| 0-1      | Float: Temperature in °C |
| 2-3      | Float: Humidity in %rh   |

#### 32769: Unknown

- Start Address: 32769
- Number of Registers: 16

| Register | Meaning                   |
|----------|---------------------------|
| 0-11     | 12 Bools, meaning unknown |

The Values read here are different from the ones written to the same address

### Write

#### Chamber and Humidity On/Off

- Start Address: 32769
- Number of Registers: 8

| Register | Meaning                         |
|----------|---------------------------------|
| 0-3      | Allways 0                       |
| 4        | Bit 0: Chamber, Bit 1: Humidity |
| 5-7      | Allways 0                       |

#### Set Temperature and Humidity Targets

Can also be Read at the same Address and with the same number of registers.

- Start Address: 32776
- Number of Registers: 14

| Register | Meaning                                   |
|----------|-------------------------------------------|
| 0-1      | Float: Temperature target in °C           |
| 2-3      | Float: Unknown, allways -34.5 in my Tests |
| 4-5      | Float: Unknown, allways 190 in my Tests   |
| 6        | Bool: Meaning unknown, reads back as 0    |
| 7-8      | Float: Humidity Target in %rh             |
| 9-11     | Allways 0                                 |
| 12-13    | Float: Allways 100.0                      |

#### Limits

The Data is MSB first here, both within registers and when splitting across registers.
Can also be Read at the same Address and with the same number of registers.

- Start Address: 3100
- Number of Registers: 8

| Register | Meaning                        |
|----------|--------------------------------|
| 0-1      | Float: Temperature lower limit |
| 2-3      | Float: Temperature upper limit |
| 4-5      | Float: Humidity lower limit    |
| 6-7      | Float: Humidity upper limit    |

### 99: Unknown

- Start Address: 99
- Number of Registers: 1

| Register | Meaning   |
|----------|-----------|
| 0        | Allways 0 |