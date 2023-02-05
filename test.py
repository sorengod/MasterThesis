import pandas as pd


df = pd.read_excel("Spot_Prices.xlsx")
df = df.pivot_table(index='HourDK', columns='GridFlow', values='ImportCapacity')
print(df)
