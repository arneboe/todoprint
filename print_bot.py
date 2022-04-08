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
                printer = Usb(0x0416, 0x5011)
                self._print_buffered_messages(printer)
                printer.close()
            except USBNotFoundError:
                #print("ERRORORORORORORORORROR")
                # this happens when the printer is not turned on
                pass

    def _print_header(self, text: str, printer: Usb):
        printer.set(font="a", double_width=True, double_height=True, align="center", bold=True)
        if " " in text:
            header = text.split(" ", 1)[0]
            printer.textln(header.upper())
        else:
            printer.textln(text)

    def _print_footer(self, text: str, printer: Usb):
        if " " in text:
            printer.set(font="a", align="left", bold=True)
            footer = text.split(" ", 1)[1]
            printer.textln(footer)

    def _print_buffered_messages(self, printer: Usb):
        while len(self.message_q) > 0:
            text = self.message_q.pop(0)
            try:
                self._print_header(text, printer)
                printer.ln(1)
                self._print_footer(text, printer)
                printer.ln(3)
            except Exception as e:
                logging.error("exception while printing")
                logging.error(str(e))
                # assume that the text has not been printed and put it back in the queue
                self.message_q.append(text)

    def _msg_handler(self, update: Update, context: CallbackContext):
        self.message_q.append(update.message.text)
        update.message.reply_text("Got it!")
