from flask import Flask
from flask import render_template, request
from datetime import datetime
from random import *
from fhict_cb_01.CustomPymata4 import CustomPymata4
import time, sys
import math

app=Flask(__name__)
#-----------
# Constants
#-----------
DHTPIN  = 12 
LDRPIN = 2 
#------------------------------
# Initialized global variables
#------------------------------
humidity = 0
temperature = 0
light=0
current_time=0
avgT=0
avgH=0
avgL=0
liT=[]
liH=[]
liL=[]

def setup():
    global board
    board = CustomPymata4(com_port = "/dev/cu.usbserial-14210")
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05)
    board.set_pin_mode_analog_input(LDRPIN)

setup()
#-----------
# functions
#-----------

def curr_time():
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return current_time
 
def LDRChanged():
    light, timestamp= board.analog_read(LDRPIN)
    return light
    
def Measure():
    humidity, temperature, timestamp = board.dht_read(DHTPIN)
    return (humidity, temperature)

def Avg(temperature,liT):
    liT.append(temperature)
    return sum(liT)/len(liT)

def Min(temperature, liT):
    liT.append(temperature)
    return min(liT)

def Max(temperature, liT):
    liT.append(temperature)
    return max(liT)


def round_up(temperature, decimals=0):
    multiplier=10**decimals
    return math.ceil(temperature*multiplier)/multiplier

# @app.route('/') 
# def index():
#     current_time=curr_time()
#     light=LDRChanged()
#     humidity, temperature=Measure()
#     avgT=round_up(Avg(temperature,liT),2)
#     avgH=round_up(Avg(humidity,liH),2)
#     avgL=round_up(Avg(light,liL),2)
#     minT=Min(temperature,liT)
#     minH=Min(humidity,liH)
#     minL=Min(light,liL)
#     maxT=Max(temperature,liT)
#     maxH=Max(humidity,liH)
#     maxL=Max(light,liL)
#     return render_template('flask_ard.html', 
#     current_time=current_time, hum=humidity, temp=temperature, 
#     level1=light, avgT=avgT, avgH=avgH, avgL=avgL, minT=minT,
#     minH=minH, minL=minL, maxT=maxT, maxH=maxH, maxL=maxL)    
  

@app.route("/")
def index():
    return render_template('flask_ard.html', data=json_data)


@app.route("/post_data", methods=['POST']) 
def receive_data():
    global json_data
    json_data = request.json
    return "OK", 200
