import boto3

sns = boto3.client('sns')

def send_notify(text):
    
    responce = sns.publish(
        TopicArn = 'arn:aws:sns:ap-northeast-1:754828967072:ClubKeysTest',
        Message = text,
        Subject = 'Lambdaからのpublish'
        )