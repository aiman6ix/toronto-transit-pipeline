import sqlite3,time,random,math

con = sqlite3.connect("toronto_transit.db")
cur = con.cursor()
cooridnates = [
               (43.6734,-79.2858),  # Neville Park (Start)
               (43.6698,-79.3011),  # Woodbine
               (43.6583,-79.3452),  # Broadview
               (43.6523,-79.3792),  # Yonge
               (43.6487,-79.3965),  # Spadina
               (43.6444,-79.4191),  # Ossington
               (43.6291,-79.4791)    # Humber Loop
                      ]
vehicle_id = "TTC-501-A"
route_name = "501-Queen"
latitude = cooridnates[0][0]
longitude = cooridnates[0][1]
speed_kmh = 0
last_updated = 0
current_index = 0
target_index = 1
while True:
    last_updated = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    speed_kmh = random.randint(0,50)
    target_destination = cooridnates[target_index]
    lat_distance =  target_destination[0] - latitude
    lon_distance = target_destination[1] - longitude
    total_distance = math.sqrt(lat_distance**2 + lon_distance**2)
    lat_distance/=total_distance
    lon_distance/=total_distance
    latitude += lat_distance * (speed_kmh*0.00001)
    longitude += lon_distance * (speed_kmh*0.00001)
    if total_distance < 0.0005 :
        current_index+=1
        target_index+=1
        #if we have reached the end of the line
        if target_index >= len(cooridnates):
            current_index=0
            target_index = 1
            #coordinates reset when reaching the end of the line
            latitude = cooridnates[0][0]
            longitude = cooridnates[0][1]
        
    query = (vehicle_id,route_name ,latitude,longitude,speed_kmh,last_updated)
    query_history = (vehicle_id,latitude,longitude,speed_kmh,last_updated)
    cur.execute("""
    INSERT OR REPLACE INTO live_status(vehicle_id,route_name,latitude,longitude,speed_kmh,last_updated)
    VALUES (?,?,?,?,?,?)
                                               
                """, query)
    cur.execute("""
    INSERT INTO transit_history(vehicle_id,latitude,longitude,speed_kmh,recorded_at)
    VALUES (?,?,?,?,?)
    """,query_history)
    con.commit()
    time.sleep(6)