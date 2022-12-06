import sys
from datetime import datetime

import requests


with open('.sessioncookie', 'r') as f:
    session_token = f.read().strip()


member_id = "1194494"
url = "https://adventofcode.com/2022/leaderboard/private/view/212116.json"
headers = {"Cookie": "session=" + session_token}

data = None
if (r := requests.get(url, headers=headers)).status_code == 200:
    data = r.json()
else:
    sys.exit(f"Response {r.status_code}: {r.reason} \n{r.content}")

me = data["members"][member_id]

print("My Stats:")
for key in sorted(me["completion_day_level"]):
    print(f"\tDay {key}:")
    for star in sorted(me["completion_day_level"][key]):
        star_time = datetime.fromtimestamp(
            me["completion_day_level"][key][star]["get_star_ts"]
        )
        print(f"\t\tStar {star} Time: {star_time}")