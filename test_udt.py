import imp


import re

test_string = "ABC/USDT"

if re.match(r"(.+/USDT)$", test_string):
    print("hha")
