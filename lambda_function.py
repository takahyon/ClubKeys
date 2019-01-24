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
    # slack.post_slack(str(body["events"]))
    list = {}
    try:
        print(1)
        # slack.post_slack(1)
        # body = event["body"]

        for events in event["events"]:
            datatype = events["message"]["type"]

            if datatype == "text":
                line.post_text(events)
            elif datatype == "sticker":
                line.post_sticker(events)
            else:
                line.post_text(events)
        return {'statusCode': 200, 'body': event}
    except:
        print(2)
        # slack.post_slack(2)
        try:
            status = event["status"]

            if event["comment"] != "":
                print(3)
                # slack.post_slack(3)
                com = event["comment"]
                dynamo.change_status(status, comment=com)
                # event = dynamo.get_status()
                slack.post_slack("iOS Client incoming!\n" + str(event))
                print("iOS Client incoming!")
                return {'statusCode': 200, 'body': "iOS Comming with message success"}
            else:
                print(4)
                # slack.post_slack(4)
                dynamo.change_status(status)
                # event = dynamo.get_status()
                slack.post_slack("iOS Client incoming!set Default\n" + str(event))
                print("iOS Client incoming! Comment set Default")
                return {'statusCode': 200, 'body': "iOS Comming success"}

        except:
            import traceback
            traceback.print_exc()

            print(5)
            # slack.post_slack(5)
            event = dynamo.get_status()
            list = dynamo.get_log()
            print(event)

            status = dynamo.get_status_raw()
            return {'statusCode': 200, 'body': event, 'status': status, 'log': list}
