# Task 1
import pandas as pd

df = pd.read_csv('ebike_data.csv')

df["bike_type"] = df["bike_type"].astype("category")
df["bike_type"].isna().sum()
df["bike_type"].unique()

df["frame_material"] = df["frame_material"].astype("category")
df["frame_material"].isna().sum()
df["frame_material"].unique()
df["frame_material"] = df["frame_material"].replace("STEel", "steel")

df['top_speed'].isna().sum()
df["top_speed"] = df["top_speed"].fillna(round(df["top_speed"].mean(), 2))

df['battery_type'] = df['battery_type'].astype('category')
df['battery_type'].unique()
df["battery_type"] = df["battery_type"].replace('-', "other")
#['li-ion', 'nimh', 'lead acid'].

df['motor_power'] = df['motor_power'].str[:-1]
df['motor_power'] = df['motor_power'].astype('float')
df['motor_power'].isna().sum()

clean_data = df

clean_data

# Task 2
import pandas as pd

df = pd.read_csv('ebike_data.csv')
bike_type_data = df.groupby("bike_type")[["production_cost", "assembly_time", "customer_score"]].mean()
bike_type_data = round(bike_type_data, 2)
bike_type_data = bike_type_data.rename(columns={
    "production_cost": "avg_production_cost",
    "assembly_time": "avg_assembly_time",
    "customer_score": "avg_customer_score"
})
bike_type_data