import os
import urllib
import json
import line

def post_slack(event, username=None):
    # TODO implement
    url = os.environ["SlackUrl"]
    method = "POST"
    
    if event is not str:
        event = json.dumps(event, indent=4, separators=(',', ': '), ensure_ascii=False)
    #item = {"text": str(jsonformat)}
    item = {
        "text":str(username+"が"+event)
    }
    
    #item = {"text":"Line/  "+text}
    #print("token = ",token)
    header = {"Content-Type" : "application/json"}
    json_data = json.dumps(item).encode("utf-8")

    #line.post_text(token, "鍵がしまったよ！")

    request = urllib.request.Request(url, data= json_data, method=method, headers=header)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
