 # coding: utf-8
import os
import sys

sd = os.path.dirname(__file__)
sys.path.append(sd + '/lib')

import urllib
import json
import line
import slack
import dynamo


def lambda_handler(event, context):
    #slack.post_slack(str(event))
    #slack.post_slack(str(body["events"]))
    list = {}
    try:
        body = json.loads(event["body"])
        for events in body["events"]:
            type = events["message"]["type"]

            if type == "text":
                line.post_text(events)
            elif type == "sticker":
                line.post_sticker(events)
            else:
                line.post_text(events)
        return {'statusCode': 200, 'body': event}
    except:

        try:
            status = event["status"]
            try:
                com = event["comment"]
                dynamo.change_status(status,comment=com)
                event = dynamo.get_status()
                slack.post_slack(event)
                print("iOS Client incoming!")
            except:
                dynamo.change_status(status)
                event = dynamo.get_status()
                slack.post_slack(event)
                print("iOS Client incoming! Comment set Default")
            
        except:
            event = dynamo.get_status()
            list = dynamo.get_log()
            print(event)
            
        status = dynamo.get_status_raw()
        return {'statusCode': 200, 'body': event, 'status':status, 'log':list}
