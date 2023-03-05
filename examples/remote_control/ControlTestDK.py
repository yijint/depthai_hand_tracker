# Edited file - original file as courtesy of https://github.com/geaxgx/depthai_hand_tracker/tree/main/examples/remote_control
#!/usr/bin/env python3

README = """
This basic demo demonstrates the control the user have on how and when events are triggered,
by simply printing to the console event information each time an event is triggered. 

This control is defined with the following parameters of a pose-action:
- trigger : possible values: 
    - enter (default): an event is triggered once, when the pose begins,
    - enter_leave : two events are triggered, one when the pose begins and one when the pose ends,
    - periodic : events are triggered periodically as long as the pose stands.
                 The period is given by the parameter 'next_trigger_delay' in s.
    - continuous : events are triggered on every frame.

- first_trigger_delay: because false positive happen in pose recognition, 
you don't necessarily want to trigger an event on the first frame where the pose is recognized.
The 'first_trigger_delay' in seconds specifies how long the pose has to stand before triggering
an initial event.

"""

print(README)

from HCDK import HandController

def trace(event):
    event.print_line()

def trace_rotation(event):
    event.print_line() 
    print("Rotation:", event.hand.rotation) 

def trace_fist(event):
    event.print_line()
    # when fist is closed, landmark 12 is at center of fist...
    x, y = event.hand.landmarks[12,:2]
    print(f"Landmark : x={x}  y={y}") 

# changed config render to false so can run in cron shell
config = {
    'renderer' : {'enable': False},
    
    'pose_actions' : [
        # {'name': 'various_enter_leave', 'pose':["TWO","THREE","FOUR","PEACE"], 'hand':'right', 'callback': 'trace',"trigger":"enter_leave"},
        {'name': 'simple_takeoff', 'pose':'OK', 'hand':'any', 'callback': 'trace',"trigger":"continuous"},
        {'name': 'simple_land', 'pose':'PEACE', 'hand':'any', 'callback': 'trace',"trigger":"continuous"},
        {'name': 'simple_yaw', 'pose':'ROCK', 'hand':'any', 'callback': 'trace_rotation',"trigger":"continuous"},
        {'name': 'simple_push_pull', 'pose':'FIVE', 'hand':'any', 'callback': 'trace',"trigger":"continuous"},
        {'name': 'simple_drag', 'pose':'FIST', 'hand':'any', 'callback': 'trace_fist',"trigger":"continuous"}
    ]
}

HandController(config).loop()