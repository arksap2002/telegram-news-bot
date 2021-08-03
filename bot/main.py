# imports
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from bot.config import TG_TOKEN

# Messages
CHOOSE_THE_TOPIC = "Choose or type the topic that interests you 👇"
CHOOSE_THE_LIST_TO_FIX = "Which topic's sources list do you want to fix? 🔧"


# topic class
class Theme:
    def __init__(self, topic_name, sites):
        self.topic_name = topic_name
        self.button_name = "callback button " + topic_name
        self.sites = sites


# array of buttons
TOPICS = [
    Theme("Sports", ["https://www.sports.ru", "https://www.skysports.com", "https://www.bbc.com/sport"]),
    Theme("Politics", ["https://meduza.io", "https://www.nbcnews.com/politics", "https://edition.cnn.com/politics"]),
    Theme("Weather", ["https://weather.com", "https://www.wunderground.com", "https://www.bbc.com/weather"]),
    Theme("IT", ["https://habr.com/ru/all", "https://www.bbc.com/news/technology", "https://medium.com/"]),
    Theme("Finance", ["https://finance.yahoo.com", "https://insight.factset.com", "https://www.stockgeist.ai"]),
    Theme("Movies", ["https://www.euronews.com/programs/cinema", "https://www.arte.tv/en/videos/cinema/cinema-news",
                     "https://www.empireonline.com/movies/news/"]),
    Theme("Music", ["https://nac-cna.ca/en/discover/music", "https://www.nme.com/news/music",
                    "https://www.rollingstone.com/music/music-news"]),
    Theme("Covid", ["https://www.worldometers.info/coronavirus", "https://covid19.who.int",
                    "https://www.un.org/en/coronavirus"]),
    Theme("Culture", ["https://www.slice.ca/", "https://www.rollingstone.com/culture/culture-news",
                      "https://www.euronews.com/lifestyle/culture"])
]

BACK_TO_START = Theme("Back to the start menu ⬅️", [])

BACK_TO_SETTINGS = Theme("Back to the setting menu 🛠️", [])

NUMBER_TOPICS_IN_THE_LINE = 3

DELETE_MODE = False

ADD_MODE = False

SETTING_MODE = False


# start move
def do_start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text=CHOOSE_THE_TOPIC,
        reply_markup=get_start_keyboard()
    )


# add move
def do_add(update: Update, context: CallbackContext) -> None:
    global ADD_MODE
    ADD_MODE = True
    update.message.reply_text(
        text="Type a new topic ✏️",
        reply_markup=get_back_to_start_keyboard()
    )


# delete move
def do_delete(update: Update, context: CallbackContext) -> None:
    global DELETE_MODE
    DELETE_MODE = True
    update.message.reply_text(
        text="Which topic do you want to delete? 🖍",
        reply_markup=get_command_keyboard()
    )


# help move
def do_help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="You can control me by sending these commands: 🤟\n" +
             "/start - go back to the topics menu 🔥\n" +
             "/add - add a new topic ➕\n" +
             "/delete - delete some topic ➖\n" +
             "/setting - Configure the list of sources ⚙️\n" +
             "/help - enjoy the recursion ❗️",
        reply_markup=get_back_to_start_keyboard()
    )


# settings move
def do_settings(update: Update, context: CallbackContext) -> None:
    global SETTING_MODE
    SETTING_MODE = True
    update.message.reply_text(
        text=CHOOSE_THE_LIST_TO_FIX,
        reply_markup=get_command_keyboard()
    )


# input move
def do_input(update: Update, context: CallbackContext) -> None:
    global ADD_MODE
    topic = update.message.text
    if ADD_MODE:
        TOPICS.append(Theme(topic, []))
        ADD_MODE = False
        update.message.reply_text(
            text=topic + " successfully added! ✅\nAlso you can fill your sources list in the /settings mode 😜",
            reply_markup=get_back_to_start_keyboard()
        )
    else:
        update.message.reply_text(
            text=news_message(topic),
            reply_markup=get_back_to_start_keyboard()
        )


# start keyboard init
def fill_topics_keyboard():
    keyboard = [[]]
    line_index = 0
    # fill topics
    for i in range(0, len(TOPICS)):
        keyboard[line_index].append(InlineKeyboardButton(TOPICS[i].topic_name, callback_data=TOPICS[i].button_name))
        if (i % NUMBER_TOPICS_IN_THE_LINE == NUMBER_TOPICS_IN_THE_LINE - 1) and (i != len(TOPICS) - 1):
            # new line
            keyboard.append([])
            line_index += 1
    return keyboard


# delete and settings keyboard init
def get_command_keyboard():
    keyboard = fill_topics_keyboard()
    # add back
    keyboard.append([InlineKeyboardButton(BACK_TO_START.topic_name, callback_data=BACK_TO_START.button_name)])
    return InlineKeyboardMarkup(keyboard)


# start keyboard init
def get_start_keyboard():
    keyboard = fill_topics_keyboard()
    return InlineKeyboardMarkup(keyboard)


# back to start keyboard init
def get_back_to_start_keyboard():
    keyboard = [[InlineKeyboardButton(BACK_TO_START.topic_name, callback_data=BACK_TO_START.button_name)]]
    return InlineKeyboardMarkup(keyboard)


# back to setting keyboard init
def get_back_to_settings_keyboard():
    keyboard = [[InlineKeyboardButton(BACK_TO_SETTINGS.topic_name, callback_data=BACK_TO_SETTINGS.button_name)]]
    return InlineKeyboardMarkup(keyboard)


# settings keyboard init
def get_settings_keyboard():
    keyboard = [[InlineKeyboardButton(BACK_TO_SETTINGS.topic_name, callback_data=BACK_TO_SETTINGS.button_name)],
                [InlineKeyboardButton(BACK_TO_START.topic_name, callback_data=BACK_TO_START.button_name)]]
    # add backs
    return InlineKeyboardMarkup(keyboard)


# redrawing the last message to the start menu
def redraw_to_start(query):
    query.edit_message_text(
        text=CHOOSE_THE_TOPIC,
        reply_markup=get_start_keyboard()
    )


# redrawing the last message to the settings menu
def redraw_to_settings(query):
    query.edit_message_text(
        text=CHOOSE_THE_LIST_TO_FIX,
        reply_markup=get_command_keyboard()
    )


def news_message(topic):
    return "Hey, nice choice! 👍\nHere are some " + topic + " news:\n" + find_news(topic)


# processing of the start and back keyboards
def keyboard_processing(update: Update, context: CallbackContext) -> None:
    global DELETE_MODE, ADD_MODE, SETTING_MODE
    query = update.callback_query
    query.answer()
    data = query.data
    # topic push
    for topic_class in TOPICS:
        if data == topic_class.button_name:
            if DELETE_MODE:
                # delete mode
                TOPICS.remove(topic_class)
                DELETE_MODE = False
                redraw_to_start(query)
            elif SETTING_MODE:
                # settings mode
                text = "Here is your list: 📜\n"
                for site in topic_class.sites:
                    text += site + '\n'
                query.edit_message_text(
                    text=text,
                    reply_markup=get_settings_keyboard()
                )
            else:
                # news mode
                query.edit_message_text(
                    text=news_message(topic_class.topic_name),
                    reply_markup=get_back_to_start_keyboard()
                )
    # back to start push
    if data == BACK_TO_START.button_name:
        redraw_to_start(query)
        DELETE_MODE = False
        ADD_MODE = False
        SETTING_MODE = False
    # back to settings push
    if data == BACK_TO_SETTINGS.button_name:
        redraw_to_settings(query)


# parsing call
def find_news(topic):
    # TODO Slava's job here in the other file!!! You have to find the news about the current topic and return text
    return "Slava's job!"


def main() -> None:
    bot = Bot(token=TG_TOKEN)
    updater = Updater(bot=bot)

    updater.dispatcher.add_handler(CommandHandler("start", do_start))
    updater.dispatcher.add_handler(CommandHandler("add", do_add))
    updater.dispatcher.add_handler(CommandHandler("delete", do_delete))
    updater.dispatcher.add_handler(CommandHandler("help", do_help))
    updater.dispatcher.add_handler(CommandHandler("settings", do_settings))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, do_input))
    updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_processing))

    # start input
    updater.start_polling()
    # do not exit too early
    updater.idle()


if __name__ == '__main__':
    main()
