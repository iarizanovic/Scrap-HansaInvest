import time
from hansainvest import HansaInvest
from config import start_time_str, repeating_period

# Get start time in seconds
start_time: int = int(time.mktime(time.strptime(f'{time.strftime("%d.%m.%Y")} {start_time_str}', "%d.%m.%Y %H:%M")))

while True:
    # Calculate the waiting_period, so that start_time is not in past
    current_time: int = int(time.time())
    while start_time - current_time < 0:
        start_time += repeating_period
    waiting_period: int = start_time-current_time

    # Sleep time
    if waiting_period > 0:
        print(f"\x1b[1;34mWaiting {waiting_period} seconds.\x1b[0m")  # blue
        time.sleep(waiting_period)

    # Start scraping the HansaInvest WebSite
    HansaInvest().process()



