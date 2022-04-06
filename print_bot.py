from escpos.exceptions import USBNotFoundError
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Dispatcher
from escpos.printer import Usb
from telegram import Update
import logging

class PrintBot:
    def __init__(self, dispatcher: Dispatcher):
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self._msg_handler))
        self.job = dispatcher.job_queue.run_repeating(self._timer_handler, interval=10, first=1, context=None)
        self.message_q = []

    def _timer_handler(self, param):
        if len(self.message_q) > 0:
            try:
                printer = Usb(0x0416, 0x5011, 0, 0x81, 0x03)
                self._print_buffered_messages(printer)
            except USBNotFoundError:
                print("ERRORORORORORORORORROR")
                # this happens when the printer is not turned on
                pass

    def _print_buffered_messages(self, printer: Usb):
        text = self.message_q.pop(0)
        try:
            printer.set(font="a", double_width=True, double_height=True, align="center", bold=True)
            printer.text("     TODO     \n\n")
            printer.set(font="a", align="left", bold=True)
            printer.text(text)
            printer.print_and_feed(5)

        except:
            logging.error("exception while printing")
            # assume that the text has not been printed and put it back in the queue
            self.message_q.append(text)

    def _msg_handler(self, update: Update, context: CallbackContext):
        self.message_q.append(update.message.text)
        update.message.reply_text("Got it!")
