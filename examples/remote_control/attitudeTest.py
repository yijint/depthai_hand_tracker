#!/usr/bin/env python3
import time, sys, argparse, math
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import numpy as np
from DroneKitAPI import Quadcopter

# print("connecting")
# vehicle = connect('com8', wait_ready = False)
# print("connected")
# quad = Quadcopter(connection_string='com5',baud=921600)

# quad.arm()
# time.sleep(3)
# quad.condition_yaw(30, relative=True)
# time.sleep(4)
# quad.vehicle.armed=False
# quad.vehicle.close()

while True:
    # vector = [0,1]
    # get fist's x, y pos
    # subtract from center 'origin' coords (half resolution)
    # rotate vector with appropiate matrix to account for camera roll/pitch
    roll = quad.getAttitude("ROLL") # returns negative values for CW angles, and vice versa
    # pitch = quad.getAttitude("PITCH")
    # yaw = quad.getAttitude("YAW")
    # attitude = quad.getAttitude("ALL")
    print(roll)
    # roll is sideways tilt, pitch is forward/backwards tilt, yaw is z-axis rotation, and all returns all in an array
    # mat = [[math.cos(roll),math.sin(roll)],[-math.sin(roll),math.cos(roll)]]
    # vector = np.matmul(mat,vector)
    # print(vector)
    # time.sleep(0.1)
    # print(roll)