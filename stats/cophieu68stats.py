import requests
import pandas as pd
from tabulate import tabulate
import urllib.request

# Constants
loginUrl = "http://www.cophieu68.vn/account/login.php"
exportListUrl = "http://www.cophieu68.vn/export.php"
exportUrl = "http://www.cophieu68.vn/export/excelfull.php?id=ACL"

# Get PHPSESSID
request = urllib.request.Request(loginUrl)
opener = urllib.request.build_opener()
response = opener.open(request)
if response.status == 200:
    phpSessId = str(response.getheader("Set-Cookie")).split(";")[0].split("=")[1]

    # Get CSVs
    request = urllib.request.Request(exportUrl)
    data = (
        ('username', 'dangki0705@gmail.com'),
        ('tpassword', '1gun2bound3'),
        ('ajax', 1),
        ('login', 1)
    )
    cookies = dict(
        PHPSESSID=phpSessId,
        cophieu68username='ZGFuZ2tpMDcwNUBnbWFpbC5jb20%3D',
        cophieu68password='YzVkY2I3NzczNDJmOTM3NWEwNmRkNWYxOWZhZWQwNjg%3D'
    )
    requests.post(exportUrl, data=data, cookies=cookies)
    response = requests.post(exportUrl, data=data, cookies=cookies)

    # Save CSVs
    remove_column_list = [13, 12, 11, 9, 8, 7, 5, 4, 3, 2, 0]
    with open('ACL.csv', 'w+') as f:
        lines = response.content.splitlines(True)
        for line in lines:
            items = str(line).split(",")
            for removeIdx in remove_column_list:
                items.pop(removeIdx)
            f.write(",".join(items) + "\n")
