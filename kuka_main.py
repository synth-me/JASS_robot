import threading
import kuka_test
from kuka_test import robot_initial, interface_import, check_interface

# first we import all functions
# we start a thread for the interface
# another for the robot's motors and action
# and the last thread will be reacting to the actions of the interface
# and integrating the interface with the robot's motor
# given the results, the threads are killed 

t0 = threading.Thread(target=interface_import,args=())
t1 = threading.Thread(target=robot_initial,args=())
func_list = [t1]
t2 = threading.Thread(target=check_interface,args=(func_list))

t0.start()
t2.start()
