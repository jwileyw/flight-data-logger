# Flight Data Logger

A flight data logger for small vehicles like drones and model rockets. Will record and store altitude, pressure, and motion to a microSD card. 

## Hardware
- Raspberry Pi Pico (RP2040)
- BMP388 barometric pressure and temperature sensor breakout
- LSM6DSOX accelerometer and gyroscope breakout
- microSD breakout

## Software
- MicroPython
- Eventual rework in C (planned)

## Interfaces
- I2C
    - Bus details: I2C1 (BMP388 SDA GP14, SCL GP15) (LSM6DSOX planned)
- SPI (microSD, planned)

## Status
- BMP388 working
- Prints altitude relative to startup initializiation, pressure, temperature