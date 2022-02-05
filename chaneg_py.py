import datetime

timeNow = datetime.datetime.now()
auto_time = int(timeNow.strftime("%M"))
print(auto_time)
print(type(auto_time))

if auto_time in [51, 52, 53, 54, 55]:
    print("hha")
