import json
import boto
import boto.dynamodb
import os

conn = boto.dynamodb.connect_to_region(
        'eu-west-1',
        aws_access_key_id = os.environ['ACCESS_KEY_ID'],
        aws_secret_access_key = os.environ['SECRET_ACCESS_KEY'])
as_user_token = conn.get_table('as_user_token')
as_user_password = conn.get_table('as_user_password')

class User:
    def __init__(self):
        self.uid = None
        self.password = None
        self.token = None

    def set_uid(self, new_uid):
        self.uid = new_uid

    def set_password(self, new_password):
        self.password = new_password

    def set_token(self, token):
        self.token = token

    def write_user_token(self):
        user = as_user_token.new_item(
            attrs={
                'uid': self.uid,
                'token': self.token
            }
        )
        user.put()

    def write_user_password(self):
        user = as_user_password.new_item(
            attrs={
                'uid': self.uid,
                'password': self.password
            }
        )
        user.put()

    def get_password(self, uid):
        user = as_user_password.get_item(uid)
        return user['password']
