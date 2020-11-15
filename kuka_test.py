from controller import Robot, Camera
import pytesseract
import PIL
from PIL import Image
import re 
import kuka_brain
from kuka_brain import pic_process, catch_it,proceedure_monad
import threading
import tkinter as tk
import datetime 
import kuka_interface
from kuka_interface import widgets 
import pathlib
import os 

# here we use the pathlib to spot the real absolute path
# of our software, so that the images will be stored indepently of configuration

def file_name(file):
    x = os.path.realpath(__file__)
    y = x.split("\\")
    y.remove(y[len(y)-1]) 
    p = "\\".join(y)
    
    return p+r"\{z}".format(z=file)


global p_img 
global t_path
global n_img

t_path = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" 
p_img = file_name('test_img_1.png')
n_img = 'test_img_1.png'

# here we use some markers , so in the future they will
# be able to control the information's flow
# through the threads and widgets 

markers = {
    "initial":[
    ],
    "break_energy":[
    ],
    "alarm":[
    ]
}

# both of this functions put the hour that the robot's motor started
# and finish 
def finish():
    date__ = str(datetime.datetime.now()).split()
    markers["break_energy"].append(1)
    
def start_x():
    date__ = str(datetime.datetime.now()).split()
    markers["initial"].append(1)
    

options = [start_x,finish]

def interface_import():
# here we first evoke a window 
    window = tk.Tk()
    global date
# configure the labels for the date 
    date = tk.Label(
    master=window,
    bg="black",
    fg='white',
    width=18,
    height=3
    )
    global date_f
    date_f = tk.Label(
    master=window,
    bg="black",
    fg='white',
    width=18,
    height=3
    )

    date.grid(row=0,column=0)
    date_f.grid(row=0,column=1)
    
    widgets(window,options)
         
                      
# using the already created delay function
def delay(time_milisec):
   timeValue = time_milisec/1000.0;
   initTime = robot.getTime()
   timeLeft = 0.00
   while (timeLeft < timeValue):
       currentTime = robot.getTime()
       timeLeft = currentTime - initTime
       robot.step(timestep)

# starting the robot's main function
robot = Robot()

n0 = 106
n1 = 127
n2 = 148

position_list = [n0,n1,n2,n2]

# here we call all robot's sensors

timestep = int(robot.getBasicTimeStep())

base_braço = robot.getMotor("arm1")
joint_0 = robot.getMotor("arm2")
joint_1 = robot.getMotor("arm3")
joint_2 = robot.getMotor("arm4")
pulso = robot.getMotor("arm5") 

roda_0 = robot.getMotor("wheel1")
roda_1 = robot.getMotor("wheel2")
roda_2 = robot.getMotor("wheel3")
roda_3 = robot.getMotor("wheel4")

rodas_l = [roda_0,roda_1,roda_2,roda_3]

finger_0 = robot.getMotor("finger1")
finger_1 = robot.getMotor("finger2")

joint_list = [joint_2,finger_0,finger_1]
finger_list = [finger_0,finger_1]

wj = [rodas_l,joint_list]

c = Camera("camera")

c.enable(samplingPeriod=2000)
# importing the tesseract executable again 
pytesseract.pytesseract.tesseract_cmd = t_path

def robot_initial():
    while robot.step(timestep) != -1:
        c.enable(samplingPeriod=100)
    
# here the robot goes forward to the tags       
        for r in rodas_l:
            r.setPosition(n0)

        base_braço.setPosition(1.5)
        delay(8500)
# here we start robot's whole process
# if the 'break energy' marker have a value the system's stop 
        counter = 0
        while counter < len(position_list)+1:
            if len(markers["break_energy"]) != 0:
                break 
            else:
                pass       
# here we save the image and passes the url as argument
# to the function that will get the picture there and process it  
            c.saveImage(
            filename=n_img,
            quality=100
            )
            phrase = pic_process()
            print(phrase)
            n = position_list[counter]
            p =  proceedure_monad("r",phrase,n,wj,delay,counter)
            if p == 0:
                pass
            else:
                break 
            counter+=1
        break
        markers["break_energy"].append(1)
        pass

def check_interface(t):
# here we associate some functions of showing the time
# to the buttons
# if the button is pressed the marker receive an value and
# then starts the actions associated to it
    while True:
        if len(markers["initial"]) != 0:
            t.start()
            date__ = str(datetime.datetime.now()).split()
            date["text"] = """start at
day:{d}
hour: {d1}""".format(
                 d=date__[0],
                 d1=date__[1]
                 )
                 
            markers["initial"].clear()
        else:
            pass 

        if len(markers["break_energy"]) != 0:
            print("break energy")
            t.join()
            date__ = str(datetime.datetime.now()).split()
            date_f["text"] = """finish at
day:{d}
hour: {d1}""".format(
                 d=date__[0],
                 d1=date__[1]
                 )
            markers["break_energy"].clear()
        else:
             pass 

