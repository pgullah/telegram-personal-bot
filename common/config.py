# pyright: strict
import os
from typing import Callable, TypeVar

TOKEN_KEY = 'TOKEN'

T = TypeVar("T")
def __lazy_get(var_name: str, callback: Callable[[], T]) -> T:
   if var_name not in globals():
      globals()[var_name] = callback()
   
   return globals()[var_name]

def __fetch_token():
   if TOKEN_KEY in os.environ:
      print("Using token from environment")
      return os.environ[TOKEN_KEY]
   else:
      import configparser
      config = configparser.ConfigParser()
      config.read(os.path.expanduser('~/.data/.private/app-secrets/telegram/tokens.ini'))
      return config.get('Bot', TOKEN_KEY)

def get_token():
   return __lazy_get(TOKEN_KEY, __fetch_token)

def get_tunnel_domain():
   return __lazy_get('TUNNEL_DOMAIN', lambda: os.environ.get('TUNNEL_DOMAIN', None))

