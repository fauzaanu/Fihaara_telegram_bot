import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler
import os
import requests

from main import etukuri_search

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)


async def all_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    if "#etukuri" in message:
        bot_response = etukuri_search(message.replace("#etukuri",""))

        # {'name': {'ACER CB282KS 28" LED Monitor (28" 4K UHD| 3840 x 2160)'},
        #   'link': {'https://shop.etukuri.mv/products/acer-cb282ks-28-led-monitor-28-4k-uhd-3840-x-2160'},
        #   'image': 'https://s3.amazonaws.com/s3.etukuri.mv/p9akZWd5/a1wni3ap.jpg'}
        print(bot_response)

        for item in bot_response:
            name = item['name']
            link = item['link']
            image = item['image']

            await context.bot.sendPhoto(chat_id=update.effective_chat.id, caption=f"<b><a href='{link}'>{name}</a></b>", photo=link, parse_mode="html")


# working part
async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="This is an unofficial etukuri search bot. To Search send a search term with #etukuri")


if __name__ == '__main__':
    token = ""
    application = ApplicationBuilder().token(token).build()

    commands = CommandHandler('start', start_command_handler)
    links = MessageHandler(filters.TEXT, all_text_handler)

    application.add_handler(commands)
    application.add_handler(links)

    application.run_polling()
