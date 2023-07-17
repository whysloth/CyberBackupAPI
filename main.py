import webapi

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

USERNAME = str(os.environ.get("USERNAME"))
PASSWORD = str(os.environ.get("PASSWORD"))

client = webapi.Client(username=USERNAME, password=PASSWORD)

print(client.location_summary_table())
print(client.active_alerts_table())
print(client.resource_summary_table())
print(client.daily_activity_table())
print(client.alerts_summary())
input()
