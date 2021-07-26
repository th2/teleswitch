#!/usr/bin/env python

import config
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def status(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == config.userId:
        update.message.reply_text('running')

def echo(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == config.userId:
        update.message.reply_text(f'unknown: {update.message.text}')

def main() -> None:
    updater = Updater(config.token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('status', status))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.bot.send_message(config.userId, 'bot started')

    updater.start_polling()

    # Run the bot until the process receives SIGINT, SIGTERM or SIGABRT
    # start_polling() is non-blocking and will stop the bot gracefully
    updater.idle()

if __name__ == '__main__':
    main()
