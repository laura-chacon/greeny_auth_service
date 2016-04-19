import falcon
import falcon.testing as testing
import uuid
import main
from model.user import User
from types import UnicodeType

class TestCreateToken(testing.TestBase):
    def before(self):
        main.add_routes(self.api)

    def test_grace(self):
        uid = str(uuid.uuid4())
        headers = [('Accept', 'application/json'),
                   ('Content-Type', 'application/json'),]
        body = self.simulate_request('/users/' + uid + '/create_token',
                                     headers=headers,
                                     decode='utf-8',
                                     method="POST",
                                     body='{}')
        self.assertEqual(self.srmock.status, falcon.HTTP_200)
        user = User(uid=uid)
        user.read_token()
        self.assertEqual(UnicodeType, type(user.get_token()))
        self.assertTrue(len(user.get_token()) > 10)
        self.assertNotEqual(None, user.get_token())
