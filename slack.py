from datetime import datetime
import os
import urllib
import json
import line

nowt = str(datetime.now())[:-10]
nowt = "[" + nowt + "]"

def post_slack(event, username=None,user_pic=None):
    # TODO implement
    url = os.environ["SlackURL"]
    method = "POST"
    
    if event is not str:
        event = json.dumps(event, indent=4, separators=(',', ': '), ensure_ascii=False)
    #item = {"text": str(jsonformat)}
    if username != None and user_pic != None :
        item = {
            'username': str(username),  # ユーザー名
            'icon_url': user_pic,
            'text': nowt + str(username+"が"+event),
            "attachments": [
                {
                    "text": "status:{0}\nat:{1} \nuser:{2}".format(event, nowt, username)
                },
            ]
        }
    else:
        item = {
            "text": "",
            "attachments": [
                {
                    "text": "status:{0}\nat:{1}".format(event, nowt)
                },
            ]
        }

    #item = {"text":"Line/  "+text}
    #print("token = ",token)
    header = {"Content-Type" : "application/json"}
    json_data = json.dumps(item).encode("utf-8")

    #line.post_text(token, "鍵がしまったよ！")

    request = urllib.request.Request(url, data= json_data, method=method, headers=header)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
