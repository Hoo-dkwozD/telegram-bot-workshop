import logging
from logging import Logger
import os
import telegram
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext, Dispatcher, Filters, MessageHandler, Updater
from dotenv import load_dotenv

## Setup logger's configs
logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level = logging.INFO
)

## Instantiate logger
logger: Logger = logging.getLogger(__name__)

## Load environment variables
load_dotenv("./.env")
TOKEN: str = os.getenv("TOKEN")

## Main app functionalities
def start(update: Update, context: CallbackContext) -> None:
    """
    Sends a message when `/start` command is issued. 

    :param Update update: The core object used to update the chat. 
    :param CallbackContext context: The context object. 

    :return None: `None` returned. 
    """

    update.message.reply_text("<b>Hello World!</b>", parse_mode = ParseMode.html)

def echo(update: Update, context: CallbackContext) -> None:
    """
    Replies the user with the same message they have sent. 

    :param Update update: The core object used to update the chat. 
    :param CallbackContext context: The context object. 

    :return None: `None` returned. 
    """

    message: str = update.message.text
    update.message.reply_text(message)

def error_handling(update: Update, context: CallbackContext) -> None:
    """
    Logs all errors or messages caused by updates. 

    :param Update update: The core object used to update the chat. 
    :param CallbackContext context: The context object. 

    :return None: `None` returned. 
    """

    logger.warning(f"Update {update} caused error {context}")

def main() -> None:
    """
    The driver code that instantiates the bot, gathers its functionalities and runs the bot. 

    :return None: `None` returned. 
    """

    # Instantiate the bot by passing the token into Updater
    updater: Updater = Updater(TOKEN)

    # Retrieve Dispatcher from Updater object
    dispatcher: Dispatcher = updater.dispatcher

    # Add the `/start` command handler
    dispatcher.add_handler(CommandHandler("start", start))

    # Add `text`-based reply handler 
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Add error handler
    dispatcher.add_error_handler(error_handling)

    # Runs bot
    updater.start_polling()

    # Runs bot until `Ctrl-C` issued on console
    updater.idle()

## Runs only as main script
if __name__ == "__main__":
    main()