import falcon
import falcon.testing as testing
import uuid
import main
import json
from model.user import User
from types import UnicodeType
import model.user

class TestValidateToken(testing.TestBase):
    def before(self):
        self.api = main.create_api()

    def test_validate_token_correct(self):
        uid = str(uuid.uuid4())
        password = "foo"
        token = "9999"
        user = User(uid=uid, password=password, auth_token=token)
        user.write()
        body = self.req(uid, token)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def test_validate_token_incorrect(self):
        uid = str(uuid.uuid4())
        password = "foo"
        token = "9999"
        user = User(uid=uid, password=password, auth_token=token)
        body = self.req(uid, token)
        body = json.loads(body)
        errors = body['errors']
        code = errors[0]['code']
        self.assertEqual(self.srmock.status, falcon.HTTP_401)
        self.assertEqual("user_not_authorized", code)

    def req(self, uid, token):
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),
                   ('Token', token)]
        return self.simulate_request(
            '/users/' + uid + '/validate_token',
            headers=headers,
            decode='utf-8',
            method="GET",
            body="")
