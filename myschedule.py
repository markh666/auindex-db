from datetime import datetime
from pytz import timezone
import traceback
import threading
from time import sleep
import threading

from myutils import *


class Schedule:
    def __init__(self, tasks, days_interval=1, hour=9, minute=0, second=0, microsecond=0, repeat=True, immediate_start=False ):
        self.tasks = tasks
        self.days_interval = days_interval
        self.hour = hour 
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        self.ended_signal = threading.Event()
        self.repeat = repeat
        self.paused = True
        self.ended = False
        self.started = False
        self.last_run_time = None
        self.next_run_time = None
        self.current_subtask = None
        self.immediate_start = immediate_start
        self.last_run_ok = None


    def run_task(self):
        if self.immediate_start == False:
            # make sure it will not immediate_start and auto start on weekdays
            current_syd_time = datetime.now(tz=timezone('Australia/Sydney'))
            current_hour = current_syd_time.hour
            current_weekday = current_syd_time.weekday()
            init_delay_days = 0
            if (current_weekday<=4) and (current_hour<self.hour):
                init_delay_days = 0
            elif (current_weekday<4) and (current_hour>self.hour):
                init_delay_days = 1
            elif (current_weekday>=4) and (current_hour>self.hour):
                init_delay_days = 7-current_weekday

            delay = self._get_delay(days_interval=init_delay_days)
            self.paused = True
            sleep(max(0, delay))
        while not self.ended_signal.is_set():
            try:
                current_syd_time = datetime.now(tz=timezone('Australia/Sydney'))
                current_weekday = current_syd_time.weekday()
                print("Current syd time:", current_syd_time)
                print("Current weekday:", current_weekday)
                if current_weekday < 5:
                    print("Starting schedule(s):")
                    self.paused = False

                    self.last_run_ok = False
                    self.last_run_time = current_syd_time
                    for task in self.tasks:
                        self.current_subtask = task
                        print("Current task:", task.__name__)
                        try:
                            task()
                        except Exception as e:
                            print(e)
                            traceback.print_exc()
                    self.last_run_ok = True
                    print("Today's schedules have finished.")
            except Exception:
                self.last_run_ok = False
                traceback.print_exc()
                # in production code you might want to have this instead of course:
                # logger.exception("Problem while executing repetitive task.")
            if self.repeat == False:
                break   

            self.current_subtask = None
            delay = self._get_delay()
            self.paused = True
            sleep(max(0, delay))
        self.ended = True

        
    def _get_delay(self, days_interval=1):
        current_syd_time = datetime.now(tz=timezone('Australia/Sydney'))
        next_run_time = add_days(current_syd_time, days=days_interval)
        self.next_run_time = next_run_time.replace(hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond)
        print("Next run syd time: ", str(self.next_run_time))
        delay = self.next_run_time - current_syd_time
        delay = delay.total_seconds()
        return delay


    def run_task_tread(self, kwargs=None):
        t = threading.Thread(target = self.run_task, kwargs = kwargs)
        t.daemon = True
        self.started = True
        t.start()
