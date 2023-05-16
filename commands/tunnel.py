from telegram import Update
import os
from telegram.ext import CallbackContext
import requests

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

def call(update: Update, context: CallbackContext):
    chat_id=update.effective_chat.id
    if not TUNNEL_DOMAIN:
        context.bot.send_message(chat_id, text='Tunnel is not available')
    
    print("TUNNEL DOMAIN:", TUNNEL_DOMAIN)
    args = context.args
    if len(args) == 2:
        tunnel_type=args[0].lower()
        option = args[1].lower()
        if option == 'on' or option == 'off':
            try:
                tunnel_api = f'{TUNNEL_DOMAIN}/{tunnel_type}'
                print('Invoking tunnel api:', tunnel_api)
                if option == 'on':
                    response = requests.put(tunnel_api, timeout=5).json()
                    message = 'Tunnel Details: \n URL: {}'.format(response['url'])
                    if 'remote_address' in response:
                        message = message + '\n Address:{}'.format(response['remote_address'])
                else:
                    response = requests.delete(tunnel_api, timeout=5)
                    message = 'Tunnel is closed'
            except requests.exceptions.HTTPError as he:
                message = f'Failed to turn {option} the {tunnel_type} tunnel.'
            except Exception as ex:
                print('failed to open tunnel:', ex)
                message = f'Unexpected error has occurred!: {str(ex)}'

            context.bot.send_message(chat_id=chat_id, text=message)
    else:
        context.bot.send_message(chat_id=chat_id, text='Please specify tunnel and option')
