#!/usr/bin/python
#
#  Author: Stephen Hilt
#  Purpose: To convert hc911.org alerts to slack messages
#  version: 0.2 
#  Notes: Fixed issue with new hc911.org where the JSON file is no longer in use. 
#
########################################
from time import strftime
from lxml import etree
import urllib
import sys

def post_slack(API,chid,message,username):
        url = "https://slack.com/api/chat.postMessage?token={}&channel={}&text={}&username={}&pretty=1".format(API,chid,message,username)
        u = urllib.urlopen(url)
        response = u.read()
        return response

url = "https://www.hc911.org/active_incidents/echo_public_incidents.php"
API = 'API_HERE'
u = urllib.urlopen(url)
response = u.read()

response = "<table>" + response + "</table>"

hour = strftime("%I").lstrip('0')
#24 hour time needed for am/pm matching of the string from hc911.org
t4hour = strftime("%H")
#if its over 11, then its pm else am
if int(t4hour) > 11:
        mn = "PM"
else:
        mn = "AM"
# minute minus 5, the time between 'created_str' and current time is around a 5min delta
min = int(strftime("%M")) -2
# if after the -5 we have a negative number then we need to make this the previous hour
if min < 0:
        min = 60 - abs(min)
        hour = str(int(hour) - 1)
min = "{0:0=2d}".format(min)

table = etree.HTML(response).find("body/table")
rows = iter(table)
headers = [col.text for col in next(rows)]
for row in rows:
    values = [col.text for col in row]
    time = values[1]
    date = time.split(" ")
    newtime = date[1].split(":")
    responder = str(values[3])
    address = str(values[6])
    event = str(values[2])
    type = str(values[4])
    link = str(values[5])
    if newtime[1] == min:
        if newtime[0] == hour:
            if date[2] == mn:
                message = time +  " _*" + type + "*_ - " + event + " - " + responder + " - _* " + address + "*_"
                #slack.chat.post_message('#hc911', str(values[3]) + " - " + str(values[6]) + " - " + str(values[2]) + " _*STATUS*_ " + str(values[4]), username="hc911bot", icon_emoji=":police_car:")
                post_slack(API,'C4FFZV0QG', message, "hc911bot")




sys.exit()
