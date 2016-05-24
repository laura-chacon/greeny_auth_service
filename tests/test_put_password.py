import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType
import model.user

class TestPutPassword(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_user_doesnt_exist(self):
        uid = str(uuid.uuid4())
        password = "abcdef"
        body = self.req(uid, body={'password': password})
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        body = json.loads(body)
        self.assertEqual({}, body)
        user = model.user.read(uid)
        self.assertEqual(UnicodeType, type(user.get_password()))
        self.assertEqual(password, user.get_password())
        self.assertEqual(None, user.get_token())

    def test_user_already_exists(self):
        uid = str(uuid.uuid4())
        old_password = "foo1"
        new_password = "foo2"
        user = User(uid=uid, password=old_password)
        user.write()
        body = self.req(uid, body={'password': new_password})
        user = model.user.read(uid)
        self.assertEqual(new_password, user.get_password())

    def req(self, uid, body):
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        return self.simulate_request('/users/' + uid + '/password',
                                     headers=headers,
                                     decode='utf-8',
                                     method="PUT",
                                     body=json.dumps(body))
