DROP TABLE IF EXISTS live_status;
DROP TABLE IF EXISTS transit_history;

CREATE TABLE live_status (
    vehicle_id TEXT PRIMARY KEY,
    route_name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    speed_kmh INTEGER NOT NULL,
    last_updated TEXT NOT NULL
);

CREATE TABLE transit_history (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    speed_kmh INTEGER NOT NULL,
    recorded_at TEXT NOT NULL
);

-- Analytics Query 1: Rank Segments by Average Speed
SELECT 
    route_segment,
    speed_kmh,
    RANK() OVER (ORDER BY speed_kmh ASC) AS speed_rank
FROM route_performance_summary;

-- Analytics Query 2: Compute Cumulative Delay Seconds for Stuck Vehicles
SELECT
    time_delta_seconds,
    is_stuck,
    vehicle_id,
    recorded_at,
    SUM(time_delta_seconds) OVER (
        PARTITION BY vehicle_id
        ORDER BY recorded_at
    ) AS continuous_stuck_seconds 
FROM cleaned_transit_telemetry 
WHERE is_stuck = 1;