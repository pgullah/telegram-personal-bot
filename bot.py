import os
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
from telegram import Update
from utils import AdminOnly
import requests
from requests.exceptions import HTTPError

TUNNEL_DOMAIN=os.environ.get('TUNNEL_DOMAIN', None)
TOKEN_KEY = 'TOKEN'
if TOKEN_KEY in os.environ:
   print("Using token from environment")
   TOKEN = os.environ[TOKEN_KEY]
else:
   import configparser
   config = configparser.ConfigParser()
   config.read(os.path.expanduser('~/.private/telegram/tokens.ini'))
   config_key='PradAIBot'
   bot_config=config[config_key]
   TOKEN=bot_config[TOKEN_KEY]

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

@AdminOnly
def start(update: Update, context: CallbackContext):
    chat_id=update.effective_chat.id
    # args = context.args
    context.bot.send_message(chat_id=chat_id, text="Hey Admin, please talk to me!")

@AdminOnly
def tunnel(update: Update, context: CallbackContext):
    chat_id=update.effective_chat.id
    if not TUNNEL_DOMAIN:
        context.bot.send_message(chat_id, text='Tunnel is not available')
    
    print("TUNNEL DOMAIN:", TUNNEL_DOMAIN)
    args = context.args
    if len(args) == 2:
        tunnel_type=args[0].lower()
        option = args[1].lower()
        if option == 'on' or option == 'off':
            method = requests.put if option == 'on' else requests.delete
            try:
                tunnel_api = TUNNEL_DOMAIN + '/' + tunnel_type
                print('Invoking tunnel api:', tunnel_api)
                if option == 'on':
                    response = requests.put(tunnel_api, timeout=5).json()
                    message = 'Tunnel Details: \n URL: {}'.format(response['url'])
                    if 'remote_address' in response:
                        message = message + '\n Address:{}'.format(response['remote_address'])
                else:
                    response = requests.delete(tunnel_api, timeout=5)
                    message = 'Tunnel is closed'
            except HTTPError as he:
                message = 'Failed to turn {} the {} tunnel.'.format(option, tunnel_type)
            except Exception as ex:
                print('faile to open tunnel:', ex)
                message = 'Unexpected error has occurred!: ' + str(ex)

            context.bot.send_message(chat_id=chat_id, text=message)
    else:
        context.bot.send_message(chat_id=chat_id, text='Please specify tunnel and option')


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry I can't understand your request!")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('tunnel', tunnel))
## fallback handler
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

print("Started bot..")
updater.start_polling()
