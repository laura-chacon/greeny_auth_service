import falcon
import uuid
from model.user import User

def create_token():
    return str(uuid.uuid4())
