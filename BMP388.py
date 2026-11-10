from machine import Pin
from machine import I2C
import time

    # create I2C object

i2c = I2C(1, scl = Pin(15), sda = Pin(14))

    # change power mode to normal

i2c.writeto_mem(0x77, 0x1B, b'\x33')

    # get trimming coefficients

trims = i2c.readfrom_mem(0x77, 0x31, 21)

nvm_t1 = trims[0] | trims[1]<<8
nvm_t2 = trims[2] | trims[3]<<8
nvm_t3 = trims[4]
nvm_p1 = trims[5] | trims[6]<<8
nvm_p2 = trims[7] | trims[8]<<8
nvm_p3 = trims[9]
nvm_p4 = trims[10]
nvm_p5 = trims[11] | trims[12]<<8 
nvm_p6 = trims[13] | trims[14]<<8
nvm_p7 = trims[15]
nvm_p8 = trims[16]
nvm_p9 = trims[17] | trims[18]<<8
nvm_p10 = trims[19] | trims[20]<<8
nvm_p11 = trims[20]

while True:
    data = i2c.readfrom_mem(0x77, 0x04, 6)
    press = data[0] | data[1]<<8 | data[2]<<16
    temp = data[3] | data[4]<<8 | data[5]<<16
    print("\rpressure = ", press, "                temperature = ", temp, end = " ")
    time.sleep(1)