import base64


def get_auth_header(username, password):
    raw = f"{username}:{password}".encode("utf-8")
    credentials = base64.b64encode(raw).decode('utf-8')
    return {'Authorization': f'Basic {credentials}'}
