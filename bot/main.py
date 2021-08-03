# imports
from telegram import (Bot,
                      Update,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          CallbackQueryHandler,
                          CallbackContext)
from bot.config import TG_TOKEN

# Choose the topic message
CHOOSE_THE_TOPIC = "Choose the topic"

# array of buttons
# TODO make the class
TOPICS = [
    ["Sports", "callback_button_sports"],
    ["Politics", "callback_button_politics"]
]

# other button init
OTHER = ["Other", "callback_button_other"]

# back button init
BACK = ["Back", "callback_button_back"]


# start move
def do_start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text=CHOOSE_THE_TOPIC,
        reply_markup=get_start_keyboard()
    )


# start keyboard init
def get_start_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TOPICS[0][0], callback_data=TOPICS[0][1]),
            InlineKeyboardButton(TOPICS[1][0], callback_data=TOPICS[1][1])
        ],
        [
            InlineKeyboardButton(OTHER[0], callback_data=OTHER[1])
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# back keyboard init
def get_back_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(BACK[0], callback_data=BACK[1]),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# processing of the start and back keyboards
def keyboard_processing(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data
    # topic push
    for topic in TOPICS:
        if data == topic[1]:
            query.edit_message_text(
                text=topic[0] + " news:\ntodo!",  # TODO find_news(sports)
                reply_markup=get_back_keyboard()
            )
    # other push
    if data == OTHER[1]:
        query.edit_message_text(
            text="Type the topic"
        )
        # topic = update.message.text TODO fix it!!!
        # query.edit_message_text(
        #     text=topic + " news:\ntodo!",  # TODO find_news(topics)
        # )
    # back push
    if data == BACK[1]:  # TODO fix copy/paste
        query.edit_message_text(
            text=CHOOSE_THE_TOPIC,
            reply_markup=get_start_keyboard()
        )


# parsing call
def find_news(topic):
    topic_tmp = topic  # TODO Slava's job here in the other file, i guess


def main():
    bot = Bot(token=TG_TOKEN, )
    updater = Updater(bot=bot, )

    updater.dispatcher.add_handler(CommandHandler("start", do_start))
    updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_processing))

    # start input
    updater.start_polling()
    # do not exit too early
    updater.idle()


if __name__ == '__main__':
    main()
