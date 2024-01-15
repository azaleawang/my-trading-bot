import boto3
import json
import os
from botocore.exceptions import ClientError
from app.utils.logger import logger

from app.exceptions import SQSError, UnexpectedError

client = boto3.client(
    "sqs",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)
sqs_url = os.getenv("SQS_URL")


def send_sqs_message(sqs_url: str = sqs_url, message_body: dict = {}):
    try:
        response = client.send_message(
            QueueUrl=sqs_url, MessageBody=json.dumps(message_body)
        )
        return response

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "QueueDoesNotExist":
            logger.error("The specified queue does not exist.")
        else:
            logger.error("An SQS ClientError occurred:", e)
        raise SQSError()

    except Exception as e:
        # Handle other non-SQS errors
        logger.error("A non-SQS error occurred:", e)
        raise UnexpectedError(detail="Backtesting job failed to push into SQS.")


# {'MD5OfMessageBody': '8e9d4681c2e34d10993c6bb537ebdcf7', 'MessageId': '294bebd2-323c-474e-a9a7-5397fbe16f2a', 'ResponseMetadata': {'RequestId': '274e9822-1404-55d5-9f5e-c5f379c6f6ce', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '274e9822-1404-55d5-9f5e-c5f379c6f6ce', 'date': 'Fri, 17 Nov 2023 13:32:50 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '106', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
