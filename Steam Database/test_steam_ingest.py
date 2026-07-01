import requests
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost,1434;"
    "DATABASE=SteamDatabaseDEV;"
    "UID=sa;"
    "PWD=YourStrong!Passw0rd;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()

game_ids = [730, 570, 440, 578080, 271590]

for app_id in game_ids:
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    res = requests.get(url)
    data = res.json()

    game_data = data[str(app_id)]["data"]
    
    name = game_data["name"]
    is_free = game_data.get("is_free", 0)

    # -------------------------
    # INSERT GAME (ignore duplicates for now)
    # -------------------------
    cursor.execute("""
    IF NOT EXISTS (SELECT 1 FROM Games WHERE GameId = ?)
    INSERT INTO Games (GameId, Name, IsFree)
    VALUES (?, ?, ?)
    """,
    app_id, app_id, name, is_free)

    # -------------------------
    # INSERT SNAPSHOT
    # (Steam store API doesn't give live players,
    # so we fake snapshot for now — we fix later)
    # -------------------------
    cursor.execute("""
    INSERT INTO GameSnapshots (GameId, PlayersCurrent, SnapshotTime)
    VALUES (?, ?, GETDATE())
    """,
    app_id, 0)

conn.commit()

print("Done inserting Steam games")