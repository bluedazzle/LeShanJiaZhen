import time
import datetime

t = time.strptime("2012-04-04", "%Y-%m-%d")
time_mine = datetime.datetime(*t[:6])
print t
print time_mine
