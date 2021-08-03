import smtplib
from datetime import datetime
from pytz import timezone
import ast
from email.message import EmailMessage
import pandas as pd
from auindex import endpoint, emailuser, emailpwd
from myutils import *


class Email_Center:
    def __init__(self, access_auindex, debug=True):
        self.access_auindex = access_auindex
        self.debug = debug


    def send_mails(self):
        print("Starting send_mails()")
        current_syd_time = datetime.now(tz=timezone('Australia/Sydney'))
        start_date = add_days(current_syd_time, -120)
        date_detected = datetime_to_date_str(start_date, include="ymd")
        url = endpoint + "/new_filter_records?end_date="+date_detected+"&detected=True&filter_config_id=3"
        df = pd.DataFrame(self.access_auindex.request_new_filter_records(
            symbol=None, end_date=date_detected, detected="True", filter_config_id="3")).T
        if df.shape[0] == 0:
            return

        df['score'] = df['details'].map(lambda x: float(ast.literal_eval(x)['t_stats_volume']))
        df['score'][df['score'] > 100] = 100
        df = df[["symbol_id","end_date","score"]]
        df = df.rename(columns={"symbol_id": "Symbol","end_date": "Detected Date","score":"Score"})
        df = df.sort_values(by=['Detected Date']).reset_index(drop=True)
        EMAIL_ADDRESS = 'auindex@outlook.com'

        s = smtplib.SMTP("email-smtp.ap-southeast-2.amazonaws.com", 587)
        s.connect("email-smtp.ap-southeast-2.amazonaws.com", 587)
        s.starttls()
        s.login(emailuser, emailpwd)
        if self.debug:
            contacts = ['auindex@outlook.com']
        else:
            contacts = ['auindex@outlook.com']
        msg = EmailMessage()
        msg['Subject'] = 'AuIndex Stock Filter Report'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = ", ".join(contacts)

        msg.set_content('This is a plain text email')
        content = ("""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <!-- Latest compiled and minified CSS -->
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
                    <!-- Optional theme -->
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap-theme.min.css" integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ" crossorigin="anonymous">
                    <!-- Latest compiled and minified JavaScript -->
                    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
                </head>
                <body>
                    <div class="row" style="margin: 5px;">
                        <p>Dear Mark,</p>
                        <p>Here are the records detected to have abnormal trading volumes in the last 120 days. The higher the score, the higher the abnormality signal.</p>
                    </div>
                    <div class="row" style="margin: 5px;">
            """)

        df['Detected Date'] = pd.to_datetime(df['Detected Date'])
        groups = df.groupby(pd.Grouper(key='Detected Date', freq='M'))
        dfs = [group for _,group in groups]
        for i in range(-1, -len(dfs)-1, -1):
            tmp = dfs[i]
            content += tmp.sort_values(by=['Score'],ascending=False).to_html(index=0)
        
        content += """
                </div>
                <br /> 
                <div class="row" style="margin: 5px;">
                    <p>For more information, please visit AuIndex API: %s<p>
                    <p>Kind Regards,</p>
                    <p>AuIndex</p>
                </div>
            </body>
            </html>""" %(url)
        content = content.replace('<table border="1" class="dataframe">','<table border="1" class="col-md-2" style="margin: 8px;">')
        content = content.replace('<tr style="text-align: left;">','<tr style="text-align: center;">')
        msg.add_alternative(content, subtype='html')
        s.sendmail(from_addr=EMAIL_ADDRESS, to_addrs= contacts,msg = msg.as_bytes())
        print("Email sent to:", contacts)


if __name__ == "__main__":
    from access_auindex import Access_auindex
    access_auindex = Access_auindex()
    email = Email_Center(access_auindex=access_auindex, debug=True)
    email.send_mails()
