import boto3
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError

ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

dynamodb = boto3.resource('dynamodb')
key_status_table = dynamodb.Table("JaclaKey")
key_log_table = dynamodb.Table("JaclaKeyLogTable")
account_table = dynamodb.Table("JaclaAccountTable")

at = str(datetime.now())


def post_account(user_id):
    line_bot_api = LineBotApi(ACCESS_TOKEN)
    try:
        profile = line_bot_api.get_profile(user_id)
    except:
        import traceback
        traceback.print_exc()

    print(str(profile))

    try:
        res = account_table.put_item(
            Item={
                "acid": user_id,
                "acnm": str(profile.display_name),
                "user_pic": str(profile.picture_url),
                "created_at": at
            }
        )
    except:
        import traceback
        traceback.print_exc()

    print("OK")

    # except e:
    #    print("error")
    #    print(e.stacktrace)
    #    pass

    print(res)
    return res


def check_user(user_id):
    try:
        res = account_table.get_item(
            Key={"acid": user_id}
        )
        response = res['Item']
    except:
        # import traceback
        # traceback.print_exc()
        post_account(user_id)
        response = check_user(user_id)
    return response


def account_regist(acid, acnm, year, at):
    item = {
        "acid": acid,
        "acnm": acnm,
        "year": year,
        "created_at": at
    }
