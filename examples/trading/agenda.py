# IMPORTATIONS
import json
import logging

from degiro_connector.trading.api import API as TradingAPI
from degiro_connector.trading.models.trading_pb2 import (
    Agenda,
    Credentials,
)

# SETUP LOGGING LEVEL
logging.basicConfig(level=logging.DEBUG)

# SETUP CONFIG DICT
with open("config/config.json") as config_file:
    config_dict = json.load(config_file)

# SETUP CREDENTIALS
int_account = config_dict.get("int_account")
username = config_dict.get("username")
password = config_dict.get("password")
totp_secret_key = config_dict.get("totp_secret_key")
one_time_password = config_dict.get("one_time_password")

credentials = Credentials(
    int_account=int_account,
    username=username,
    password=password,
    totp_secret_key=totp_secret_key,
    one_time_password=one_time_password,
)

# SETUP TRADING API
trading_api = TradingAPI(credentials=credentials)

# CONNECT
trading_api.connect()

# SETUP REQUEST
request = Agenda.Request()
request.start_date.FromJsonString("2021-06-21T22:00:00Z")
request.end_date.FromJsonString("2021-11-28T23:00:00Z")
request.calendar_type = Agenda.CalendarType.DIVIDEND_CALENDAR
request.offset = 0
request.limit = 25  # 0 < limit <= 100

# FETCH DATA
agenda = trading_api.get_agenda(
    request=request,
    raw=False,
)

# DISPLAY AGENDA
print("Agenda :", agenda)
