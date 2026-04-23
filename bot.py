import requests
import datetime

# --- YOUR DATA ---
SIMPLEPUSH_KEY = "3D56JP"
BDL_API_KEY = "443751d1-9270-42c8-9f48-6655810b9dc5"
TARGET_MARGIN = 12

def send_simplepush(message):
    # This uses the exact URL format you confirmed works
    # We replace spaces with %20 so the URL doesn't break
    clean_msg = message.replace(" ", "%20")
    test_url = f"https://api.simplepush.io/send/{SIMPLEPUSH_KEY}/NBA_ALERT/{clean_msg}"
    
    try:
        r = requests.get(test_url)
        print(f"Sent to Phone: {r.status_code}")
    except Exception as e:
        print(f"Failed to send: {e}")

def check_nba_games():
    # April 24, 2026
    today = datetime.date.today().isoformat()
    url = f"https://api.balldontlie.io/v1/games?dates[]={today}"
    headers = {"Authorization": BDL_API_KEY}
    
    try:
        response = requests.get(url, headers=headers).json()
        games = response.get('data', [])
        
        if not games:
            print("No games found for today yet.")
            return

        for game in games:
            home = game['home_team']['abbreviation']
            away = game['visitor_team']['abbreviation']
            status = game.get('status', '')
            
            print(f"Checking {away} @ {home} | Status: {status}")

            # Trigger only at Halftime
            if status == "Halftime":
                margin = abs(game['home_team_score'] - game['visitor_team_score'])
                
                if margin >= TARGET_MARGIN:
                    alert_text = f"BLOWOUT_{margin}_POINTS_{away}_AT_{home}"
                    send_simplepush(alert_text)
                    print(f"!!! ALERT TRIGGERED for {away}@{home} !!!")
                else:
                    print(f"Margin is {margin}. No alert needed.")

    except Exception as e:
        print(f"Error checking scores: {e}")

if __name__ == "__main__":
    check_nba_games()
