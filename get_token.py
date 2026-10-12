from yandex_music import Client

def on_code(code):
    print(f'Откройте {code.verification_url} и введите код: {code.user_code}')

client = Client()
token = client.device_auth(on_code=on_code)

print(f'access_token:  {token.access_token}')
print(f'refresh_token: {token.refresh_token}')
print(f'expires_in:    {token.expires_in}')

client.init()

#код с документации яндекса