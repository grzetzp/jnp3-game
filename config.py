import os
# from base64 import b64encode

MONGO_URI = 'mongodb://test_mongodb:27017/test_mongodb'
APP_SALT = os.urandom(32)
ENC_ALGO = 'HS256'
DEC_FORMAT = 'utf-8'
APP_SECRET_KEY = "TODO:_change_to_real_random_SECRET_KEY"
# APP_SECRET_KEY = b64encode(os.urandom(32)).decode(DEC_FORMAT)
