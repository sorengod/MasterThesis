import pandas as pd
import requests

endpoints = {
    'spot_prices' : 'https://api.energidataservice.dk/dataset/Elspotprices?start=2021-01-01&end=2023-01-01&filter={"PriceArea":["DK1", "DK2", "SE3", "SE4", "NO2"]}&sort=HourDK asc'
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
    
    def pivot_table(self, index:str, columns:str, values:str):
        df = self.extract_columns_from_ColumnDictionary()
        pivot_table = df.pivot_table(index=index, columns=columns, values=values)
        return pivot_table


          
object = Energy_Data(f'{endpoints["spot_prices"]}')
df = object.extract_columns_from_ColumnDictionary()
df.to_excel("Spot_Prices.xlsx")

