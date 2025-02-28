import hashlib
import hmac
import time
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.conf import settings

def verify_telegram_authentication(bot_token, auth_data):
    if 'hash' not in auth_data:
        return False
    
    received_hash = auth_data['hash']
    auth_data_check_string = '\n'.join(sorted([f'{k}={v}' for k, v in auth_data.items() if k != 'hash']))
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, auth_data_check_string.encode(), hashlib.sha256).hexdigest()
    
    return calculated_hash == received_hash and (time.time() - int(auth_data['auth_date'])) < 86400

class TelegramAuthBackend(BaseBackend):
    def authenticate(self, request, telegram_id=None, first_name=None, last_name=None, username=None):
        User = get_user_model()
        
        try:
            user = User.objects.get(userprofile__telegram_id=telegram_id)
        except User.DoesNotExist:
            user = User.objects.create_user(username=f'telegram_{telegram_id}')
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            user.userprofile.telegram_id = telegram_id
            user.userprofile.save()
        
        return user

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

