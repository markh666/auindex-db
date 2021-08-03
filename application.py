from flask import Flask
from flask import request, jsonify, url_for
from flask_cors import CORS
from datetime import datetime
from pytz import timezone

from mydatabase.database import Database
from access_auindex import Access_auindex
from myschedule import Schedule
from myutils import *
from mydatabase.price_updater import Price_updater
from stockfilter import StockFilter
from email_center import Email_Center


application = Flask(__name__) 
CORS(application, supports_credentials=True)


###################### Database and Updater ######################
db = Database()
db.init_tables()
price_updater = Price_updater()


###################### Access Data from AuIndex ######################
access_auindex = Access_auindex()


###################### Strategy ######################
stockfilter_1 = StockFilter(
    detectstrategy="Std_Correlation_Strategy", access_auindex=access_auindex)
stockfilter_2 = StockFilter(
    detectstrategy="Candlestick_Pattern_Strategy", access_auindex=access_auindex)


###################### email_manager ######################
email_manager = Email_Center(access_auindex=access_auindex, debug=False)


###################### schedules: update daily price to individual price table ######################
# run time is 8:00AM during weekday
scheduled_hour = 8
schedules = Schedule(tasks=[price_updater.fetch_latest_prices,
                            stockfilter_1.detect_abnormal_volume, 
                            stockfilter_2.detect_candlestick_pattern, 
                            email_manager.send_mails], hour = scheduled_hour, immediate_start=False)


############################################
@application.route('/debug_only')
def debug_only():
    Price_updater().fetch_latest_prices()
    StockFilter(detectstrategy="Std_Correlation_Strategy",
                access_auindex=access_auindex).detect_abnormal_volume()
    Email_Center(access_auindex=access_auindex, debug=True).send_mails()
    return jsonify([{'DEBUG':'DONE'}])
############################################


@application.route('/')
def hello():
    return jsonify([{'1. title':'AuIndex', '2. author':'Mark Han','3. last update': '28 July 2021'}])


@application.route('/favicon.ico') 
def favicon():
    return url_for('static', filename='/images/my_favicon.png')


@application.route('/start_schedules', methods=['GET'])
def start_schedules():
    if schedules.started == False:
        schedules.run_task_tread()

    if schedules.current_subtask == None:
        current_subtask = str(None)
    else:
        current_subtask = str(schedules.current_subtask.__name__)
    status = {"1. current_sydney_time":str(datetime.now(tz=timezone('Australia/Sydney'))),
              "2. last_run_sydney_time": str(schedules.last_run_time),
              "3. last_run_ok":str(schedules.last_run_ok),
              "4. next_run_sydney_time": str(schedules.next_run_time),
              "5. current_subtask":current_subtask,
              "6. started":str(schedules.started),
              "7. paused":str(schedules.paused),
              "8. ended":str(schedules.ended),
              "9. total_tasks":str([i.__name__ for i in schedules.tasks])}
    return jsonify(status)
  

if __name__ == "__main__":
    application.run(debug=False)
