import json
import boto3
import boto.dynamodb
import os

client = boto3.resource(
    'dynamodb',
    region_name='eu-west-1',
    aws_access_key_id=os.environ['ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['SECRET_ACCESS_KEY']
)

as_users = client.Table('as_users')

class User:
    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.password = kwargs.get("password", None)
        self.auth_token = kwargs.get("auth_token", None)

    def get_uid(self):
        return self.uid

    def get_token(self):
        return self.auth_token

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def set_token(self, auth_token):
        self.auth_token = auth_token

    def write(self):
        if self.password != None:
            as_users.put_item(
                Item={
                    'uid': self.uid,
                    'password': self.password
                }
            )
        if self.auth_token != None:
            as_users.put_item(
                Item={
                    'uid': self.uid,
                    'auth_token': self.auth_token
                }
            )
        if self.password != None and self.auth_token != None:
            as_users.put_item(
                Item={
                    'uid': self.uid,
                    'password': self.password,
                    'auth_token': self.auth_token
                }
            )


def try_read(uid):
    response = as_users.get_item(
        Key={
            'uid': uid
        }
    )
    if 'Item' in response:
        item = response['Item']
        return User(**item)
    else:
        return None

def read(uid):
    response = as_users.get_item(
        Key={
            'uid': uid
        }
    )
    item = response['Item']
    return User(**item)
