import os
from threading import Thread
import time
import serial

TESTING = False

class Hardware:

    def __init__(self):

        if not TESTING:
            #Initialize serial connection
            self.ser_con = serial.Serial("/dev/cu.usbmodem14101", 9600, timeout=1)

        #Resume previous goal on restart
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
        #while True:
        #    self.cur_temp = self.ser_con.readline().decode('utf-8').rstrip()

        #Fan spinny stuff
        self.fan_thread = None
        self.enabled = False

        #Start time, separate files because sick and brain not working
        try:
            with open(self.path_root + "/start_time.txt", "r") as f:
                self.start_time = f.read()
        except IOError:
            with open(self.path_root + "/start_time.txt", "w") as f:
                self.start_time = "00:01"
                f.write(self.start_time)

        #End time, separate files because sick and brain not working
        try:
            with open(self.path_root + "/end_time.txt", "r") as f:
                self.end_time = f.read()
        except IOError:
            with open(self.path_root + "/end_time.txt", "w") as f:
                self.end_time = "00:01"
                f.write(self.end_time)

        #Timing stuff, starts if between start and stop time
        self.updated_time = time.strftime("%H:%M", time.localtime())
        if self.start_time < self.updated_time < self.end_time:
            self.start()

        self.timing_thread = Thread(target=self.time_keeper, daemon=True)
        self.timing_thread.start()

    #Checks whether current time is start or stop
    #Once a minute to quickly get updates without triggering multiple times
    def time_keeper(self):
        while(True):
            if TESTING:
                print("Current Time: " + time.strftime("%H:%M", time.localtime()) + "\tStart Time: " + self.start_time + "\tEnd Time: " + self.end_time)

            if self.start_time != self.end_time:
                self.updated_time = time.strftime("%H:%M", time.localtime())
                if self.updated_time == self.end_time:
                    self.stop()
                elif self.updated_time == self.start_time:
                    self.start()
            time.sleep(60)

    def set_start(self, start_time):
        self.start_time = start_time
        with open(self.path_root + "/start_time.txt", "w") as f:
            f.write(str(self.start_time))

    def set_end(self, end_time):
        self.end_time = end_time
        with open(self.path_root + "/end_time.txt", "w") as f:
            f.write(str(self.end_time))

    def update_temp(self):
        if not TESTING:
            if self.ser_con.in_waiting > 0:
                data = self.ser_con.readline().decode('utf-8').strip()
                print(f"Retrieved raw data: {data}")  # Debugging: show raw data

                if "Temperature:" in data:
                    try:
                        # Extract and update temperature from the data
                        self.cur_temp = float(data.split(":")[1].strip())
                        print(f"Updated temperature: {self.cur_temp}")  # Debugging: confirm temperature update
                    except ValueError:
                        print(f"Error parsing temperature from data: {data}")  # Handle unexpected data formats
                else:
                    print(f"Data does not contain temperature information: {data}")  # Data format mismatch
            else:
                print("No data available in serial buffer")


    # def update_temp(self):
    #     if not TESTING:
    #         if self.ser_con.in_waiting > 0:
    #             data = self.ser_con.readline().decode('utf-8').strip()
    #             print(f"retrieved data: {data}")
    #             if "Temperature:" in data:
    #                 self.cur_temp = data.split(":")[1].strip()
    #                 #print(f"Received temperature:{self.cur_

                    
    def set_goal(self, goal):
        self.goal_temp = float(goal)
        with open(self.path_root + "/goal_temp.txt", "w") as f:
            f.write(str(self.goal_temp))

    #Four speed settings: 0 off to 3 max
    def get_cur_speed(self) -> int:
        t_dif = self.cur_temp - self.goal_temp
        if t_dif < -1:
            return 0
        elif t_dif < 0:
            return 1
        elif t_dif < 1:
            return 2
        else:
            return 3

    #TODO: Replace with however it actually controls fan
    def spin_fan(self):
        speeds = ["Off", "Slow", "Moderate", "Max"]
        print("Current fan speed: " + speeds[self.get_cur_speed()])

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
            print("Fan started!")

    def stop(self):
        if self.enabled:
            self.enabled = False
            self.fan_thread.join()
            #TODO: Actually stop fan
            print("Fan stoppped!")