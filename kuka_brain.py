import pytesseract
import PIL
from PIL import Image
import re
import controller
import json 
import pathlib
import os 

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
p_img =  file_name('test_img_1.png)
n_img =  'test_img_1.png'


pytesseract.pytesseract.tesseract_cmd = r'{y}'.format(y=t_path)

def pic_process():
# here we find the tesseract.exe
# we put the picture localizated on the image.open
# then return the text of the picture 
    dir  = r"{x}".format(x=str(p_img.replace("}\n","")))
    image = Image.open(dir)
    phrase = pytesseract.image_to_string(image, lang="eng",config="--psm 7")
    return phrase

def catch_it(delay,joints):
# here we change the joint's motors position
# to catch the object 
    delay(6000)
    joints[0].setPosition(-1.75) 
    joints[1].setPosition(0.02)
    joints[2].setPosition(0.02)
    delay(4000)
    joints[1].setPosition(0)
    joints[2].setPosition(0)
    delay(4000)
    joints[0].setPosition(1.75)

def throw(delay,joints):
# here we change the joint's motors positions
# so that the arm will just throw the object
# actually the object just fall because the arm just open
    print("throw the object")
    joints[1].setPosition(0.025)
    joints[2].setPosition(0.025)

def lateral_slide(wheels,mov,delay,position):
# here the robot will move in the path for going to the boxes
# to throw the object 
    rel = {
        0:-10, 
        1:10,
        2:-10,
        3:-10
        }
    r_now = rel[position]
# here the motor's wheel will move depending upon
# the localization of the robot given by
# the argument "position"    
    wheels[0].setPosition(mov)
    wheels[1].setPosition(-mov)
    wheels[2].setPosition(mov)
    wheels[3].setPosition(-mov)
    print('passed first')
    delay(10000)
# if the robot the robot is in the first box, a given
# amount of psition is needed and so on 
    wheels[0].setPosition(-mov+r_now)
    wheels[1].setPosition(-mov+r_now)
    wheels[2].setPosition(-mov+r_now)
    wheels[3].setPosition(-mov+r_now)
    print('passed second')
    delay(10000)

    
def proceedure_monad(char,phrase,move,wheels_joints,delay,position):
# this monad( bundle of functions at one) will detect the
# action given a input string
# uising the regular expressions we can detect the subtring the
# compose the main string and then act 
    if re.findall(char,phrase) or re.findall(">",phrase):
        for r in wheels_joints[0]:
            r.setPosition(move)
        delay(4000)
        return 0
    else:
        catch_it(delay,wheels_joints[1])
        delay(4000)
        lateral_slide(wheels_joints[0],move,delay,position)
        delay(4000)
        throw(delay,wheels_joints[1])
        delay(4000)
        return 1 
