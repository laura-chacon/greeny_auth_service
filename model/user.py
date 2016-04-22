import json
import boto
import boto.dynamodb
import os

conn = boto.dynamodb.connect_to_region(
        'eu-west-1',
        aws_access_key_id = os.environ['ACCESS_KEY_ID'],
        aws_secret_access_key = os.environ['SECRET_ACCESS_KEY'])
as_users = conn.get_table('as_users')

class User:
    def __init__(self, **kwargs):
        self.uid = kwargs.get("uid", None)
        self.password = kwargs.get("password", None)
        self.token = kwargs.get("token", None)

    def get_uid(self):
        return self.uid

    def get_token(self):
        return self.token

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def set_token(self, token):
        self.token = token

    def write(self):
        m = {'uid': self.uid}
        if self.password != None:
            m['password'] = self.password
        if self.token != None:
            m['token'] = self.token
        user = as_users.new_item(attrs=m)
        user.put()

def try_read(uid):
    try:
        m = as_users.get_item(uid)
        return User(**m)
    except boto.dynamodb.exceptions.DynamoDBKeyNotFoundError:
        return None

def read(uid):
    m = as_users.get_item(uid)
    return User(**m)
