import requests
import time
from auindex import endpoint

class Access_auindex:
    def __init__(self, base_url=endpoint):
        self.base_url = base_url
    

    def request_new_watchlist(self):
        link = self.base_url + "new_watchlist"
        r = requests.get(link)
        if r.ok:
            return r.json()


    def request_prices(self, symbol=None, date_from=None, date_to=None):
        link = self.base_url + "prices"
        if symbol != None:
            link = link + "?symbol=" + symbol
        if (date_from != None) and (date_to == None):
            link += f"&date_from={date_from}"
        elif (date_from != None) and (date_to != None):
            link += f"&date_from={date_from}&date_to={date_to}"
        elif (date_from == None) and (date_to != None):
            link += f"&date_to={date_to}"
        
        try:
            r = requests.get(link)

        except requests.exceptions.ConnectionError:
            time.sleep(0.1)
            r = requests.get(link)

        if r.ok:
            return r.json()


    def request_recommendations(self, symbol=None):
        link = self.base_url + "recommendations"
        if symbol != None:
            link = link + "?symbol=" + symbol
        r = requests.get(link)
        if r.ok:
            return r.json()


    def request_latest_recommendations(self, symbol=None):
        link = self.base_url + "latest_recommendations"
        if symbol != None:
            link = link + "?symbol=" + symbol
        r = requests.get(link)
        if r.ok:
            return r.json()


    def request_balance_sheets(self, symbol=None):
        link = self.base_url + "balance_sheets"
        if symbol != None:
            link = link + "?symbol=" + symbol
        r = requests.get(link)
        if r.ok:
            return r.json()


    def request_income_statements(self, symbol=None):
        link = self.base_url + "income_statements"
        if symbol != None:
            link = link + "?symbol=" + symbol
        r = requests.get(link)
        if r.ok:
            return r.json()


    def request_cash_flows(self, symbol=None):
        link = self.base_url + "cash_flows"
        if symbol != None:
            link = link + "?symbol=" + symbol
        r = requests.get(link)
        if r.ok:
            return r.json()


    def request_short_interests(self, symbol=None):
        link = self.base_url + "short_interests"
        if symbol != None:
            link = link + "?symbol=" + symbol
        r = requests.get(link)
        if r.ok:
            return r.json()


    def request_ownerships(self, symbol=None):
        link = self.base_url + "ownerships"
        if symbol != None:
            link = link + "?symbol=" + symbol
        r = requests.get(link)
        if r.ok:
            return r.json()

    
    def request_new_filter_records(self, symbol, end_date, detected=None, filter_config_id=None):
        link = self.base_url + "new_filter_records"
        if symbol != None:
            if "?" not in link:
                link += "?"
            link += f"symbol_id={symbol}"
        if end_date != None:
            if "?" not in link:
                link += "?"
            else:
                link += "&"
            link += f"end_date>={end_date}"
        if detected != None:
            if "?" not in link:
                link += "?"
            else:
                link += "&"
            link += f"detected={str(detected)}"
        if filter_config_id != None:
            if "?" not in link:
                link += "?"
            else:
                link += "&"
            link += f"filter_config_id={filter_config_id}"

        r = requests.get(link)
        if r.ok:
            return r.json()
