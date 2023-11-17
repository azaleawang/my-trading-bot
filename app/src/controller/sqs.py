import boto3
import json
client = boto3.client('sqs')
sqs_url = "https://sqs.ap-northeast-1.amazonaws.com/958720635143/lambda-queue"

def send_message(sqs_url, message_body):
    print("message body", message_body)
    response = client.send_message(
        QueueUrl = sqs_url,
        MessageBody = json.dumps(message_body)
    )
    return response

#{'MD5OfMessageBody': '8e9d4681c2e34d10993c6bb537ebdcf7', 'MessageId': '294bebd2-323c-474e-a9a7-5397fbe16f2a', 'ResponseMetadata': {'RequestId': '274e9822-1404-55d5-9f5e-c5f379c6f6ce', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '274e9822-1404-55d5-9f5e-c5f379c6f6ce', 'date': 'Fri, 17 Nov 2023 13:32:50 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '106', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}