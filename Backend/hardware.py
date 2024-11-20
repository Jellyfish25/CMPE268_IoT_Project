import os
from threading import Thread
import time
import serial

TESTING = False

class Hardware:

    def __init__(self):

        if not TESTING:
            #Initialize serial connection
            self.ser_con = serial.Serial("/dev/cu.usbmodem14301", 9600, timeout=1)

        #Resume previous settings on restart
        self.path_root = os.path.dirname(__file__)
        try:
            with open(self.path_root + "/goal_temp.txt", "r") as f:
                self.goal_temp = float(f.read())
        except IOError:
            with open(self.path_root + "/goal_temp.txt", "w") as f:
                self.goal_temp = 20
                f.write("20")

        #Default to 25 temp, then try to update to real
        self.cur_temp = 25
        self.update_temp()

        #Thread variables
        self.fan_thread = None
        self.enabled = False

    def update_temp(self):
        if TESTING:
            print("Updated temp")
        else:
            if self.ser_con.in_waiting > 0:
                data = self.ser_con.readline().decode('utf-8').strip()
                #print(f"retrieved data: {data}")
                if "Temperature:" in data:
                    self.cur_temp = data.split(":")[1].strip()
                    #print(f"Received temperature:{self.cur_temp}")

    def set_goal(self, goal):
        self.goal_temp = float(goal)
        with open(self.path_root + "/goal_temp.txt", "w") as f:
            f.write(str(self.goal_temp))

    #TODO: Replace with however it actually controls fan
    def spin_fan(self):
        t_dif = self.cur_temp - self.goal_temp

        if TESTING:
            if t_dif < -2:
                print("Fan stopped due to low temp!")
            elif t_dif < 0:
                print("Fan spinning slowly")
            elif t_dif < 2:
                print("Fan spinning medium")
            else:
                print("Fan max power!")

    def do_stuff(self):
        while self.enabled:
            self.update_temp()
            self.spin_fan()
            time.sleep(1)

    def start(self):
        if not self.enabled:
            self.enabled = True
            self.fan_thread = Thread(target=self.do_stuff, daemon=True)
            self.fan_thread.start()

    def stop(self):
        if self.enabled:
            self.enabled = False
            self.fan_thread.join()
            #TODO: Actually stop fan
            print("Fan stoppped!")