import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType
import model.user

class TestValidatePassword(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_validate_password_correct(self):
        uid = str(uuid.uuid4())
        password = "foo"
        user = User(uid=uid, password=password)
        user.write()
        body = self.req(uid, password)
        user = model.user.read(uid)
        body = json.loads(body)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(body['token'], user.get_token())
        self.assertEqual(password, user.get_password())

    def test_validate_password_incorrect(self):
        uid = str(uuid.uuid4())
        password = "foo"
        user = User(uid=uid, password=password)
        user.write()
        body = self.req(uid, "foo2")
        body = json.loads(body)
        self.assertEqual(self.srmock.status, falcon.HTTP_401)
        self.assertEqual(body, {'errors': [{'code': "password_invalid"}]})

    def test_validate_password_user_not_exists(self):
        uid = str(uuid.uuid4())
        password = "foo1"
        body = self.req(uid, password)
        self.assertEqual(self.srmock.status, falcon.HTTP_404)
        body = json.loads(body)
        self.assertEqual(body, {'errors': [{'code':"user_not_found"}]})

    def test_user_already_has_token(self):
        uid = str(uuid.uuid4())
        password = "foo"
        old_token = "abc"
        user = User(uid=uid, password=password, token=old_token)
        user.write()
        body = self.req(uid, password)
        user = model.user.read(uid)
        body = json.loads(body)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        self.assertEqual(body['token'], user.get_token())
        self.assertEqual(password, user.get_password())
        self.assertNotEqual(old_token, user.get_token())

    def req(self, uid, password):
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        return self.simulate_request(
            '/users/' + uid + '/validate_password',
            headers=headers,
            decode='utf-8',
            method="POST",
            body=json.dumps({'password': password}))
