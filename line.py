import sys
sys.path.append('./lib')
import requests
import json
import os
import slack
import dynamo
import account
from datetime import datetime
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError


REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
method = "POST"


def post_text(event):
    nowt = str(datetime.now())[:-10]
    nowt = "[" + nowt + "]"

    reply_token = event["replyToken"]
    text = event["message"]["text"]
    user_id = event["source"]["userId"]
    profile = account.check_user(user_id)

    
    try:
        group_id = event["source"]["groupId"]
    except:
        pass

    try:
        user_name = profile['acnm']
        user_pic = profile['user_pic']
        print(user_name)
    except LineBotApiError as e:
    # error handle
        reply_text = str(e)
    
    if "あけ" in text or "開" in text:
        message = str(nowt) + "  開けました！"
        slack.post_slack(message, user_name)
        dynamo.change_status("open")
        reply_text = "りょーかい！練習頑張って！"
    elif "かり" in text or "借" in text:
        message = str(nowt) + "  借りました！"
        slack.post_slack(message, user_name)
        dynamo.change_status("borrow")
        reply_text = "借りたのねー！了解！"
    elif "かえし" in text or "返" in text:
        message = str(nowt) + "  部室の鍵を返しました！"
        slack.post_slack(message, user_name)
        dynamo.change_status("return")
        reply_text = "お疲れ様でしたー！"
    elif "しめ" in text or "閉" in text:
        message = str(nowt) + "  部室閉めました！"
        slack.post_slack(message, user_name)
        dynamo.change_status("close")
        reply_text = "おっけー！またねー"
    elif "鍵" or "かぎ" in text:
        # TODO: write code...:
        reply_text = str(dynamo.get_status())
    else:
        slack.post_slack(text)
        reply_text = user_name
        
    reply_text = event
    LINE_API_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": str("Bearer " + ACCESS_TOKEN)
    }
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": str(user_name)

            }
        ]
    }

    json_data = json.dumps(payload).encode("utf-8")

    response = requests.post(REPLY_ENDPOINT, headers=LINE_API_HEADERS, data=json.dumps(payload))
    print(response.status_code)


def post_sticker(event):
    nowt = str(datetime.now())[:-10]
    nowt = "[" + nowt + "]"
    reply_token = event["replyToken"]
    stid = event["message"]["stickerId"]

    if stid == "23397320":
        message = str(nowt) + "  借りました！"
        slack.post_slack(message)
        reply_text = "借りたのねー！了解"
        dynamo.change_status("borrow")
    elif stid == "23397321":
        message = str(nowt) + "  返しました！"
        slack.post_slack(message)
        dynamo.change_status("return")
        reply_text = "お疲れ様でしたー！"

    elif stid == "23397327":
        message = str(nowt) + "  部室開けました！"
        slack.post_slack(message)
        dynamo.change_status("open")
        reply_text = "りょーかい！練習頑張って"
    elif stid == "23397326":
        message = str(nowt) + "  部室閉めました！"
        slack.post_slack(message)
        dynamo.change_status("close")
        reply_text = "おっけー！またねー"

    else:
        pass

    LINE_API_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": str("Bearer " + ACCESS_TOKEN)
    }
    jsonformat = json.dumps(event, indent=4, separators=(',', ': '), ensure_ascii=False)
    
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": reply_text
    
            }
        ]
    }
    
    json_data = json.dumps(payload).encode("utf-8")
    
    #response = requests.post(REPLY_ENDPOINT, headers=LINE_API_HEADERS, data = json_data)
    print(response.status_code)
