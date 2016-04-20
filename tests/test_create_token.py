import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType

class TestCreateToken(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_create_token_success(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        body = self.simulate_request('/users/' + uid + '/create_token',
                                     headers=headers,
                                     decode='utf-8',
                                     method="POST",
                                     body='{}')
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        body = json.loads(body)
        self.assertEqual(1, len(body))
        self.assertEqual(['token'], body.keys())
        user = User(uid=uid)
        user.read_token()
        self.assertEqual(UnicodeType, type(user.get_token()))
        self.assertTrue(len(user.get_token()) > 10)
        self.assertTrue(user.get_token() == body['token'])

    def test_body_not_json(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        body = self.simulate_request('/users/' + uid + '/create_token',
                                     headers=headers,
                                     decode='utf-8',
                                     method="POST",
                                     body='aaa')
        self.assertEqual(self.srmock.status, falcon.HTTP_753)

    def test_method_not_post(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        body = self.simulate_request('/users/' + uid + '/create_token',
                                     headers=headers,
                                     decode='utf-8',
                                     method="GET",
                                     body='{}')
        self.assertEqual(self.srmock.status, falcon.HTTP_405)

    def test_header_not_json(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', 'application/xml'),
                   ('Content-Type', 'application/json'),]
        body = self.simulate_request('/users/' + uid + '/create_token',
                                     headers=headers,
                                     decode='utf-8',
                                     method="POST",
                                     body='{}')
        self.assertEqual(self.srmock.status, falcon.HTTP_406)

    def test_contenttype_not_json(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/xml'),]
        body = self.simulate_request('/users/' + uid + '/create_token',
                                     headers=headers,
                                     decode='utf-8',
                                     method="POST",
                                     body='{}')
        self.assertEqual(self.srmock.status, falcon.HTTP_415)
