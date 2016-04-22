import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType
import model.user

class TestCreateToken(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_create_token_success(self):
        uid = str(uuid.uuid4())
        body = self.req(uid)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        body = json.loads(body)
        self.assertEqual(1, len(body))
        self.assertEqual(['token'], body.keys())
        user = model.user.read(uid)
        self.assertEqual(UnicodeType, type(user.get_token()))
        self.assertTrue(len(user.get_token()) > 10)
        self.assertTrue(user.get_token() == body['token'])
        self.assertEqual(None, user.get_password())

    def test_user_already_exists(self):
        uid = str(uuid.uuid4())
        old_token = str(uuid.uuid4())
        password = "asd2"
        user = User(uid=uid, token=old_token, password=password)
        user.write()
        body = self.req(uid)
        body = json.loads(body)
        user = model.user.read(uid)
        self.assertEqual(password, user.get_password())
        self.assertNotEqual(old_token, user.get_token())
        self.assertTrue(user.get_token() == body['token'])

    def test_body_not_json(self):
        uid = str(uuid.uuid4())
        body = self.req(uid, body='aaa')
        self.assertEqual(self.srmock.status, falcon.HTTP_753)

    def test_method_not_post(self):
        uid = str(uuid.uuid4())
        body = self.req(uid, method="GET")
        self.assertEqual(self.srmock.status, falcon.HTTP_405)

    def test_header_not_json(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', 'application/xml'),
                   ('Content-Type', 'application/json'),]
        body = self.req(uid, headers=headers)
        self.assertEqual(self.srmock.status, falcon.HTTP_406)

    def test_contenttype_not_json(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/xml'),]
        body = self.req(uid, headers=headers)
        self.assertEqual(self.srmock.status, falcon.HTTP_415)

    def test_contenttype_header_missing(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', 'application/json'),
                   ('Content-Type',''),]
        body = self.req(uid, headers=headers)
        self.assertEqual(self.srmock.status, falcon.HTTP_415)

    def test_accept_header_missing(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', ''),
                   ('Content-Type', 'application/json'),]
        body = self.req(uid, headers=headers)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        body = json.loads(body)
        self.assertEqual(1, len(body))

    def req(self, uid, method="POST", headers=None, body='{}'):
        if headers == None:
            headers = [('Accept', 'application/json'),
                       ('Content-Type', 'application/json'),]
        return self.simulate_request('/users/' + uid + '/create_token',
                                     headers=headers,
                                     decode='utf-8',
                                     method=method,
                                     body=body)
