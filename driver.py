import json
import lambda_function
import os

os.environ["LINE_CHANNEL_ACCESS_TOKEN"] = "HogeHoge"
os.environ["SlackUrl"] = "HogeHoge"

json = {
   "events": [
       {
           "type": "message",
           "replyToken": "6893c03120cb40d097d7ac6f0340a9ab",
           "source": {
               "userId": "U83d0082086d489298a5e0e4c683fd6db",
               "type": "user"
           },
           "timestamp": 1533723835523,
           "message": {
               "type": "text",
               "id": "8387851245136",
               "text": "テキストの場合"
           }
       }
   ]
}

lambda_function.lambda_handler(json,"ada")
