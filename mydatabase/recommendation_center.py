import pandas as pd

from mydatabase.database import Database


class Recommendation_center(Database):
    def __init__(self) -> None:
        super().__init__()
    

    def insert_rating_firms(self, firms):
        query = "INSERT ignore INTO firms (firm_name) VALUES (%s);"
        val = [tuple([firm]) for firm in firms]
        self.insert_query(query, val)

    
    def insert_recommendations(self, df):
        firms = list(set(df.firm_name))
        self.insert_rating_firms(firms)

        query = "INSERT ignore INTO recommendations (symbol, firm_name, analyst, recommendation, rating, action_code, target_price,period,date,barr,1_year_return) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"  
        val = [tuple(x) for x in df.to_numpy()]
        self.insert_query(query, val)


    """ 
    select the latest recommendations by a given symbol

    Args:
        symbols (list): a list of symbol

    Returns:
        recommendations (df): a dataframe containing the last recommendations of a given symbol
    """
    def select_recommendations_by_symbol(self, symbol) -> pd.DataFrame:
        query = f"SELECT * from recommendations WHERE symbol = '{symbol}';"
        rows = self.select_query(query)
        columns = ["symbol","firm_name","analyst","recommendation","rating","action_code","target_price","period","date","barr","1_year_return"]
        recommendations = pd.DataFrame(rows, columns=columns)
        return recommendations
    

    def select_latest_recommendations_by_symbol(self, symbol) -> pd.DataFrame:
        query = f"SELECT * from recommendations WHERE symbol = '{symbol}';"
        rows = self.select_query(query)
        columns = ["symbol","firm_name","analyst","recommendation","rating","action_code","target_price","period","date","barr","1_year_return"]
        df = pd.DataFrame(rows, columns=columns)
        df = df.sort_values(by='date', ascending=False)
        df = df.drop_duplicates(subset='firm_name', keep='first')
        df = df.reset_index(drop=True)
        return df

    
    # def get_latest_recommendations(self, symbols=[]): 
    #     query = "SELECT * from recommendations"
    #     if (len(symbols) != 0 ):
    #         symbols = ",".join(symbols)
    #         query += " WHERE symbol IN ("+symbols+")"
    #         query += " WHERE symbol IN ("+query+")"
    #     query += ";"

    #     return self.select_query(query)
