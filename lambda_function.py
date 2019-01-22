 # coding: utf-8

import os
import urllib
import json
import line
import slack
import dynamo
import sys
import env

sys.path.append('./lib')

def lambda_handler(event, context):
    slack.post_slack(str(event))
    try:
        for events in event["body-json"]["events"]:
            type = events["message"]["type"]
            
            if type == "text":
                line.post_text(events)
            elif type == "sticker":
                line.post_sticker(events)
            else:
                line.post_text(events)
        return {'statusCode': 200, 'body': event, 'status':status}
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
            print(event)
            
        status = dynamo.get_status_raw()
        return {'statusCode': 200, 'body': event, 'status':status}
