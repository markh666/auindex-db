import json
import pandas as pd

from mydatabase.database import Database


class Filter_center(Database):
    def __init__(self) -> None:
        super().__init__()
    

    def get_filter_config_id(self, filter_name, configs):
        query = "SELECT c.id FROM filters_configs c where c.filter_name ='"+filter_name+"' and c.configs ='"+configs+"' ;"
        rows = self.select_query(query=query)
        return rows
    

    def add_filter(self, filter_name, description):
        query = "INSERT IGNORE INTO filters (name, description) VALUES (%s, %s);"
        val = (filter_name,description)
        self.insert_query(query, val)


    def add_filter_config(self, filter_name, configs):
        query = "INSERT IGNORE INTO filters_configs (filter_name, configs) VALUES (%s, %s) ;"
        val = (filter_name,configs)
        self.insert_query(query,val)
       

    def add_new_filter_record(self, symbol, record):
        json_configs = json.dumps(record["configs"])
        config_Id = self.get_filter_config_id(record["filter_name"], json_configs)
        
        if config_Id == []:
            print("add new config Id")
            config_Id = self.add_filter_config(record["filter_name"], json_configs)
        else:
            config_Id = config_Id[0][0]

        query = "INSERT IGNORE INTO new_filter_records (begin_date, end_date, detected, details, filter_name, filter_config_id, symbol_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        val = (record["begin_date"], record["end_date"],  str(record["detected"]),  json.dumps(record["details"]), str(record["filter_name"]), config_Id, symbol)
        self.insert_query(query, val)
