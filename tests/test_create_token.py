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

    def test_create_token(self):
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
