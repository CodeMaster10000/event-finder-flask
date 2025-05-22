def validate_user(user, exc):
    if user is None:
        raise exc

def validate_event(event, exc):
    if event is None:
        raise exc