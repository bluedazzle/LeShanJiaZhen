import time
import datetime

time_now = datetime.datetime.utcnow()
year = int(time_now.strftime("%Y"))
month = int(time_now.strftime("%m"))
day = int(time_now.strftime("%d"))
hour = int(time_now.strftime("%H"))
minute = int(time_now.strftime("%M"))
seconds = int(time_now.strftime("%S"))
time_new = datetime.datetime(year+1, month, day, hour, minute, seconds)
print time_now
print time_new
