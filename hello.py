import time

dt = "2020-06-17 00:00:00"
ts = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
tt = time.mktime(ts)
print( tt )
print(round( tt * 1000))
print(int(round(tt * 1000)))
print(time.time())
print( time.time() * 1000)
print( round( time.time() * 1000) )