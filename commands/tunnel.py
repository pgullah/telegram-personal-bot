from telegram import Update
import os
from telegram.ext import CallbackContext
import requests

from common.util import get_env_config

TUNNEL_DOMAIN = get_env_config("TUNNEL_DOMAIN")
assert TUNNEL_DOMAIN, "Tunnel domain must be provided."

TOKEN = get_env_config(
    "TOKEN", "~/.data/.private/app-secrets/telegram/tokens.ini", "Bot"
)
assert TOKEN, "Telegram Bot Token must be provided"


async def call(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not TUNNEL_DOMAIN:
        await context.bot.send_message(chat_id, text="Tunnel is not available")

    print("TUNNEL DOMAIN:", TUNNEL_DOMAIN)
    args = context.args
    if len(args) == 2:
        tunnel_type = args[0].lower()
        option = args[1].lower()
        if option == "on" or option == "off":
            try:
                tunnel_api = f"{TUNNEL_DOMAIN}/{tunnel_type}"
                print("Invoking tunnel api:", tunnel_api)
                if option == "on":
                    response = requests.put(tunnel_api, timeout=5).json()
                    message = f'Tunnel Details: \n URL: {response["url"]}'
                    if "remote_address" in response:
                        message = f'{message}\n Address:{response["remote_address"]}'
                else:
                    response = requests.delete(tunnel_api, timeout=5)
                    message = "Tunnel is closed"
            except requests.exceptions.HTTPError as he:
                message = f"Failed to turn {option} the {tunnel_type} tunnel."
            except Exception as ex:
                print("failed to open tunnel:", ex)
                message = f"Unexpected error has occurred!: {str(ex)}"

            await context.bot.send_message(chat_id=chat_id, text=message)
    else:
        await context.bot.send_message(
            chat_id=chat_id, text="Please specify tunnel and option"
        )
