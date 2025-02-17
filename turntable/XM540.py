import os
from dynamixel_sdk import *
import logging as log
from time import time, sleep

class XM540:
    PROTOCOL_VERSION         = 2.0
    BAUDRATE                 = 57600
    DXL_ID                   = 2

    MIN_TARGET_POS = 0
    MAX_TARGET_POS = 4095

    def __init__(self, DEVICE_NAME="/dev/ttyUSB0", motor_id=None, velocity=100, packet_handler=None):
        if motor_id is None:
            motor_id = self.DXL_ID
        self.packetHandler = PacketHandler(XM540.PROTOCOL_VERSION) if packet_handler is None else packet_handler
        self.portHandler = PortHandler(DEVICE_NAME)
        self.id = motor_id
        self.velocity = velocity
        self.open_port()
        self.set_baudrate()
        self.connect_library()
        self._target = None
        self.set_vel_raw(self.velocity)
        

    def wait_until_done(self, timeout=10.0, tolerance=50):
        if self._target is None:
            return
        start = time()
        raw_pos = 0
        while True:
            if timeout is not None and time() - start > timeout:
                print(f'[TurntableMotor] timed out at {timeout} sec')
                return raw_pos
            self.set_pos_raw(self._target)
            raw_pos, succ = self.get_pos_raw()
            if not succ:
                sleep(0.05)
                continue
            diff = self.get_distance(raw_pos, self._target)
            if diff < tolerance:
                self._target = None
                return raw_pos         
            sleep(0.05)

    def get_distance(self, a, b):
        _min = min(a, b)
        _max = max(a, b)
        return min(_max - _min, _min+4096-_max)

    def connect_library(self):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, 64, 1)
        if dxl_comm_result != COMM_SUCCESS:
            log.debug("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            log.debug("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            log.debug("Dynamixel has been successfully connected")

    def open_port(self):
        if self.portHandler.openPort():
            log.info("Succeeded to open the port")
        else:
            log.error("Failed to open the port, terminating")
            quit()
    
    def set_baudrate(self):
        if self.portHandler.setBaudRate(self.BAUDRATE):
            log.info("Succeeded to change the baudrate")
        else:
            log.error("Failed to change the baudrate, terminating")
            quit()

    def close_port(self):
        self.portHandler.closePort()
        log.info('Successfully closed port')

    def check_error(self, dxl_comm_result, dxl_err):
        if dxl_comm_result != COMM_SUCCESS:
            log.info("[Turntable]%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_err != 0:
            log.info("[Turntable]%s" % self.packetHandler.getRxPacketError(dxl_err))
        else:
            log.debug("Successful COMMAND")
            return True
        return False

    def write_4_byte(self, reg_num, reg_value):
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(
            self.portHandler, self.id, reg_num, reg_value)
        return self.check_error(dxl_comm_result, dxl_error)

    def write_2_byte(self, reg_num, reg_value):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler, self.id, reg_num, reg_value)
        return self.check_error(dxl_comm_result, dxl_error)

    def read_4_byte(self, reg_num):
        reg_data, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(
            self.portHandler, self.id, reg_num)
        return reg_data, self.check_error(dxl_comm_result, dxl_error)

    def read_2_byte(self, reg_num):
        reg_data, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(
            self.portHandler, self.id, reg_num)
        return reg_data, self.check_error(dxl_comm_result, dxl_error)

    def get_pos_raw(self):
        try:
            current_position, succ = self.read_4_byte(132)
        except:
            sleep(0.02)
            return self.get_pos_raw() #not sure if this is a good idea but lets go for now.
        return current_position, succ

    def set_vel_raw(self, raw_vel):
        """Set the velocity
        
        Arguments:
            raw_vel {[type]} -- [description]
        """
        err = self.write_4_byte(112, int(raw_vel))
        if err:
            log.debug("Set vel to %d" % int(raw_vel))

    def set_pos_raw(self, raw_pos):
        raw_pos = int(raw_pos)
        if raw_pos < self.MIN_TARGET_POS or raw_pos > self.MAX_TARGET_POS:
            log.error(f"[Error]: Wrong pos!, must be in range ({self.MIN_TARGET_POS}, {self.MAX_TARGET_POS})")
            return False
        self._target = raw_pos
        err = self.write_4_byte(116, raw_pos)
        if err:
            log.debug("Set pos to %d" % raw_pos)
        return True

    def reset_to_0(self):
        self.set_pos_raw(0)

    def set_pos_degree(self, degree_pos):
        err = self.write_4_byte(116, int(float(degree_pos) * 11.3777))
        if err:
            log.debug("Set pos to %d degree" % int(degree_pos))

    def move_one_degree(self):
        cur_pos_raw = self.get_pos_raw()
        next_pos_raw = cur_pos_raw + 16 #
        if next_pos_raw > self.MAX_TARGET_POS:
            next_pos_raw %= self.MAX_TARGET_POS
        self.set_pos_raw(next_pos_raw)
        return

    def move_n(self, n):
        cur_pos_raw = self.get_pos_raw()
        next_pos_raw = cur_pos_raw + n #
        if next_pos_raw > self.MAX_TARGET_POS:
            next_pos_raw %= self.MAX_TARGET_POS
        self.set_pos_raw(next_pos_raw)
        return
    
    