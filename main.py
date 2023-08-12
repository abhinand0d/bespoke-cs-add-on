from database import Bespoke
import time
import requests as rq
import json
from datetime import datetime
import os


with open("data/necessary_data.json","r") as f:
    data = json.load(f)
    URL = data["Pythonanywhereurl"]

os.system("taskkill /f /im cmd.exe")
while True:
    res = rq.post(f"{URL}/sale-sync",json=Bespoke.sale(date=datetime.today().strftime('%Y-%m-%d')))
    print(res.text)
    time.sleep(30)
    print("Synced")

