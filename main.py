import os
import time
from dotenv import load_dotenv
from twitter.account import Account
from twitter.scraper import Scraper

load_dotenv()

cookies = {
    "auth_token": os.getenv("AUTH_TOKEN"),
    "ct0": os.getenv("CT0")
}

account = Account(cookies=cookies)
scraper = Scraper(cookies=cookies)

user = scraper.users(["cvdite"])[0]
user_id = int(user["data"]["user"]["result"]["rest_id"])

following = scraper.following([user_id])
all_following = []
for follow in following:
    for instruction in follow["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]:
        if instruction["type"] == "TimelineAddEntries":
            for entry in instruction["entries"]:
                if entry["entryId"].startswith("user"):
                    all_following.append(entry["content"]["itemContent"]["user_results"]["result"])


for user in reversed(all_following):
    account.follow(int(user["rest_id"]))
    print(f"[!] Followed {user['screen_name']}")
    time.sleep(1)
