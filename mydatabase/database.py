import mysql.connector
from sqlalchemy import create_engine
import time
from auindex import dbhost, dbuser, dbpwd


class Database:
    def __init__(self, host=dbhost, user=dbuser, passwd=dbpwd, database="datacenter", port=3306):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.port = port


    def make_connection(self):
        conn = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                port = self.port,
                database = self.database
            )
        cursor = conn.cursor()
        
        return conn, cursor
  

    def select_query(self, query):
        try:
            conn, cursor = self.make_connection()
            cursor.execute(query)
            rows = cursor.fetchall() 
        except Exception as e:
            print(e)
            time.sleep(0.1)
            print("########### Re-try select_query() ###########")
            conn, cursor = self.make_connection()
            cursor.execute(query)
            rows = cursor.fetchall() 
        finally:
            cursor.close() 
            conn.close()
        return rows
    
    
    def insert_query(self, query, val=None):
        try:
            conn, cursor = self.make_connection()
            if type(val) is list: 
                cursor.executemany(query, val)
            elif type(val) is tuple: 
                cursor.execute(query, val)
            else:
                cursor.execute(query)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()

    
    def init_tables(self):
        #no tables needed to be created by AuIndex in the beginning
        try:
            conn, cursor = self.make_connection()

            query = """CREATE TABLE IF NOT EXISTS emails (
                        email varchar(255) NOT NULL,
                        name varchar(255) NOT NULL,
                        PRIMARY KEY (email)
                    );"""
            self.insert_query(query)

            query = """ CREATE TABLE IF NOT EXISTS filters (
                            name VARCHAR(255) PRIMARY KEY,
                            description VARCHAR(255)
                        ); """
            self.insert_query(query)

            query = """ CREATE TABLE IF NOT EXISTS filters_configs (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            configs VARCHAR(255),
                            filter_name VARCHAR(255),
                            FOREIGN KEY (filter_name) REFERENCES filters (name)
                        ); """ 
            self.insert_query(query)

            query = """CREATE TABLE IF NOT EXISTS new_filter_records (
                            begin_date VARCHAR(50) NOT NULL,
                            end_date VARCHAR(50) NOT NULL,
                            detected VARCHAR(10) NOT NULL,
                            details VARCHAR(255) NOT NULL,
                            filter_name VARCHAR(100) NOT NULL,
                            filter_config_id INT NOT NULL,
                            symbol_id VARCHAR(50) NOT NULL,
                            PRIMARY KEY (begin_date, end_date, detected, filter_name, filter_config_id, symbol_id),
                            FOREIGN KEY (filter_name) REFERENCES filters (name),
                            FOREIGN KEY (filter_config_id) REFERENCES filters_configs (id),
                            FOREIGN KEY (symbol_id) REFERENCES watchlist (id)
                        );"""
            self.insert_query(query)

        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()
    

    def create_sqlalchemy_engine(self):
        conn_str = f"mysql+mysqlconnector://{self.user}:{self.passwd}@{self.host}:3306/{self.database}"
        engine = create_engine(conn_str, echo=False)

        return engine
