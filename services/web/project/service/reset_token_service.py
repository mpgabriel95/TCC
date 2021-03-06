from ..repository import token_repository
from datetime import datetime, timedelta
from time import sleep


def switch_token():
    print("Switching token...")
    set_expired()
    return get_available_token()

#TODO validate timezone
#returns an available token, if there isn't, sleep...
def get_available_token():
    most_recent_token = token_repository.get_first_expirated()
    last_expiration = most_recent_token.last_expiration

    now = datetime.now()
    now_minus_1 = now - timedelta(hours=1)

    if __is_token_not_ready(last_expiration, now_minus_1):
        diference = last_expiration - now_minus_1
        print("@@ waiting " +  str(diference) + "ms for token to be available")
        sleep(diference.seconds + 1)

    return most_recent_token

def set_expired():
    most_recent_token = token_repository.get_first_expirated()
    token_repository.update_last_expiration(most_recent_token.id , datetime.now())

def __is_token_not_ready(last_expiration, now_minus_1):
    return last_expiration > now_minus_1