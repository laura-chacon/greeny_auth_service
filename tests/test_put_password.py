import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType

class TestPutPassword(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_put_password_success(self):
        uid = str(uuid.uuid4())
        password = str(uuid.uuid4())
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        body = self.simulate_request('/users/' + uid + '/password',
                                     headers=headers,
                                     decode='utf-8',
                                     method="PUT",
                                     body=json.dumps({'password': password}))
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        body = json.loads(body)
        self.assertEqual(0, len(body))
        self.assertEqual([], body.keys())
        user = User(uid=uid, password=password)
        user.read_password()
        self.assertEqual(UnicodeType, type(user.get_password()))
        self.assertTrue(user.get_uid() == uid)
        self.assertTrue(user.get_password() == password)
