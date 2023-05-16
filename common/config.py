import os

TUNNEL_DOMAIN=os.environ.get('TUNNEL_DOMAIN', None)
TOKEN_KEY = 'TOKEN'
if TOKEN_KEY in os.environ:
   print("Using token from environment")
   TOKEN = os.environ[TOKEN_KEY]
else:
   import configparser
   config = configparser.ConfigParser()
   config.read(os.path.expanduser('~/.data/.private/app-secrets/telegram/tokens.ini'))
   TOKEN=config.get('Bot', TOKEN_KEY)

def get_token():
   return TOKEN

def get_tunnel_domain():
   return TUNNEL_DOMAIN