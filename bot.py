#!/usr/bin/env python

import config
import logging
import threading
from PIL import ImageGrab
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(config.token)

def status(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == config.userId:
        update.message.reply_text('running')

def screenshot(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == config.userId:
        screenshot = ImageGrab.grab(all_screens=True)
        screenshot.save(r'temp/screenshot.png')
        update.message.reply_photo(open('temp/screenshot.png', 'rb'))

def stop(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == config.userId:
        update.message.reply_text('shutting down')
        threading.Thread(target=shutdown).start()

def shutdown():
    updater.stop()
    updater.is_idle = False

def echo(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == config.userId:
        update.message.reply_text(f'unknown: {update.message.text}')

def main() -> None:
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_handler(CommandHandler('screenshot', screenshot))
    dispatcher.add_handler(CommandHandler('stop', stop))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.bot.send_message(config.userId, 'bot started')

    updater.start_polling()

    # Run the bot until the process receives SIGINT, SIGTERM or SIGABRT
    # start_polling() is non-blocking and will stop the bot gracefully
    updater.idle()

if __name__ == '__main__':
    main()
