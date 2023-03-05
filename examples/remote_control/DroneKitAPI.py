# Modified from examples provided by official DroneKit API
# https://dronekit-python.readthedocs.io/en/latest/examples/guided-set-speed-yaw-demo.html

import time, sys, argparse, math, os
os.environ['MAVLINK20'] = '1'
import numpy as np
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil

class Quadcopter:
    def __init__(self, connection_string : str, baud : int):
        print("Connecting...")
        self.vehicle = connect(connection_string, wait_ready=False, baud=baud)
        print("Connection established.")
        # change FoR as needed
        self.initAlt = self.vehicle.location.global_relative_frame.alt
    
    def getAttitude(self, param, degrees=False):
        if param == "ALL":
            return self.vehicle.attitude # can scalar multiply list?
            # for i in range(len(self.vehicle.attitude)):
            #     self.vehicle.attitude[i] = self.vehicle.attitude[i]*180/math.pi
        elif param == "ROLL":
            if degrees:
                return self.vehicle.attitude.roll*180/math.pi
            return self.vehicle.attitude.roll
        elif param == "PITCH":
            if degrees:
                return self.vehicle.attitude.pitch*180/math.pi
            return self.vehicle.attitude.pitch
        elif param == "YAW":
            if degrees:
                return self.vehicle.attitude.yaw*180/math.pi
            return self.vehicle.attitude.yaw
        else:
            return None
    
    def attitudeAdjust(self, vec, param):
        if param in ["ROLL","PITCH","YAW"]:
            att = self.getAttitude(param)
            theta = -(att)
            # apply CCW rotation matrix with theta to vector
            mat = [[math.cos(theta),math.sin(theta)],[-math.sin(theta),math.cos(theta)]]
            return np.matmul(mat,vec)
        else:
            print("The function only takes singular values, not arrays.")
            return None
        
    def arm(self):
        if not self.vehicle.armed:
            # print("Basic pre-arm checks")
            # # Don't let the user try to arm until autopilot is ready
            # while not self.vehicle.is_armable:
            #     print(" Waiting for vehicle to initialise...")
            #     time.sleep(1)

            print("Arming motors")
            # Copter should arm in GUIDED mode
            # self.vehicle.mode = VehicleMode("GUIDED")
            self.vehicle.armed = True
            
            while not self.vehicle.armed:      
                print(" Waiting for arming...")
                time.sleep(0.5)
    
    def takeoff(self, aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """
        if not self.vehicle.armed:
            self.arm()

        print("Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
        # after Vehicle.simple_takeoff will execute immediately).
        self.wait_for_alt(aTargetAltitude, epsilon=0.25, rel=True, timeout=None)
        print("Reached target altitude.")
        # while True:
        #     print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)      
        #     if self.vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
        #         print("Reached target altitude")
        #         break
        #     time.sleep(1)
    
    def land(self):
        self.vehicle.mode = VehicleMode("LAND")
        # wait until landed
        # epsilon in meters, rel = global / global_relative, timeout = error after x seconds
        self.vehicle.wait_for_alt(self.initAlt, epsilon=0.1, rel=True, timeout=None)
        print("Touchdown.")
        
    def condition_yaw(self, heading, relative=False):
        """
        Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).
        This method sets an absolute heading by default, but you can set the `relative` parameter
        to `True` to set yaw relative to the current yaw heading.
        By default the yaw of the vehicle will follow the direction of travel. After setting 
        the yaw using this function there is no way to return to the default yaw "follow direction 
        of travel" behaviour (https://github.com/diydrones/ardupilot/issues/2427)
        For more information see: 
        http://copter.ardupilot.com/wiki/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_condition_yaw
        """
        if relative:
            is_relative = 1 #yaw relative to direction of travel
        else:
            is_relative = 0 #yaw is an absolute angle
        # create the CONDITION_YAW command using command_long_encode()
        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
            0, #confirmation
            heading,    # param 1, yaw in degrees
            0,          # param 2, yaw speed deg/s
            1,          # param 3, direction -1 ccw, 1 cw
            is_relative, # param 4, relative offset 1, absolute angle 0
            0, 0, 0)    # param 5 ~ 7 not used
        # send command to vehicle
        self.vehicle.send_mavlink(msg)

    def play_scale(self):
        '''Play a tune on the vehicle'''
        tune_c_scale = b'MFT200L16<cdefgab>cdefgab>c'
        self.vehicle.play_tune(tune_c_scale)