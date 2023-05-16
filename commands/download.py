from pathlib import Path
import sys
from typing import List
from telegram.ext import CallbackContext
import urllib, ssl
import requests
import yt_dlp
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputMedia, InputTextMessageContent, KeyboardButton, ReplyKeyboardMarkup, Update
from common.decorators import exit_after
from common.models import Media, MediaMetadata
from common.util import default_if_empty, find_handler
from resp_parser import youtube, insta, generic
import filetype
import urllib.parse
from telegram.constants import ParseMode
from html import escape
from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from uuid import uuid4

MIME_HANDLERS = {
    '^image': lambda context: context.bot.send_photo,
    '^video': lambda context: context.bot.send_video,
    '^audio': lambda context: context.bot.send_audio,
    '^(?!text\/html).+': lambda context: context.bot.send_document
}

RESP_PARSERS = {
    '^youtube' : lambda: youtube, 
    '^instagram' : lambda: insta, 
    '.*': lambda: generic,
}


def _find_url_handler(url, ):
    response = requests.get(url)
    content_type = response.headers['content-type']
    return find_handler(MIME_HANDLERS, content_type)


def _eval_extension(url_resp):
    ft = filetype
    for kind in ft.types:
        if kind.mime == url_resp.headers.get_content_type():
            return kind.extension
        
    return None


def _eval_file_name(url_resp):
    result = urllib.parse.urlparse(url_resp.url)
    return Path(result.path).name


@exit_after(10)
async def _upload_and_send(bot_fn, chat_id: str, url: str,):
    with urllib.request.urlopen(url, context=ssl._create_unverified_context()) as vf:
        file_name = default_if_empty(_eval_file_name(vf), 'download')
        if '.' not in file_name:
            file_ext = default_if_empty(_eval_extension(vf), 'dat')
            file_name = file_name + '.' + file_ext            
        return await bot_fn(chat_id, vf, filename=file_name)
    

async def _send_url_or_file(bot_fn, chat_id: str, url: str,):
    print("sending as url first")
    try:
        return await bot_fn(chat_id, url)
    except:
        print("url send failed... so sending actual file")
        return await _upload_and_send(bot_fn, chat_id, url)
    

def _build_download_buttons(media_list: List[Media]):
    return [InlineKeyboardButton(f'Download ({default_if_empty(m.title, "")})', callback_data=(uuid4(), m.url)) for m in media_list]

async def _ask_user(update: Update, _: CallbackContext, metadata: MediaMetadata):
    media_list = metadata.items
    reply_markup = InlineKeyboardMarkup.from_row(_build_download_buttons(media_list))
    # InlineQueryResultArticle()
    html=f'''
        <b>{default_if_empty(metadata.title, "No title")}</b>
        Found multiple items to download!!
    '''.strip()
    await update.message.reply_html(text=html, reply_markup=reply_markup)

    
async def _send_embedded_files(update: Update, context: CallbackContext, input_url):
    chat_id = update.effective_chat.id
    with yt_dlp.YoutubeDL() as ytdlp:
        info = ytdlp.extract_info(input_url, download=False)
        resp_parser = find_handler(RESP_PARSERS, info['extractor'])
        if resp_parser:
            media_metadata: MediaMetadata = resp_parser().parse(info)
            media_items: List[Media] = media_metadata.items
            if len(media_items) == 1:
                embedded_url = media_items[0].url
                handler = _find_url_handler(embedded_url)
                bot_method = handler(context) if handler else None
                if bot_method:
                    return await _send_url_or_file(bot_method, chat_id, embedded_url)
            elif len(media_items) > 1:
                print("Got more than 1 item..asking user to choose the appropriate resource")
                return await _ask_user(update, context, media_metadata)
                    
    raise ValueError("Sorry, I can't handle this type of link")


async def handle_reply(update: Update, context: CallbackContext):
    query = update.callback_query
    _, data = query.data
    await query.answer("Please wait while I'm download the file...")
    context.args = [data]

    inline_keyboard_buttons = []
    for entry in query.message.reply_markup.inline_keyboard:
        inline_keyboard_buttons.append(tuple([f for f in list(entry) if f.callback_data != query.data]))

    # query.edit_message_text(text=query.message.text_html, parse=ParseMode.HTML)
    await call(update, context)
    await query.edit_message_reply_markup(reply_markup = InlineKeyboardMarkup(tuple(inline_keyboard_buttons)))
    # pass


async def handle_invalid_button(update: Update, context: CallbackContext) -> None:
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕 Please send a fresh download request."
    )


async def call(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args
    url = args[0]
    handler = _find_url_handler(url)
    if not handler:
        print("couldn't find the handler, finding embedded links")
        await _send_embedded_files(update, context, url)
        # try:
        #     return await _send_embedded_files(update, context, url)
        # except Exception as ex:
        #     print("Error occured!!", sys.exc_info()[0])
        #     await update.message.reply_text("Sorry, I'm unable to handle your request. Please try after sometime.")
    else:
        await _send_url_or_file(handler(context), chat_id, url)
        print("Finished sending the url content")
