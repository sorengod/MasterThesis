import requests
import pandas as pd
import json

headers = {
    'X-Gravitee-Api-Key': '3e504790-5fb0-47ac-b785-dbccbdf1a15f'
}

response = requests.get('https://dmigw.govcloud.dk/v2/metObs/collections/observation/items?parameterId=wind_speed_past1h&stationId=06149&datetime=2018-01-01T00:00:00Z/2022-12-31T00:00:00Z&limit=50000', headers=headers)
result = response.json()
json_formatted_str = json.dumps(result, indent=2)


d = result['features']

df = pd.DataFrame.from_dict(d)

df = df['properties'].apply(pd.Series)
df = df.sort_values(by=['observed'])
df.to_pickle("data/MeanWindPower1h_Gedser.pkl")
print(df)


