import hashlib
import time

SECRET_KEY = '038b3ef0-bfd2-4a7d-8014-97603f62cf08'


def generate_token(secret_key):
    timestamp = int(time.time())
    print(timestamp)
    token_data = f"{timestamp}{secret_key}"
    token = hashlib.sha1(token_data.encode('utf-8')).hexdigest()
    return token, timestamp


_token, _timestamp = generate_token(SECRET_KEY)

headers_auth = f"{2034}:{_token}:{_timestamp}"
print(headers_auth)


def verify_token(secret_key, token, timestamp):
    token_data = f"{timestamp}{secret_key}"

    expected_token = hashlib.sha1(token_data.encode('utf-8')).hexdigest()
    return expected_token == token


print(verify_token(SECRET_KEY, _token, _timestamp))
