import traceback
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext, CallbackQueryHandler, InvalidCallbackData
from telegram import Update
from commands import download, tunnel
from common.decorators import AdminOnly
from common import config


@AdminOnly
async def start(update: Update, context: CallbackContext):
    chat_id=update.effective_chat.id
    # args = context.args
    context.bot.send_message(chat_id=chat_id, text="Hey Admin, please talk to me!")    

async def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry I can't understand your request!")

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    print("Exception while handling an update:", context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    print("error desc:", tb_string)
    if update.effective_chat:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I'm Unable to process your request. Please try after sometime.")
    else:
        print("Couldn't get any chat info!!")
    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    # update_str = update.to_dict() if isinstance(update, Update) else str(update)
    # message = (
    #     f"An exception was raised while handling an update\n"
    #     f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
    #     "</pre>\n\n"
    #     f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
    #     f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
    #     f"<pre>{html.escape(tb_string)}</pre>"
    # )

    # Finally, send the message
    # context.bot.send_message(
    #     chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    # )


def main(): 
    application = Application.builder().token(config.get_token()).arbitrary_callback_data(True).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('tunnel', tunnel.call))
    application.add_handler(CommandHandler('download', download.call))
    # download
    application.add_handler(CallbackQueryHandler(download.handle_invalid_button, pattern=InvalidCallbackData))
    application.add_handler(CallbackQueryHandler(download.handle_reply))

    ## fallback handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # error handler
    application.add_error_handler(error_handler)


    print("Started bot..")
    application.run_polling()
    application.idle()

if __name__ == "__main__":
    main()
