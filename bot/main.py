# imports
from telegram import (Bot,
                      Update,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (Updater,
                          CommandHandler,
                          CallbackQueryHandler,
                          CallbackContext)
from bot.config import TG_TOKEN

# Choose the topic message
CHOOSE_THE_TOPIC = "Choose the topic"


# topic class
class Topic:
    def __init__(self, topic_name, button_name):
        self.topic_name = topic_name
        self.button_name = button_name


# array of buttons
TOPICS = [
    Topic("Sports", "callback_button_sports"),
    Topic("Politics", "callback_button_politics"),
    Topic("Weather", "callback_button_weather"),
    Topic("Technology", "callback_button_technology"),
    Topic("Finance", "callback_button_finance"),
    Topic("Cinema", "callback_button_cinema"),
    Topic("Music", "callback_button_music"),
    Topic("Covid", "callback_button_covid"),
    Topic("Culture", "callback_button_culture")
]

OTHER = Topic("Other", "callback_button_other")

BACK = Topic("Back", "callback_button_back")

number_topics_in_the_line = 3


# start move
def do_start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text=CHOOSE_THE_TOPIC,
        reply_markup=get_start_keyboard()
    )


# start keyboard init
def get_start_keyboard():
    keyboard = [[]]
    line_index = 0
    # fill topics
    for i in range(0, len(TOPICS)):
        keyboard[line_index].append(InlineKeyboardButton(TOPICS[i].topic_name, callback_data=TOPICS[i].button_name))
        if (i % number_topics_in_the_line == number_topics_in_the_line - 1) and (i != len(TOPICS) - 1):
            # new line
            keyboard.append([])
            line_index += 1
    # add other
    keyboard.append([InlineKeyboardButton(OTHER.topic_name, callback_data=OTHER.button_name)])
    return InlineKeyboardMarkup(keyboard)


# back keyboard init
def get_back_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(BACK.topic_name, callback_data=BACK.button_name),
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
        if data == topic.button_name:
            query.edit_message_text(
                text=topic.topic_name + " news:\nSlava's job!",  # TODO Slava find_news(sports)
                reply_markup=get_back_keyboard()
            )
    # other push
    if data == OTHER.button_name:
        query.edit_message_text(
            text="Type the topic"
        )
        # topic = update.message.text TODO fix it!!!
        # query.edit_message_text(
        #     text=topic + " news:\nSlava's job!",  # TODO Slava find_news(topics)
        # )
    # back push
    if data == BACK.button_name:  # TODO fix copy/paste
        query.edit_message_text(
            text=CHOOSE_THE_TOPIC,
            reply_markup=get_start_keyboard()
        )


# parsing call
def find_news(topic) -> None:
    topic_tmp = topic  # TODO Slava's job here in the other file, i guess


def main() -> None:
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
