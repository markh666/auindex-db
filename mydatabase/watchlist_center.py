from mydatabase.database import Database


class Wathlist_center(Database):
    def __init__(self) -> None:
        super().__init__()
    

    """
    select all symbols from watchlist table
    """
    def select_watchlist(self) -> list:
        query = "select id from watchlist;"
        rows = self.select_query(query)
        watchlist = [symbol[0] for symbol in rows]

        return watchlist


    """
    insert given symbols to watchlist
    """
    def insert_watchlist_by_symbols(self, symbols:list) -> None:
        query = "INSERT ignore INTO watchlist (id) VALUES (%s);"
        val = [tuple([symbol]) for symbol in symbols]
        self.insert_query(query, val)
