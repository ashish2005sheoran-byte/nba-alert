import requests
import datetime
import pytz

# --- CONFIG ---
SIMPLEPUSH_KEY = "3D56JP"
BDL_API_KEY = "443751d1-9270-42c8-9f48-6655810b9dc5"
TARGET_MARGIN = 12

def send_alert(message):
    clean_msg = message.replace(" ", "%20")
    url = f"https://api.simplepush.io/send/{SIMPLEPUSH_KEY}/NBA_ALERT/{clean_msg}"
    requests.get(url)

def check_nba_halftime():
    # Set timezone to India to check exact time
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.datetime.now(ist)
    
    # FORCE ALARM AT 2:44 AM IST
    if now_ist.hour == 2 and now_ist.minute == 44:
        send_alert("TEST_ALARM_2_44_SUCCESSFUL")
        print("Scheduled test alarm sent!")

    # NORMAL NBA LOGIC
    today = datetime.date.today().isoformat()
    url = f"https://api.balldontlie.io/v1/games?dates[]={today}"
    headers = {"Authorization": BDL_API_KEY}
    
    try:
        response = requests.get(url, headers=headers).json()
        for game in response.get('data', []):
            status = game.get('status', '')
            if status == "Halftime":
                margin = abs(game['home_team_score'] - game['visitor_team_score'])
                if margin >= TARGET_MARGIN:
                    msg = f"Margin_{margin}_{game['visitor_team']['abbreviation']}_at_{game['home_team']['abbreviation']}"
                    send_alert(msg)
            print(f"Checked {game['home_team']['abbreviation']} - Status: {status}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_nba_halftime()
