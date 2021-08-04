# imports
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from bot.config import TG_TOKEN


# topic class
class Topic:
    def __init__(self, name, sites):
        self.name = name
        self.sites = sites


# array of buttons
TOPICS = [
    Topic("Sports", ["https://www.sports.ru", "https://www.skysports.com", "https://www.bbc.com/sport"]),
    Topic("Politics", ["https://meduza.io", "https://www.nbcnews.com/politics", "https://edition.cnn.com/politics"]),
    Topic("Weather", ["https://weather.com", "https://www.wunderground.com", "https://www.bbc.com/weather"]),
    Topic("IT", ["https://habr.com/ru/all", "https://www.bbc.com/news/technology", "https://medium.com/"]),
    Topic("Finance", ["https://finance.yahoo.com", "https://insight.factset.com", "https://www.stockgeist.ai"]),
    Topic("Movies", ["https://www.euronews.com/programs/cinema", "https://www.arte.tv/en/videos/cinema/cinema-news",
                     "https://www.empireonline.com/movies/news/"]),
    Topic("Music", ["https://nac-cna.ca/en/discover/music", "https://www.nme.com/news/music",
                    "https://www.rollingstone.com/music/music-news"]),
    Topic("Covid", ["https://www.worldometers.info/coronavirus", "https://covid19.who.int",
                    "https://www.un.org/en/coronavirus"]),
    Topic("Culture", ["https://www.slice.ca/", "https://www.rollingstone.com/culture/culture-news",
                      "https://www.euronews.com/lifestyle/culture"])
]

# Messages
CHOOSE_THE_TOPIC = "Choose or type the topic that interests you 👇"
CHOOSE_THE_LIST_TO_FIX = "Which topic's sources list do you want to fix? 🔧"

WIDTH_OF_KEYBOARD = 3

# extra button names
BACK_TO_START = "Back to the start menu ⬅️"
BACK_TO_SETTINGS = "Back to the setting menu 🛠"
FIX_THE_LIST = "Fix the list 📐"

# mode flag (0 - start mode, 1 - add mode, 2 - delete mode, 3 - settings mode)
MODE = 0

SETTINGS_TOPIC_NAME = Topic("", [])


# start move
def do_start(update: Update, context: CallbackContext) -> None:
    global MODE
    MODE = 0
    update.message.reply_text(text=CHOOSE_THE_TOPIC, reply_markup=get_start_keyboard())


# add move
def do_add(update: Update, context: CallbackContext) -> None:
    global MODE
    MODE = 1
    update.message.reply_text(text="Type a new topic ✏️", reply_markup=get_back_to_start_keyboard())


# delete move
def do_delete(update: Update, context: CallbackContext) -> None:
    global MODE
    MODE = 2
    update.message.reply_text(text="Which topic do you want to delete? 🖍", reply_markup=get_command_keyboard())


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
    global MODE
    MODE = 3
    update.message.reply_text(text=CHOOSE_THE_LIST_TO_FIX, reply_markup=get_command_keyboard())


# input move
def do_input(update: Update, context: CallbackContext) -> None:
    global MODE
    text = update.message.text
    if MODE == 1:
        # add mode
        TOPICS.append(Topic(text, []))
        update.message.reply_text(
            text=text + " successfully added! ✅\nAlso you can fill your sources list in the /settings mode 😜",
            reply_markup=get_back_to_start_keyboard())
    elif MODE == 3:
        # settings mode
        for i in range(0, len(TOPICS)):
            if TOPICS[i].name == SETTINGS_TOPIC_NAME:
                TOPICS[i].sites = []
                TOPICS[i].sites = text.split('\n')
        update.message.reply_text("List successfully fixed! ☑️", reply_markup=get_fix_the_list_keyboard())
    else:
        # input the topic
        update.message.reply_text(text=news_message(text), reply_markup=get_back_to_start_keyboard())


def create_the_button(name):
    return InlineKeyboardButton(name, callback_data=name)


# start keyboard init
def fill_topics_keyboard():
    keyboard = [[]]
    line_index = 0
    # fill topics
    for i in range(0, len(TOPICS)):
        keyboard[line_index].append(create_the_button(TOPICS[i].name))
        if (i % WIDTH_OF_KEYBOARD == WIDTH_OF_KEYBOARD - 1) and (i != len(TOPICS) - 1):
            # new line
            keyboard.append([])
            line_index += 1
    return keyboard


# delete and settings keyboard init
def get_command_keyboard():
    keyboard = fill_topics_keyboard()
    keyboard.append([create_the_button(BACK_TO_START)])
    return InlineKeyboardMarkup(keyboard)


# start keyboard init
def get_start_keyboard():
    return InlineKeyboardMarkup(fill_topics_keyboard())


# back to start keyboard init
def get_back_to_start_keyboard():
    return InlineKeyboardMarkup([[create_the_button(BACK_TO_START)]])


# back to setting keyboard init
def get_back_to_settings_keyboard():
    return InlineKeyboardMarkup([[create_the_button(BACK_TO_SETTINGS)]])


# settings keyboard init
def get_settings_keyboard():
    return InlineKeyboardMarkup([[create_the_button(FIX_THE_LIST)], [create_the_button(BACK_TO_SETTINGS)],
                                 [create_the_button(BACK_TO_START)]])


# fix the list keyboard init
def get_fix_the_list_keyboard():
    return InlineKeyboardMarkup([[create_the_button(BACK_TO_SETTINGS)], [create_the_button(BACK_TO_START)]])


# redrawing the last message to the start menu
def redraw_to_start(query):
    query.edit_message_text(text=CHOOSE_THE_TOPIC, reply_markup=get_start_keyboard())


# redrawing the last message to the settings menu
def redraw_to_settings(query):
    query.edit_message_text(text=CHOOSE_THE_LIST_TO_FIX, reply_markup=get_command_keyboard())


def news_message(topic):
    return "Hey, nice choice! 👍\nHere are some " + topic + " news:\n" + find_news(topic)


# processing of the start and back keyboards
def keyboard_processing(update: Update, context: CallbackContext) -> None:
    global MODE, SETTINGS_TOPIC_NAME
    query = update.callback_query
    query.answer()
    data = query.data
    # topic push
    for topic_class in TOPICS:
        if data == topic_class.name:
            if MODE == 2:
                # delete mode
                TOPICS.remove(topic_class)
                redraw_to_start(query)
            elif MODE == 3:
                # settings mode
                SETTINGS_TOPIC_NAME = topic_class.name
                text = "Here is your list: 📜\n"
                for site in topic_class.sites:
                    text += site + '\n'
                query.edit_message_text(text=text, reply_markup=get_settings_keyboard())
            else:
                # news mode
                query.edit_message_text(text=news_message(topic_class.name),
                                        reply_markup=get_back_to_start_keyboard())
    # fix the list
    if data == FIX_THE_LIST:
        query.edit_message_text(text="Please, type the list of sources, that you prefer 📚\n" +
                                     "Each one in the new line without extra words.",
                                reply_markup=get_fix_the_list_keyboard())
    # back to start push
    if data == BACK_TO_START:
        redraw_to_start(query)
        MODE = 0
    # back to settings push
    if data == BACK_TO_SETTINGS:
        redraw_to_settings(query)
        MODE = 3


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
