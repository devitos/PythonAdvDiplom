from urllib.parse import urlencode, urljoin

APP_ID = # СЮДА ВСТАВЛЯЕМ ID НАШЕГО ПРИЛОЖЕНИЯ

URL = 'https://oauth.vk.com/authorize'

REDIRECT_URI = 'https://oauth.vk.com/blank.html'

SCOPE = ['friends', 'photos', 'likes']

response_type = 'token'

OAUTH_PARAMS = {'redirect_uri': REDIRECT_URI, 'scope': SCOPE, 'response_type': response_type, 'client_id': APP_ID}
print('?'.join([URL, urlencode(OAUTH_PARAMS)]))
