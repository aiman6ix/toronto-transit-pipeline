import pandas as pd
import sqlite3

#df=pd.DataFrame
con = sqlite3.connect("toronto_transit.db")
cur = con.cursor()

sql_string= """
               SELECT * FROM transit_history
            """

df = pd.read_sql_query(sql_string,con)
df['recorded_at'] = pd.to_datetime(df['recorded_at'])
df['time_delta'] = df['recorded_at'].diff()
df['time_delta_seconds'] = df['time_delta'].dt.total_seconds()
df = df.loc[df['time_delta_seconds'] < 20]
df['longitude'] = df['longitude'].astype(float)
df['latitude'] = df['latitude'].astype(float)
df['speed_kmh'] = df['speed_kmh'].astype(int)
df['is_stuck'] = 0
df.loc[
    (df['longitude'] ==df['longitude'].shift(1)) & (df['latitude']==df['latitude'].shift(1)) & (df['speed_kmh']==0)
,'is_stuck'] = 1
cooridnates = [
               -79.4791,  # Humber
               -79.4191,  # Ossington
               -79.3965,  # Spadina
               -79.3792,  # Yonge
               -79.3452,  # Broadview
               -79.3011,  # Woodbine
               -79.2858,  # Neville Park
                      ]
segment_lab = ['Ossington -->Humber ','Spadina -->Ossington','Yonge --> Spadina','Broadview --> Yonge','Woodbine --> Broadview','Neville Park --> Woodbine']

df['route_segment'] = pd.cut(df['longitude'],bins=cooridnates,labels=segment_lab,include_lowest=True )

df_summary = df.groupby('route_segment').agg({
    'time_delta_seconds':'sum',
    'speed_kmh':'mean',
    'is_stuck':lambda x: (x == 1).sum(),
    'vehicle_id':'count'
    }).reset_index()
df_summary.rename(columns={'is_stuck': 'total_stuck_incidents'}, inplace=True)
df.to_sql(
    name='cleaned_transit_telemetry',
    con=con,
    if_exists="replace",
    index=False
)
df_summary.to_sql(
    name='route_performance_summary',
    con=con,
    if_exists="replace",
    index=False
)
# Print raw history records loaded from SQLite
print("Raw Telemetry History:")
print(df[['vehicle_id', 'latitude', 'longitude', 'speed_kmh', 'recorded_at']].head(10))
print(df_summary)
con.close()