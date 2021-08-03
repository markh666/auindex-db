import pandas as pd
from time import sleep
from sqlalchemy.exc import IntegrityError

from mydatabase.database import Database



class Price_center(Database):
    def __init__(self) -> None:
        super().__init__()
        self.engine = self.create_sqlalchemy_engine()


    def create_price_table(self, symbol):
        query = f'''CREATE TABLE IF NOT EXISTS {symbol} (
                    time DATE,
                    open FLOAT,
                    high FLOAT,
                    low FLOAT,
                    close FLOAT,
                    adj_close FLOAT,
                    volume INT,
                    PRIMARY KEY (time)
                );'''
        
        try:
            self.insert_query(query)
        except UnboundLocalError:
            sleep(5)
            self.insert_query(query)


    # def insert_price(self, symbol, hist):
    #     symbol = symbol.lower()
    #     self.create_price_table(symbol)

    #     hist.loc[:, "time"] = hist.loc[:, "time"].apply(str)
    #     query = f"INSERT ignore INTO {symbol} (time, open, high, low, close, adj_close, volume) VALUES (%s, %s ,%s, %s, %s, %s, %s);"  
    #     val = [tuple(x) for x in hist.to_numpy()]
    #     self.insert_query(query, val)


    def insert_price(self, symbol, hist, all_price_tables_exist):
        # each symbol table's name is lower case due to pandas.to_sql() problem
        symbol = symbol.lower()
        self.create_price_table(symbol)

        insert_again = False
        try:
            if all_price_tables_exist:
                current_update_start_date = hist.time[0]
                pre_df = pd.read_sql_query(sql=f"select * from {symbol} where time >= '{current_update_start_date}'", con=self.engine)
            else:
                pre_df = pd.read_sql_query(sql=f"select * from {symbol}", con=self.engine)

            if pre_df.shape[0] != 0:
                current_update_last_date = hist.time.iloc[-1]
                pre_df_last_date = pre_df.time.iloc[-1]
                if current_update_last_date <= pre_df_last_date:
                    return False

            non_duplicate_part = pd.concat([pre_df, hist]).drop_duplicates(keep=False)
            non_duplicate_part.time = non_duplicate_part.time.apply(str)

            # DEBUG
            # print("pre_df:", pre_df)
            # print("hist:", hist)
            # print("non_duplicate_part:", non_duplicate_part)
            # print("\n")

            if non_duplicate_part.shape[0] == 0:
                return False
            non_duplicate_part.to_sql(symbol, con=self.engine, if_exists='append', index=False)
        # catch (mysql.connector.errors.IntegrityError) 1062 (23000): Duplicate entry
        except IntegrityError as e:
            print("\n######################### Error Occured #########################")
            print(e, f"{symbol} needs to try again!")
            print("######################### Error Occured #########################\n")
            insert_again = True
        
        return insert_again
            
    
    def select_prices_by_symbol(self, symbol):
        # each symbol table's name is lower case due to pandas.to_sql() problem
        symbol = symbol.lower()
        query = f"SELECT * from {symbol} ORDER BY time DESC;"
        rows = self.select_query(query)
        columns = ["time", "open", "high", "low", "close", "adj_close", "volume"]
        df = pd.DataFrame(rows, columns=columns)
        return df
