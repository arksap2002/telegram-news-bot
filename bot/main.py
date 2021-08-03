import logging

from parser import get_topics, get_href
from config import TG_TOKEN

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ParseMode
)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
MAIN, GET, EXIT = range(3)
# Callback data
CMAIN, CGET, smth1, CEXIT = range(4)
#dict of tops with links

def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton("theme", callback_data=str(CGET)),
        ],

        [
            InlineKeyboardButton("exit", callback_data=str(CEXIT)),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)

    return MAIN

def start_over(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s started_over the conversation.", user.first_name)

    keyboard = [
        [
            InlineKeyboardButton("theme", callback_data=str(CGET)),
        ],

        [
            InlineKeyboardButton("exit", callback_data=str(CEXIT)),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)

    return MAIN


def get(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    user = update.message.from_user

    logger.info("User %s in get func, got text: %s", user.first_name, text)

    reply_keyboard = [["1", "2", "3"]]

    tops = get_topics(text)
    text = "choose one of this topics:\n1)" + get_href(tops[0]) + "\n2)" + get_href(tops[1]) + "\n3)" + get_href(tops[2])

    update.message.reply_text(text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Number of topic?',
            parse_mode=ParseMode.HTML
        ),
    )

    return MAIN

def pre_get(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.callback_query.from_user
    query.answer()

    logger.info("User %s in pre_get func", user.first_name)

    query.edit_message_text(text="Enter theme pls:")
    return GET

def exit_(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user = update.callback_query.from_user
    query.answer()

    logger.info("User %s in exit func", user.first_name)

    return MAIN


def main():
    updater = Updater(TG_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                MAIN: [
                        CallbackQueryHandler(start_over, pattern='^' + str(CMAIN) + '$'),
                        CallbackQueryHandler(pre_get, pattern='^' + str(CGET) + '$'),
                        CallbackQueryHandler(exit_, pattern='^' + str(CEXIT) + '$'),
                    ],
                GET: [
                        MessageHandler(
                            Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                            get,
                        )
                    ],
                EXIT: [
                    ],
                },
            fallbacks=[CommandHandler("start", start)],
        )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()