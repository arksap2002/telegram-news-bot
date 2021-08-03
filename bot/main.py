# imports
from telegram import (Bot,
                      Update,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          CallbackQueryHandler)
from bot.config import TG_TOKEN


# buttons inits
CALLBACK_BUTTON_SPORTS = "callback_button_sports"
CALLBACK_BUTTON_POLITICS = "callback_button_politics"
CALLBACK_BUTTON_OTHER = "callback_button_other"


# list of buttons
TITLES = {
    CALLBACK_BUTTON_SPORTS: "Sports",
    CALLBACK_BUTTON_POLITICS: "Politics",
    CALLBACK_BUTTON_OTHER: "Other"
}


# start move
def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Choose the topic",
        reply_markup=get_start_keyboard(),
    )


# start keyboard init
def get_start_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_SPORTS], callback_data=CALLBACK_BUTTON_SPORTS),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_SPORTS], callback_data=CALLBACK_BUTTON_SPORTS),
        ],
        InlineKeyboardButton(TITLES[CALLBACK_BUTTON_OTHER], callback_data=CALLBACK_BUTTON_OTHER),
    ]
    return InlineKeyboardMarkup(keyboard)


# processing of the start keyboard
def keyboard_processing(bot: Bot, update: Update, chat_data=None, **kwargs):
    query = update.callback_query
    data = query.data
    if data == CALLBACK_BUTTON_SPORTS:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Sports news:\n"
                 "todo!",  # TODO
        )
    if data == CALLBACK_BUTTON_POLITICS:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Politics news:\n"
                 "todo!",  # TODO
        )
    if data == CALLBACK_BUTTON_OTHER:
        text = update.message.text
        bot.send_message(
            chat_id=update.message.chat_id,
            text=text + "news:\n"
                        "todo!",  # TODO
        )


# parsing call
def find_news(topic):
    topic_tmp = topic  # TODO Slava's job here in the other file, i guess


def main():
    bot = Bot(token=TG_TOKEN, )
    updater = Updater(bot=bot, )

    start_handler = CommandHandler("start", do_start)
    buttons_handler = CallbackQueryHandler(callback=keyboard_processing, pass_chat_data=True)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(buttons_handler)

    # start input
    updater.start_polling()
    # do not exit too early
    updater.idle()


if __name__ == '__main__':
    main()
