import requests
print(requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v1/").status_code)