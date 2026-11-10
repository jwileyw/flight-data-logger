# Flight Data Logger

A flight data logger for small vehicles like drones and model rockets. Will record and store altitude, pressure, and motion to a microSD card. 

## Hardware
- Raspberry Pi Pico (RP2040)
- BMP388 barometric pressure and temperature sensor breakout
- LSM6SDOX accelerometer and gyroscope breakout
- microSD breakout

## Software
- MicroPython
- Eventual rework in C (planned)

## Interfaces
- I2C
    - Bus details: I2C1, BMP388 SDA GP14, SCLGP15

## Status
- BMP388 is configured over I2C, reads raw temperature and pressure data
- Trimming coefficients indexed from BMP388 NVM read, sign conversion in progress
- Calibration for meaningful values next