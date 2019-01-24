# coding: utf-8
import boto3
import sns
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr 
dynamodb = boto3.resource('dynamodb')
key_status_table = dynamodb.Table("JaclaKey")
key_log_table = dynamodb.Table("JaclaKeyLogTable")

def change_status(status,comment=None):
    at = str(datetime.now())
    item = {
            "location" : "room" ,
            "status": status,
            "logged_at": at
        }
    if comment != "" or not comment == None:
        message = comment
        
    if comment == None or comment == "":
        if status =="borrow":
            message = "鍵は借りられているよ！"
        elif status =="open":
            message = "部室は開いてるよ！"
        elif status =="close":
            message = "部室はしまってるみたい.."
        elif status =="return":
            message = "鍵は返されているみたい.."
        else:
            message = "鍵はどこ？？どこなの..?"
            

    
    item.update({"message": message})
    key_status_table.put_item(Item = item)
    key_log_table.put_item(Item = item)
    sns.send_notify(message)


def get_status():
    status = key_status_table.get_item(Key = {"location":"room"})
    res = status["Item"]["message"]
    return res
    
def get_status_raw():
    status = key_status_table.get_item(Key = {"location":"room"})
    res = status["Item"]["status"]
    return res

def get_log(room="room"):
    list = key_log_table.query(
    KeyConditionExpression=Key('location').eq(room),
    ScanIndexForward=False,
    Limit=15
    )
    return list["Items"]