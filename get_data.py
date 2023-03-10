import pandas as pd
import requests

endpoints = {
    'Spot_Prices' : 'https://api.energidataservice.dk/dataset/Elspotprices?start=2018-01-01&end=2023-01-01&filter={"PriceArea":["DK1", "DK2", "SE3", "SE4", "NO2"]}&sort=HourDK asc',
    'Transmission' : 'https://api.energidataservice.dk/dataset/Transmissionlines?start=2018-01-01&end=2023-01-01&sort=HourDK asc', 
    'Production&Consumption_DK1' : 'https://api.energidataservice.dk/dataset/ProductionConsumptionSettlement?start=2018-01-01&end=2023-01-01&filter={"PriceArea":"DK1"}&sort=HourDK asc',
    'Production&Consumption_DK2' : 'https://api.energidataservice.dk/dataset/ProductionConsumptionSettlement?start=2018-01-01&end=2023-01-01&filter={"PriceArea":"DK2"}&sort=HourDK asc'
}


class Energy_Data:

    def __init__ (self, url:str):
        self.url = url
    
    def get_data_from_api(self):
        response = requests.get(
        url=self.url)
        result = response.json()
        return result

    def create_df_from_request(self):
        raw_json = self.get_data_from_api()
        df = pd.DataFrame.from_dict(raw_json)
        return df

    def extract_columns_from_ColumnDictionary(self):
        df = self.create_df_from_request()
        df = df['records'].apply(pd.Series)
        return df

    def construct_GridFlow_column_and_pivot(self, from_area:str, to_area:str):
        df = self.extract_columns_from_ColumnDictionary()
        df['GridFlow'] = df[from_area] + "-->" + df[to_area]
        df = df.drop(columns=[f'{from_area}', f'{to_area}'])
        return df

    def pivot_df(self, index:str, columns:str, values:str):
        df = self.extract_columns_from_ColumnDictionary()
        pivot_table = df.pivot_table(index=index, columns=columns, values=values)
        return df
def pivot_df(input_df:pd.DataFrame, index, columns, values):
    df = input_df.pivot_table(index=index, columns=columns, values=values)
    return df 



object = Energy_Data(f'{endpoints["Production&Consumption_DK2"]}')
df = object.extract_columns_from_ColumnDictionary()
df.to_pickle("Production&Consumption_DK2.pkl")
print("DONE")


#new_df = pivot_df(df, index='HourDK', columns='GridFlow', values='ScheduledExchangeDayAhead')
#new_df.to_pickle("data/ScheduledExchangeDayAhead.pkl")


