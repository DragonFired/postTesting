#!/usr/bin/env python
__author__ = "Arana Fireheart"

import requests
from plantUtilities import uUrlEncode

dictionaryElement = {"Value1": "{0}".format(5), "Value2": "{0}".format("Very wet!")}

encodedData = uUrlEncode(dictionaryElement)
print(encodedData)


def email_alert(first, second, third):
    report = {}
    report["value1"] = first
    report["value2"] = second
    report["value3"] = third
    print(f"Encoded Dictionary: {uUrlEncode(report)}")
    webhookURL = "https://maker.ifttt.com/trigger/PlantTalk/with/key/oKQM5KSDAg9lAxclodsMonxnGBehfLm3dEmGe2aUMDB"
    response = requests.post(webhookURL, data=report)
    print(response.text)
    print(f"Sent: {report}")


a = "Gotta"
b = "have"
c = "water"
email_alert(a, b, c)
