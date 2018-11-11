from flask import Flask, render_template, jsonify, request
from threading import Lock, Thread, Condition
import csv
import datetime
from collections import deque
import time
import os
from random import randint
from kafka import KafkaConsumer
from flask_cors import CORS

consumer = KafkaConsumer('my-stream', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
fname = 'test.csv'
lock = Lock()
connex_app = Flask(__name__)
CORS(connex_app)



@connex_app.route("/")
def home():
    return render_template("home.html")



@connex_app.route("/data/<x>")

def get_data(x):
    x = int(x)
    lock.acquire()
    with open(fname, 'r') as f:
        q = deque(f, x)
    sum = 0
    for item in q:
        sum+= int(item.split(',')[1])
    average = sum/float(x)
    print (average)
    lock.release()
    time.sleep(1)
    ans = {'result': average}
    return jsonify(ans)
    
@connex_app.route("/stopconsumer")
def stop_consumer():
    lock.acquire()
    os.environ['StopConsumer'] = "True"
    print ('stopped consumer')
    lock.release()
    return jsonify({'result':"stopped consumer"})


        
def consumerWrite():

    lock.acquire()
    stopC = os.environ.get("StopConsumer", default="False")

    if stopC == "True":
        lock.release()
        print ("Not starting consumer")
        return
    lock.release()
 
    exitLoop  = False
    while True:

      for msg in consumer:
        lock.acquire()
        stopC = os.environ.get("StopConsumer", default="False")

        if stopC == "True":
            lock.release()
            print ("Exiting consumer..")
            exitLoop = True
            break            
        field =  (msg.value.decode('utf-8')).strip("[]").split(',')
        field[0] = str(field[0].strip('\''))
        field[1] = int(field[1])
                

        with open(fname, 'a') as f:    
            writer = csv.writer(f)    
            writer.writerow(field)
            print ('written to csv')
        
        lock.release()
        time.sleep(3)

      if exitLoop:
        print ("Exiting consumer finally...")
        break            
      else:
          lock.acquire()
          stopC = os.environ.get("StopConsumer", default="False")          
          if stopC == "True":
            lock.release()
            print ("Exiting consumer..")
            exitLoop = True
            break            
          lock.release()
      time.sleep(3)

@connex_app.route("/startconsumer")
def start_consumer():
    lock.acquire()
    os.environ['StopConsumer'] = "False"
    print ('started consumer')
    lock.release()
    t2 = Thread(target=consumerWrite)
    t2.start()
    return jsonify({'result':"started consumer"})

if __name__ == "__main__":
    connex_app.run(debug=True)
