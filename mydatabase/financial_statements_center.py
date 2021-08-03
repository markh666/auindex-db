import pandas as pd

from mydatabase.database import Database


class Financial_statements_center(Database):
    def __init__(self) -> None:
        super().__init__()


    def insert_balance_sheets(self, df):
        df = df.fillna('')
        query = "INSERT ignore INTO balance_sheets (symbol,date,intangible_assets,capital_surplus,total_liab,total_stockholder_equity,minority_interest,other_current_liab,total_assets,common_stock,other_current_assets,retained_earnings,other_liab,good_will,treasury_stock,other_assets,cash,total_current_liabilities,deferred_long_term_asset_charges,short_long_term_debt,other_stockholder_equity,property_plant_equipment,total_current_assets,long_term_investments,net_tangible_assets,short_term_investments,net_receivables,long_term_debt,inventory,accounts_payable) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"  
        val = [tuple(x) for x in df.to_numpy()]
        self.insert_query(query, val)


    def select_balance_sheets_by_symbol(self, symbol):
        query = f"SELECT * from balance_sheets WHERE symbol = '{symbol}' ORDER BY date DESC;"
        rows = self.select_query(query)
        columns = ['symbol','date','intangible_assets','capital_surplus','total_liab','total_stockholder_equity','minority_interest','other_current_liab','total_assets','common_stock','other_current_assets','retained_earnings','other_liab','good_will','treasury_stock','other_assets','cash','total_current_liabilities','deferred_long_term_asset_charges','short_long_term_debt','other_stockholder_equity','property_plant_equipment','total_current_assets','long_term_investments','net_tangible_assets','short_term_investments','net_receivables','long_term_debt','inventory','accounts_payable']
        df = pd.DataFrame(rows, columns=columns)
        return df


    def insert_income_statements(self, df):
        df = df.fillna('')
        query = "INSERT ignore INTO income_statements (symbol,date,research_development,effect_of_accounting_charges,income_before_tax,minority_interest,net_income,selling_general_administrative,gross_profit,ebit,operating_income,other_operating_expenses,interest_expense,extraordinary_items,non_recurring,other_items,income_tax_expense,total_revenue,total_operating_expenses,cost_of_revenue,total_other_income_expense_net,discontinued_operations,net_income_from_continuing_ops,net_income_applicable_to_common_shares) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"    
        val = [tuple(x) for x in df.to_numpy()]
        self.insert_query(query, val)


    def select_income_statements_by_symbol(self, symbol):
        query = f"SELECT * from income_statements WHERE symbol = '{symbol}' ORDER BY date DESC;"
        rows = self.select_query(query)
        columns = ['symbol', 'date', 'research_development', 'effect_of_accounting_charges', 'income_before_tax', 'minority_interest', 'net_income', 'selling_general_administrative', 'gross_profit', 'ebit', 'operating_income', 'other_operating_expenses', 'interest_expense', 'extraordinary_items', 'non_recurring', 'other_items', 'income_tax_expense', 'total_revenue', 'total_operating_expenses', 'cost_of_revenue', 'total_other_income_expense_net', 'discontinued_operations', 'net_income_from_continuing_ops', 'net_income_applicable_to_common_shares']
        df = pd.DataFrame(rows, columns=columns)
        return df
    

    def insert_cash_flows(self, df):
        df = df.fillna('')
        query = "INSERT ignore INTO cash_flows (symbol,date,investments,change_to_liabilities,total_cashflows_from_investing_activities,net_borrowings,total_cash_from_financing_activities,change_to_operating_activities,issuance_of_stock,net_income,change_in_cash,repurchase_of_stock,effect_of_exchange_rate,total_cash_from_operating_activities,depreciation,other_cashflows_from_investing_activities,dividends_paid,change_to_inventory,change_to_account_receivables,other_cashflows_from_financing_activities,change_to_netincome,capital_expenditures) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"  
        val = [tuple(x) for x in df.to_numpy()]
        self.insert_query(query, val)


    def select_cash_flows_by_symbol(self, symbol):
        query = f"SELECT * from cash_flows WHERE symbol = '{symbol}' ORDER BY date DESC;"
        rows = self.select_query(query)
        columns = ['symbol','date','investments','change_to_liabilities','total_cashflows_from_investing_activities','net_borrowings','total_cash_from_financing_activities','change_to_operating_activities','issuance_of_stock','net_income','change_in_cash','repurchase_of_stock','effect_of_exchange_rate','total_cash_from_operating_activities','depreciation','other_cashflows_from_investing_activities','dividends_paid','change_to_inventory','change_to_account_receivables','other_cashflows_from_financing_activities','change_to_netincome','capital_expenditures']
        df = pd.DataFrame(rows, columns=columns)
        return df


    def select_short_interests_by_symbol(self, symbol):
        query = f"SELECT * from short_interests WHERE symbol = '{symbol}' ORDER BY date DESC;"
        rows = self.select_query(query)
        columns = ['symbol','date','SHORT_INT','SHORT_SELL_NUM_SHARES','LAST_PRICE','VOLUME','SHORT_INT_RATIO']
        df = pd.DataFrame(rows, columns=columns)
        return df
    

    def select_ownerships_by_symbol(self, symbol):
        query = f"SELECT * from ownerships WHERE symbol = '{symbol}' ORDER BY percent_outstanding DESC;"
        rows = self.select_query(query)
        columns = ["symbol","collected_date","holder_name","portfolio_name","holder_id","position","position_change","filing_date","filing_source","insider_status","percent_outstanding","institution_type","metro_area","country","ticker","company_identifier"]
        df = pd.DataFrame(rows, columns=columns)
        latest_date = df.collected_date.max()
        latest_df = df[df.collected_date==latest_date].reset_index(drop=True)
        return latest_df
