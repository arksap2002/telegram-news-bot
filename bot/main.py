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

# messages
CHOOSE_THE_TOPIC = "Choose or type the topic that interests you 👇"
CHOOSE_THE_LIST_TO_FIX = "Which topic's sources list do you want to fix? 🔧"
CHOOSE_THE_TYPE_OF_SETTINGS = "Yo, welcome to the settings!\nSet me up for yourself! 🤙"

WIDTH_OF_KEYBOARD = 3

# extra button names
BACK_TO_START = "Back to the start menu ⬅️"
BACK_TO_SETTINGS = "Back to the setting menu 🛠"
FIX_THE_LIST = "Fix the list 📐"
LIST_SETTINGS = "Sources list settings 🗂"
KEYBOARD_SETTINGS = "Keyboard settings ⌨️"
CHANGE_THE_WIDTH = "Width of keyboard 📏"
CHANGE_THE_PLACEMENT = "Placement of buttons 🔀"

# mode flag
# (0 - "start" mode, 1 - "add" mode, 2 - "delete mode", 3 - "settings" mode)
#         (4 - "list settings" mode, 5 - "keyboard settings" mode)
MODE = 0

# what topics are you working to ("list settings" mode) and first pushed in the "swap" mode
SETTINGS_TOPIC_NAME = ""


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# "start" move
def do_start(update: Update, context: CallbackContext) -> None:
    global MODE
    MODE = 0
    update.message.reply_text(text=CHOOSE_THE_TOPIC, reply_markup=get_start_keyboard())


# "add" move
def do_add(update: Update, context: CallbackContext) -> None:
    global MODE
    MODE = 1
    update.message.reply_text(text="Type a new topic ✏️", reply_markup=get_back_to_start_keyboard())


# "delete" move
def do_delete(update: Update, context: CallbackContext) -> None:
    global MODE
    MODE = 2
    update.message.reply_text(text="Which topic do you want to delete? 🖍", reply_markup=get_delete_keyboard())


# "help" move
def do_help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text="You can control me by sending these commands: 🤟\n" +
             "/start - go back to the topics menu 🔥\n" +
             "/add - add a new topic ➕\n" +
             "/delete - delete some topic ➖\n" +
             "/settings - Configure the list of sources ⚙️\n" +
             "/help - enjoy the recursion ❗️",
        reply_markup=get_back_to_start_keyboard()
    )


# "settings" move
def do_settings(update: Update, context: CallbackContext) -> None:
    global MODE, SETTINGS_TOPIC_NAME
    MODE = 3
    SETTINGS_TOPIC_NAME = ""
    update.message.reply_text(text=CHOOSE_THE_TYPE_OF_SETTINGS, reply_markup=get_settings_keyboard())


# "input" move
def do_input(update: Update, context: CallbackContext) -> None:
    global MODE, WIDTH_OF_KEYBOARD
    text = update.message.text
    if MODE == 1:
        # "add" mode
        is_new = True
        for topic_class in TOPICS:
            if topic_class.name == text:
                is_new = False
        if is_new:
            TOPICS.append(Topic(text, []))
            update.message.reply_text(
                text=text + " successfully added! ✅\nAlso you can fill your sources list in the /settings mode 😜",
                reply_markup=get_back_to_start_keyboard())
        else:
            update.message.reply_text(text="You already have this topic 😂",
                                      reply_markup=get_back_to_start_keyboard())
    elif MODE == 4:
        # "list settings" mode
        for i in range(0, len(TOPICS)):
            if TOPICS[i].name == SETTINGS_TOPIC_NAME:
                TOPICS[i].sites = []
                TOPICS[i].sites = text.split('\n')
        update.message.reply_text("List successfully fixed! ☑️", reply_markup=get_backs_keyboard())
    elif MODE == 5:
        # "new width" mode
        if represents_int(text):
            WIDTH_OF_KEYBOARD = int(text)
            update.message.reply_text("Width successfully changed! 👌️", reply_markup=get_backs_keyboard())
        else:
            update.message.reply_text(text="It is not a number 😂", reply_markup=get_back_to_start_keyboard())
    else:
        # input the topic
        update.message.reply_text(text=news_message(text), reply_markup=get_back_to_start_keyboard())


def create_the_button(name):
    return InlineKeyboardButton(name, callback_data=name)


# "start" keyboard init
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


# "delete" keyboard init
def get_delete_keyboard():
    keyboard = fill_topics_keyboard()
    keyboard.append([create_the_button(BACK_TO_START)])
    return InlineKeyboardMarkup(keyboard)


# "topics" in "settings" mode keyboard init
def get_topics_in_settings_keyboard():
    keyboard = fill_topics_keyboard()
    keyboard.append([create_the_button(BACK_TO_SETTINGS)])
    return InlineKeyboardMarkup(keyboard)


# "start" keyboard init
def get_start_keyboard():
    return InlineKeyboardMarkup(fill_topics_keyboard())


# "back to start" keyboard init
def get_back_to_start_keyboard():
    return InlineKeyboardMarkup([[create_the_button(BACK_TO_START)]])


# "back to setting" keyboard init
def get_back_to_settings_keyboard():
    return InlineKeyboardMarkup([[create_the_button(BACK_TO_SETTINGS)]])


# "settings" keyboard init
def get_settings_keyboard():
    return InlineKeyboardMarkup([[create_the_button(LIST_SETTINGS)], [create_the_button(KEYBOARD_SETTINGS)],
                                 [create_the_button(BACK_TO_START)]])


# "view list" keyboard init
def get_view_list_keyboard():
    return InlineKeyboardMarkup([[create_the_button(FIX_THE_LIST)], [create_the_button(BACK_TO_SETTINGS)]])


# "fix the list" and "change the width" keyboard init
def get_backs_keyboard():
    return InlineKeyboardMarkup([[create_the_button(BACK_TO_SETTINGS)], [create_the_button(BACK_TO_START)]])


# "keyboard settings" keyboard init
def get_keyboard_settings_keyboard():
    return InlineKeyboardMarkup([[create_the_button(CHANGE_THE_WIDTH)], [create_the_button(CHANGE_THE_PLACEMENT)],
                                 [create_the_button(BACK_TO_SETTINGS)]])


# redrawing the last message to the "start menu"
def redraw_to_start(query):
    global MODE
    MODE = 0
    query.edit_message_text(text=CHOOSE_THE_TOPIC, reply_markup=get_start_keyboard())


# redrawing the last message to the "settings menu"
def redraw_to_settings(query):
    global MODE, SETTINGS_TOPIC_NAME
    MODE = 3
    SETTINGS_TOPIC_NAME = ""
    query.edit_message_text(text=CHOOSE_THE_TYPE_OF_SETTINGS, reply_markup=get_settings_keyboard())


def news_message(topic):
    return "Hey, nice choice! 👍\nHere are some " + topic + " news:\n" + find_news(topic)


# processing of all buttons
def keyboard_processing(update: Update, context: CallbackContext) -> None:
    global MODE, SETTINGS_TOPIC_NAME
    query = update.callback_query
    query.answer()
    pushed_button_name = query.data
    # "topic" push
    for topic_class in TOPICS:
        if pushed_button_name == topic_class.name:
            if MODE == 2:
                # "delete" mode
                TOPICS.remove(topic_class)
                redraw_to_start(query)
            elif MODE == 4:
                # "list settings" mode
                SETTINGS_TOPIC_NAME = topic_class.name
                text = "Here is your list: 📜\n"
                for site in topic_class.sites:
                    text += site + '\n'
                query.edit_message_text(text=text, reply_markup=get_view_list_keyboard())
            elif MODE == 5:
                # "keyboard settings" mode
                if SETTINGS_TOPIC_NAME == "":
                    print(SETTINGS_TOPIC_NAME, topic_class.name, "1")
                    # saving first topic
                    SETTINGS_TOPIC_NAME = topic_class.name
                    query.edit_message_text(text="Good job, now choose the second one ✌️",
                                            reply_markup=get_topics_in_settings_keyboard())
                else:
                    print(SETTINGS_TOPIC_NAME, topic_class.name, "2")
                    # swap making
                    first_index = -1
                    for i in range(0, len(TOPICS)):
                        if TOPICS[i].name == SETTINGS_TOPIC_NAME or TOPICS[i].name == topic_class.name:
                            if first_index == -1:
                                # saving first topic
                                first_index = i
                            else:
                                # swap making
                                TOPICS[i], TOPICS[first_index] = TOPICS[first_index], TOPICS[i]
                                break
                    SETTINGS_TOPIC_NAME = ""
                    query.edit_message_text(text="Choose two topics, that you want to swap 🔄",
                                            reply_markup=get_topics_in_settings_keyboard())
                    break
            else:
                # "news" mode
                query.edit_message_text(text=news_message(topic_class.name),
                                        reply_markup=get_back_to_start_keyboard())
    # "list settings" push
    if pushed_button_name == LIST_SETTINGS:
        MODE = 4
        query.edit_message_text(text=CHOOSE_THE_LIST_TO_FIX, reply_markup=get_topics_in_settings_keyboard())
    # "keyboard settings" push
    if pushed_button_name == KEYBOARD_SETTINGS:
        MODE = 5
        query.edit_message_text(text="🙃", reply_markup=get_keyboard_settings_keyboard())
    # "fix the list" pushed
    if pushed_button_name == FIX_THE_LIST:
        query.edit_message_text(text="Please, type the list of sources, that you prefer 📚\n" +
                                     "Each one in the new line without extra words",
                                reply_markup=get_backs_keyboard())
    # "change the width" pushed
    if pushed_button_name == CHANGE_THE_WIDTH:
        query.edit_message_text(text="Please, type a new width 🖊")
    # "change the placement" pushed
    if pushed_button_name == CHANGE_THE_PLACEMENT:
        query.edit_message_text(text="Choose two topics, that you want to swap 🔄",
                                reply_markup=get_topics_in_settings_keyboard())
    # "back to start" pushed
    if pushed_button_name == BACK_TO_START:
        redraw_to_start(query)
    # "back to settings" pushed
    if pushed_button_name == BACK_TO_SETTINGS:
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
