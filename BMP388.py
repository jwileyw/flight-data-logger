from machine import Pin
from machine import I2C
import time
import struct



i2c = I2C(1, scl = Pin(15), sda = Pin(14))                  # create I2C object

i2c.writeto_mem(0x77, 0x1B, b'\x33')                        # change power mode to normal

i2c.writeto_mem(0x77, 0x1D, b'\x02')                        # ODR: output data rate = 50Hz

i2c.writeto_mem(0x77, 0x1C, b'\x02')                        # OSR: standard oversampling, x4 pressure x1 temperature

trims = i2c.readfrom_mem(0x77, 0x31, 21)                    # get trimming coefficients

nvm_par_t1, nvm_par_t2, nvm_par_t3, nvm_par_p1, nvm_par_p2, nvm_par_p3, nvm_par_p4, nvm_par_p5, nvm_par_p6, nvm_par_p7, nvm_par_p8, nvm_par_p9, nvm_par_p10, nvm_par_p11 = struct.unpack("<HHbhhbbHHbbhbb", trims)      

par_t1 = nvm_par_t1 / 2**-8
par_t2 = nvm_par_t2 / 2**30
par_t3 = nvm_par_t3 / 2**48
par_p1 = (nvm_par_p1 - 2**14) / 2**20
par_p2 = (nvm_par_p2 - 2**14) / 2**29
par_p3 = nvm_par_p3 / 2**32
par_p4 = nvm_par_p4 / 2**37
par_p5 = nvm_par_p5 / 2**-3
par_p6 = nvm_par_p6 / 2**6
par_p7 = nvm_par_p7 / 2**8
par_p8 = nvm_par_p8 / 2**15
par_p9 = nvm_par_p9 / 2**48
par_p10 = nvm_par_p10 / 2**48
par_p11 = nvm_par_p11 / 2**65


# temperature compensation
def compensate_temp(uncomp_temp):
    partial_data1 = uncomp_temp - par_t1
    partial_data2 = partial_data1 * par_t2
    return partial_data2 + (partial_data1**2 * par_t3)


# pressure compensation
def compensate_press(t_lin, uncomp_press):
    partial_data1 = par_p6 * t_lin
    partial_data2 = par_p7 * t_lin**2
    partial_data3 = par_p8 * t_lin**3
    partial_out1 = par_p5 + partial_data1 + partial_data2 + partial_data3

    partial_data1 = par_p2 * t_lin
    partial_data2 = par_p3 * t_lin**2
    partial_data3 = par_p4 * t_lin**3
    partial_out2 = uncomp_press * (par_p1 + partial_data1 + partial_data2 + partial_data3)

    partial_data1 = uncomp_press**2
    partial_data2 = par_p9 + par_p10 * t_lin
    partial_data3 = partial_data1 * partial_data2
    partial_data4 = partial_data3 + uncomp_press**3 * par_p11
    return partial_out1 + partial_out2 + partial_data4


# barometric formula constants
ref_temp = 288.15
temp_lapse = 0.0065
ref_press = 101325
baro_exp = 5.2559


# altitude calculation
def calc_alt(comp_press):
    return (ref_temp / temp_lapse) * (1 - (comp_press / ref_press)**(1 / baro_exp))


while True:
    data = i2c.readfrom_mem(0x77, 0x04, 6)
    
    uncomp_press = data[0] | data[1]<<8 | data[2]<<16
    uncomp_temp = data[3] | data[4]<<8 | data[5]<<16

    t_lin = compensate_temp(uncomp_temp)
    comp_press = compensate_press(t_lin, uncomp_press)
    alt = calc_alt(comp_press)
 
    print("\raltitude = ", alt, "m", "                pressure = ", comp_press, "Pa",           "                temperature = ", t_lin, "°C      ", end = " ")
    time.sleep(0.5)