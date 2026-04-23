name: NBA Halftime Alert
on:
  schedule:
    # This runs every 10 minutes (Cron format)
    - cron: '*/10 * * * *' 
  workflow_dispatch: # Allows you to test it manually

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install requests
      - name: Run bot
        run: python bot.py
