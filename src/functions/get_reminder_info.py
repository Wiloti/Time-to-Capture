from datetime import datetime, timedelta
import requests

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"}

# fetching data to create event reminders from now until 1 year
def get_reminder_info() -> list:
    event_list = []
    start = round(datetime.now().timestamp())
    finish = round((datetime.now() + timedelta(365)).timestamp())
    req = requests.get(f"https://ctftime.org/api/v1/events/?limit=100&start={start}&finish={finish}", headers=headers)
    data = req.json()
    # stop at 25 due to Discord limitation
    for event in range(0, 25):
        event_list.append(dict(event=data[event]["title"],
                               start_date=f"{data[event]['start']}",
                               finish_date=f"{data[event]['finish']}",
                               url=data[event]["url"],
                               description=data[event]["description"]))
    return event_list
get_reminder_info()
