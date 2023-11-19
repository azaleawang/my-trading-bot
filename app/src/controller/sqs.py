import boto3
import json
import os
from botocore.exceptions import ClientError

client = boto3.client('sqs')
sqs_url = os.getenv('SQS_URL')
def send_message(sqs_url: str = sqs_url, message_body: json = {}):
    try:
        print("message body", message_body)
        response = client.send_message(
            QueueUrl=sqs_url,
            MessageBody=json.dumps(message_body)
        )
        return response
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'QueueDoesNotExist':
            print("The specified queue does not exist.")
        else:
            print("An SQS ClientError occurred:", e)
        return {"error": "SQS error", "details": str(e)}
    
    except Exception as e:
        # Handle other non-SQS errors
        print("A non-SQS error occurred:", e)
        return {"error": "Non-SQS error", "details": str(e)}

#{'MD5OfMessageBody': '8e9d4681c2e34d10993c6bb537ebdcf7', 'MessageId': '294bebd2-323c-474e-a9a7-5397fbe16f2a', 'ResponseMetadata': {'RequestId': '274e9822-1404-55d5-9f5e-c5f379c6f6ce', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '274e9822-1404-55d5-9f5e-c5f379c6f6ce', 'date': 'Fri, 17 Nov 2023 13:32:50 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '106', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}