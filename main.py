from telegram.ext import Updater
import logging
from print_bot import PrintBot
import os

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.INFO)
    if "BOT_TOKEN" not in os.environ:
        logging.error("BOT_TOKEN not set")
        exit(-1)

    token = os.environ["BOT_TOKEN"]
    updater = Updater(token=token)
    bot = PrintBot(updater.dispatcher)
    updater.start_polling()
    updater.idle()
