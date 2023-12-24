import boto3
from botocore.exceptions import ClientError
import os
import logging

from fastapi import HTTPException

ec2 = boto3.client(
    "ec2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


def create_ec2_instance(
    image_id=os.getenv("AMI_ID"),
    instance_type="t2.micro",
    key_pair=os.getenv("EC2_KEY_PAIR"),
    security_groups=[os.getenv("EC2_SG")],
):
    try:
        instance_params = {
            "ImageId": image_id,
            "InstanceType": instance_type,
            "KeyName": key_pair,
        }
        if security_groups is not None:
            instance_params["SecurityGroupIds"] = [sg for sg in security_groups]
        instance = ec2.run_instances(**instance_params, MinCount=1, MaxCount=1)
        print("waiting for running ec2")

    except ClientError as err:
        logging.error(
            "Couldn't create instance with image %s, instance type %s, and key %s. "
            "Here's why: %s: %s",
            image_id,
            instance_type,
            key_pair,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise HTTPException(status_code=500, detail="Couldn't create instance")
    else:
        return instance


def start_ec2_instance(instance_id: str):
    try:
        print("starting ec2, instance id = ", instance_id)
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
        return True
    except ClientError as err:
        logging.error(
            "Couldn't start instance id %s"
            "Here's why: %s: %s",
            instance_id,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise HTTPException(status_code=500, detail="Couldn't start instance: " + str(err.response["Error"]["Message"]))



def stop_ec2_instance(instance_id: str):
    try:
        print("stopping ec2, instance id = ", instance_id)
        response = ec2.stop_instances(InstanceIds=[instance_id], Hibernate=False, DryRun=False, Force=False)
        print(response)
        return True
    except ClientError as err:
        logging.error(
            "Couldn't stop instance id %s"
            "Here's why: %s: %s",
            instance_id,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise HTTPException(status_code=500, detail="Couldn't stop instance: " + str(err.response["Error"]["Message"]))