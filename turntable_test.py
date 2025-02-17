from turntable.XM540 import XM540
import time

def main():
    DEVICE_NAME="/dev/ttyUSB0"
    turntable1=XM540(DEVICE_NAME=DEVICE_NAME, velocity=12)
    MIN_TARGET_POS = 0
    MAX_TARGET_POS = 4095
    #turntable.set_pos_raw(4000)
    #turntable1.set_pos_raw(4095//2)
    for i in range(MIN_TARGET_POS, MAX_TARGET_POS,200):
        time.sleep(5)
        turntable1.set_pos_raw(i)


if __name__=="__main__":
    main()
