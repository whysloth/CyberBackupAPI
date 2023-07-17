import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

HOST = str(os.environ.get("HOST"))
PORT = int(os.environ.get("PORT"))

AUTH_URL = "http://%s:%d/idp/token" % (HOST, PORT)

AUTH_PAYLOAD = {
    "grant_type": "password",
    "password": "",
    "username": ""
}

AUTH_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded"
}

ALERTS_SUMMARY_URL = "http://%s:%d/am/api/1/playbook/call/alerts_summary"  % (HOST, PORT)

DAILY_ACTIVITY_TABLE_URL = "http://%s:%d/am/api/1/playbook/call/daily_activity_table"  % (HOST, PORT)

LOCATION_SUMMARY_TABLE_URL = "http://%s:%d/am/api/1/playbook/call/location_summary_table"  % (HOST, PORT)

ACTIVE_ALERTS_TABLE_URL = "http://%s:%d/am/api/1/playbook/call/active_alerts_table"  % (HOST, PORT)

RESOURCE_SUMMARY_TABLE_URL = "http://%s:%d/am/api/1/playbook/call/resource_summary_table"  % (HOST, PORT)


AUTHORIZATION_TOKEN_HEADER = {
    "Authorization": "Bearer "
}

__all__ = [
    AUTH_URL, AUTH_HEADERS, AUTH_PAYLOAD,
    ALERTS_SUMMARY_URL,
    DAILY_ACTIVITY_TABLE_URL,
    LOCATION_SUMMARY_TABLE_URL,
    ACTIVE_ALERTS_TABLE_URL,
    RESOURCE_SUMMARY_TABLE_URL,
    AUTHORIZATION_TOKEN_HEADER,
    HOST, PORT
]
