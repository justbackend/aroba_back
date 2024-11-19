import time
import hashlib

SECRET_KEY = 'some_secret_key'


def generate_token(secret_key):
    timestamp = int(time.time())
    token_data = f"{timestamp}{secret_key}"
    token = hashlib.sha1(token_data.encode('utf-8')).hexdigest()
    return token, timestamp


_token, _timestamp = generate_token(SECRET_KEY)
print(_token)


def verify_token(secret_key, token, timestamp):
    token_data = f"{timestamp}{secret_key}"

    expected_token = hashlib.sha1(token_data.encode('utf-8')).hexdigest()
    print(expected_token)
    return expected_token == token


print(verify_token(SECRET_KEY, _token, _timestamp))
