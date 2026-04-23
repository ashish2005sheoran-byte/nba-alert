import requests
import datetime

# --- UPDATED KEYS ---
SIMPLEPUSH_KEY = "3D56JP"  # This is your 6-char Simplepush Key
BDL_API_KEY = "443751d1-9270-42c8-9f48-6655810b9dc5"  # This is your Balldontlie API Key
TARGET_MARGIN = 12

def check_nba_halftime():
    # Gets today's date in YYYY-MM-DD
    today = datetime.date.today().isoformat()
    url = f"https://api.balldontlie.io/v1/games?dates[]={today}"
    headers = {"Authorization": BDL_API_KEY}
    
    try:
        response = requests.get(url, headers=headers).json()
        
        # Check if we got data back
        if 'data' not in response:
            print("No games found for today yet.")
            return

        for game in response['data']:
            # Log progress for your GitHub Actions logs
            home_abbr = game['home_team']['abbreviation']
            visitor_abbr = game['visitor_team']['abbreviation']
            status = game.get('status', '')
            
            print(f"Checking {visitor_abbr} @ {home_abbr} - Status: {status}")

            # Trigger only if status is 'Halftime'
            if status == "Halftime":
                home_score = game['home_team_score']
                visitor_score = game['visitor_team_score']
                margin = abs(home_score - visitor_score)
                
                if margin >= TARGET_MARGIN:
                    msg = f"NBA BLOWOUT: {visitor_abbr} @ {home_abbr} | Margin: {margin}"
                    # Send alert to your phone
                    # We use 'event=critical' to help bypass some DND settings
                    requests.get(f"https://simplepush.io/send/{SIMPLEPUSH_KEY}/NBA_ALERT/{msg}?event=critical")
                    print(f"!!! ALERT SENT: {msg} !!!")
                else:
                    print(f"Margin is only {margin}. No alert sent.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_nba_halftime()
