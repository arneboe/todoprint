from escpos.printer import Usb
from telegram.ext import Updater
import logging
from print_bot import PrintBot


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.INFO)
    updater = Updater(token='')

    # printer = Usb(0x0416, 0x5011, 0, 0x81, 0x03)
    # printer.set(font="a", double_width=True, double_height=True, align="center", bold=True)
    # printer.text("     TODO     \n")
    # printer.set(font="a", align="center", bold=True)
    # printer.text("---------------\n")
    # printer.text("\n")
    # printer.text("\n")
    # exit()
    bot = PrintBot(updater.dispatcher)


    updater.start_polling()
    updater.idle()
