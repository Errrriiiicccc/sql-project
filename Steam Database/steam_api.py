import requests

import json

STEAM_API = {
    # Game metadata (name, price, genres, etc.)
    "app_details": "https://store.steampowered.com/api/appdetails?appids={app_id}",

    # Current live player count
    "current_players": "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}",

    # Full Steam app list (IDs + names only)
    "app_list": "https://api.steampowered.com/ISteamApps/GetAppList/v2/",


    # Steam store search (HTML, not structured API)
    "store_search": "https://store.steampowered.com/search/?term={query}"
}

def read_game(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    res = requests.get(url)
    data = res.json()

    game = data[str(app_id)]["data"]

    return {
        "id": app_id,
        "name": game["name"],
        "is_free": game.get("is_free", False)
    }

def test_read_game():
    game = read_game(730)
    assert game["id"] == 730
    assert game["name"] == "Counter-Strike 2"
    assert game["is_free"] is True

#######

# test_read_game()

#######


def steam_api_help(print_result=False, run_examples=False):
    def pretty(obj):
        return json.dumps(obj, indent=2)[:800]  # keep readable + not massive

    endpoints = {
        "App Details (Game Info)": {
            "description": "Get full metadata about a Steam game (name, price, genres, etc.)",
            "url": STEAM_API["app_details"].format(app_id=730),
            "example": lambda: requests.get(
                STEAM_API["app_details"].format(app_id=730)
            ).json()
        },

        "Current Players": {
            "description": "Get live player count for a game",
            "url": STEAM_API["current_players"].format(app_id=730),
            "example": lambda: requests.get(
                STEAM_API["current_players"].format(app_id=730)
            ).json()
        },

        "App List (All Games)": {
            "description": "List of all Steam games (app IDs + names only)",
            "url": STEAM_API["app_list"],
            "example": lambda: requests.get(
                STEAM_API["app_list"]
            ).json()["applist"]["apps"][:3]
        },

        "Store Search": {
            "description": "Search Steam store (returns HTML, not structured JSON)",
            "url": STEAM_API["store_search"].format(query="counter strike"),
            "example": None
        }
    }

    print("\n================ STEAM API OVERVIEW ================\n")

    for name, info in endpoints.items():
        print(f"🔹 {name}")
        print(f"   Description: {info['description']}")
        print(f"   URL: {info['url']}")

        if run_examples and info["example"]:
            try:
                result = info["example"]()
                print("   Example Output:")
                print(pretty(result))
            except Exception as e:
                print("   Example Output: ERROR ->", e)

        print("\n----------------------------------------------------\n")

    print("====================================================\n")

    return endpoints

# steam_api_help(print_result=True, run_examples=True)
def get_all_games():
    url = STEAM_API["app_list"]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print("Request failed:", res.status_code)
        return []

    try:
        data = res.json()
    except Exception:
        print("Not JSON response:")
        print(res.text[:300])
        return []

    return data["applist"]["apps"]

print(get_all_games()[:5])  # Print first 5 games for testing