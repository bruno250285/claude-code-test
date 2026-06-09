import os
import sys
import requests
from dotenv import load_dotenv, set_key

ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_FILE)

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

AUTH_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/oauth/token"
API_BASE = "https://www.strava.com/api/v3"


def abort(msg):
    print(f"Error: {msg}")
    sys.exit(1)


def authorize():
    """One-time OAuth flow: print auth URL, collect code, exchange for tokens."""
    url = (
        f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code"
        f"&redirect_uri=http://localhost&approval_prompt=force"
        f"&scope=activity:read_all"
    )
    print("\nOpen this URL in your browser and approve access:\n")
    print(f"  {url}\n")
    print("After approving, you'll be redirected to http://localhost (the page won't load).")
    print("Copy the 'code' value from the URL bar and paste it below.")
    code = input("\nPaste the code here: ").strip()

    resp = requests.post(TOKEN_URL, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    })
    if not resp.ok:
        abort(f"Token exchange failed: {resp.text}")

    data = resp.json()
    save_tokens(data["access_token"], data["refresh_token"])
    return data["access_token"]


def refresh_access_token():
    """Use the refresh token to obtain a new access token."""
    resp = requests.post(TOKEN_URL, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
    })
    if not resp.ok:
        abort(f"Token refresh failed: {resp.text}")

    data = resp.json()
    save_tokens(data["access_token"], data["refresh_token"])
    return data["access_token"]


def save_tokens(access_token, refresh_token):
    set_key(ENV_FILE, "STRAVA_ACCESS_TOKEN", access_token)
    set_key(ENV_FILE, "STRAVA_REFRESH_TOKEN", refresh_token)


def get_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        abort("STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET must be set in .env")

    if not REFRESH_TOKEN:
        return authorize()

    return refresh_access_token()


def format_distance(meters):
    if meters >= 1000:
        return f"{meters / 1000:.2f} km"
    return f"{int(meters)} m"


def format_duration(seconds):
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m}m {s:02d}s"


def print_summary(activity):
    date = activity.get("start_date_local", "")[:10]
    print("\n--- Latest Strava Activity ---")
    print(f"  Name      : {activity.get('name')}")
    print(f"  Type      : {activity.get('sport_type', activity.get('type'))}")
    print(f"  Date      : {date}")
    print(f"  Distance  : {format_distance(activity.get('distance', 0))}")
    print(f"  Moving time: {format_duration(activity.get('moving_time', 0))}")
    print(f"  Elevation : {activity.get('total_elevation_gain', 0):.0f} m gain")
    print("-----------------------------\n")


def main():
    token = get_token()

    resp = requests.get(
        f"{API_BASE}/athlete/activities",
        headers={"Authorization": f"Bearer {token}"},
        params={"per_page": 1},
    )
    if not resp.ok:
        abort(f"API request failed: {resp.text}")

    activities = resp.json()
    if not activities:
        print("No activities found on your Strava account.")
        return

    print_summary(activities[0])


if __name__ == "__main__":
    main()
