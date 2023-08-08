from telegram import Update
import os
from telegram.ext import CallbackContext
import requests
import traceback
from dotenv_vault import load_dotenv
load_dotenv()

HOST_API_DOMAIN = os.getenv("HOST_API_DOMAIN")
HOST_API_USER = os.getenv("HOST_API_USER")
HOST_API_PASSWORD = os.getenv("HOST_API_PASSWORD")

assert HOST_API_DOMAIN, "Tunnel domain must be provided."

TOKEN = os.getenv("TOKEN")
assert TOKEN, "Telegram Bot Token must be provided"

async def call(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if not HOST_API_DOMAIN:
        await context.bot.send_message(chat_id, text="Tunnel is not available")

    print("HOST_API_DOMAIN:", HOST_API_DOMAIN)
    args = context.args
    if len(args) == 2:
        tunnel_type = args[0].lower()
        option = args[1].lower()
        if option == "on" or option == "off":
            def execute_tunnel_request():
                method = 'PUT' if option == 'on' else 'DELETE'
                tunnel_api = f"{HOST_API_DOMAIN}/tunnel/{tunnel_type}"
                print("Invoking tunnel api:", tunnel_api)
                # do login
                session = requests.Session()
                login_response = session.request('POST', f"{HOST_API_DOMAIN}/login", json={"username": HOST_API_USER, "password": HOST_API_PASSWORD})
                # print("Login response:", login_response)
                if login_response.status_code == 200 :
                    response = session.request(method, tunnel_api, timeout=5)
                    print("got response:", response)
                    return response
                else:
                    raise requests.exceptions.HTTPError(login_response.status_code)

            try:
                if option == "on":
                    response = execute_tunnel_request().json()
                    message = f'Tunnel Details: \n URL: {response["url"]}'
                    if "remote_address" in response:
                        message = f'{message}\n Address:{response["remote_address"]}'
                else:
                    response = execute_tunnel_request()
                    message = "Tunnel is closed"
            except requests.exceptions.HTTPError as he:
                message = f"Failed to turn {option} the {tunnel_type} tunnel."
                print(traceback.format_exc())
            except Exception as ex:
                print("failed to open tunnel:", ex)
                print(traceback.format_exc())
                message = f"Unexpected error has occurred!: {str(ex)}"

            await context.bot.send_message(chat_id=chat_id, text=message)
    else:
        await context.bot.send_message(
            chat_id=chat_id, text="Please specify tunnel and option"
        )
