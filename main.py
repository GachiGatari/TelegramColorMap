from func import get_color
from bot_handlers import image_handler, start_handler
import configparser
import json
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, MessageHandler, CallbackQueryHandler,Filters, CommandHandler



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read("settings.ini")
token = config["Telegram"]["token"]




def main() -> None:
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
    dispatcher.add_handler(CommandHandler('start',start_handler))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()





