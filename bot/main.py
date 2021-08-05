# imports
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from bot.config import TG_TOKEN

from globals import *
from data_processing.loading import *


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# "start" move
def do_start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    add_to_current_or_create_user(user.id)
    cur_users[user.id].mode = 0
    update.message.reply_text(text=CHOOSE_THE_TOPIC, reply_markup=get_start_keyboard(update.message.from_user))
    save_data()


# "add" move
def do_add(update: Update, context: CallbackContext) -> None:
    add_to_current_or_create_user(update.message.from_user.id)
    cur_users[update.message.from_user.id].mode = 1
    update.message.reply_text(text="Type a new topic ✏️", reply_markup=get_back_to_start_keyboard())
    save_data()


# "delete" move
def do_delete(update: Update, context: CallbackContext) -> None:
    add_to_current_or_create_user(update.message.from_user.id)
    cur_users[update.message.from_user.id].mode = 2
    update.message.reply_text(text="Which topic do you want to delete? 🖍",
                              reply_markup=get_delete_keyboard(update.message.from_user))
    save_data()


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
    save_data()


# "settings" move
def do_settings(update: Update, context: CallbackContext) -> None:
    add_to_current_or_create_user(update.message.from_user.id)
    cur_users[update.message.from_user.id].mode = 3
    update.message.reply_text(text=CHOOSE_THE_TYPE_OF_SETTINGS, reply_markup=get_settings_keyboard())
    save_data()


# "input" move
def do_input(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    user = update.message.from_user
    add_to_current_or_create_user(user.id)
    if len(text) > 45:
        update.message.reply_text(
            text="This is too long message 😔",
            reply_markup=get_back_to_start_keyboard())
    elif cur_users[user.id].mode == 1:
        # "add" mode
        is_new = True
        for topic_class in cur_users[user.id].topics:
            if topic_class.name == text:
                is_new = False
        if is_new:
            add_theme(user.id, Topic(text, []))
            update.message.reply_text(
                text=text + " successfully added! ✅\nAlso you can fill your sources list in the /settings mode 😜",
                reply_markup=get_back_to_start_keyboard())
        else:
            update.message.reply_text(text="You already have this topic 😂",
                                      reply_markup=get_back_to_start_keyboard())
    elif cur_users[user.id].mode == 4:
        # "list settings" mode
        for i in range(0, len(cur_users[user.id].topics)):
            if cur_users[user.id].topics[i].name == cur_users[user.id].setting_topic_name:
                cur_users[user.id].topics[i].sites = []
                cur_users[user.id].topics[i].sites = text.split('\n')
        update.message.reply_text("List successfully fixed! ☑️", reply_markup=get_backs_keyboard())
    elif cur_users[user.id].mode == 5:
        # "new width" mode
        if represents_int(text):
            cur_users[user.id].width_of_keyboard = int(text)
            update.message.reply_text("Width successfully changed! 👌️", reply_markup=get_backs_keyboard())
        else:
            update.message.reply_text(text="It is not a number 😂", reply_markup=get_back_to_start_keyboard())
    else:
        # input the topic
        update.message.reply_text(text=news_message(text), reply_markup=get_back_to_start_keyboard())
    save_data()


def create_the_button(name):
    return InlineKeyboardButton(name, callback_data=name)


# "start" keyboard init
def fill_topics_keyboard(user):
    keyboard = [[]]
    line_index = 0
    # fill topics
    for i in range(0, len(cur_users[user.id].topics)):
        keyboard[line_index].append(create_the_button(cur_users[user.id].topics[i].name))
        if (i % cur_users[user.id].width_of_keyboard == cur_users[user.id].width_of_keyboard - 1) and (
                i != len(cur_users[user.id].topics) - 1):
            # new line
            keyboard.append([])
            line_index += 1
    return keyboard


# "delete" keyboard init
def get_delete_keyboard(user):
    keyboard = fill_topics_keyboard(user)
    keyboard.append([create_the_button(BACK_TO_START)])
    return InlineKeyboardMarkup(keyboard)


# "topics" in "settings" mode keyboard init
def get_topics_in_settings_keyboard(user):
    keyboard = fill_topics_keyboard(user)
    keyboard.append([create_the_button(BACK_TO_SETTINGS)])
    return InlineKeyboardMarkup(keyboard)


# "start" keyboard init
def get_start_keyboard(user):
    return InlineKeyboardMarkup(fill_topics_keyboard(user))


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
    user = query.from_user
    add_to_current_or_create_user(user.id)
    cur_users[user.id].mode = 0
    query.edit_message_text(text=CHOOSE_THE_TOPIC, reply_markup=get_start_keyboard(user))


# redrawing the last message to the "settings menu"
def redraw_to_settings(query):
    user = query.from_user
    cur_users[user.id].mode = 0
    cur_users[user.id].setting_topic_name = ""
    query.edit_message_text(text=CHOOSE_THE_TYPE_OF_SETTINGS, reply_markup=get_settings_keyboard())


def news_message(topic):
    return "Hey, nice choice! 👍\nHere are some " + topic + " news:\n" + find_news(topic)


# processing of all buttons
def keyboard_processing(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    pushed_button_name = query.data
    user = query.from_user
    add_to_current_or_create_user(user.id)
    # "topic" push
    for topic_class in cur_users[user.id].topics:
        if pushed_button_name == topic_class.name:
            if cur_users[user.id].mode == 2:
                # "delete" mode
                remove_theme(user.id, topic_class)
                redraw_to_start(query)
            elif cur_users[user.id].mode == 4:
                # "list settings" mode
                cur_users[user.id].setting_topic_name = topic_class.name
                text = "Here is your list: 📜\n"
                for site in topic_class.sites:
                    text += site + '\n'
                query.edit_message_text(text=text, reply_markup=get_view_list_keyboard())
            elif cur_users[user.id].mode == 5:
                # "keyboard settings" mode
                if cur_users[user.id].setting_topic_name == "":
                    # saving first topic
                    cur_users[user.id].setting_topic_name = topic_class.name
                    query.edit_message_text(text="Good job, now choose the second one ✌️",
                                            reply_markup=get_topics_in_settings_keyboard(user))
                else:
                    # swap making
                    first_index = -1
                    for i in range(0, len(cur_users[user.id].topics)):
                        if cur_users[user.id].topics[i].name == cur_users[user.id].setting_topic_name or \
                                cur_users[user.id].topics[i].name == topic_class.name:
                            if first_index == -1:
                                # saving first topic
                                first_index = i
                            else:
                                # swap making
                                cur_users[user.id].topics[i], cur_users[user.id].topics[first_index] = \
                                    cur_users[user.id].topics[first_index], cur_users[user.id].topics[i]
                                break
                    cur_users[user.id].setting_topic_name = ""
                    query.edit_message_text(text="Choose two topics, that you want to swap 🔄",
                                            reply_markup=get_topics_in_settings_keyboard(user))
                    break
            else:
                # "news" mode
                query.edit_message_text(text=news_message(topic_class.name), reply_markup=get_back_to_start_keyboard())
    # "list settings" push
    if pushed_button_name == LIST_SETTINGS:
        cur_users[user.id].mode = 4
        query.edit_message_text(text=CHOOSE_THE_LIST_TO_FIX, reply_markup=get_topics_in_settings_keyboard(user))
    # "keyboard settings" push
    if pushed_button_name == KEYBOARD_SETTINGS:
        cur_users[user.id].mode = 5
        query.edit_message_text(text="🙃", reply_markup=get_keyboard_settings_keyboard())
    # "fix the list" pushed
    if pushed_button_name == FIX_THE_LIST:
        query.edit_message_text(text="Please, type the list of sources, that you prefer 📚\n" +
                                     "Each one in the new line without extra words", reply_markup=get_backs_keyboard())
    # "change the width" pushed
    if pushed_button_name == CHANGE_THE_WIDTH:
        query.edit_message_text(text="Please, type a new width 🖊")
    # "change the placement" pushed
    if pushed_button_name == CHANGE_THE_PLACEMENT:
        query.edit_message_text(text="Choose two topics, that you want to swap 🔄",
                                reply_markup=get_topics_in_settings_keyboard(user))
    # "back to start" pushed
    if pushed_button_name == BACK_TO_START:
        redraw_to_start(query)
    # "back to settings" pushed
    if pushed_button_name == BACK_TO_SETTINGS:
        redraw_to_settings(query)
    save_data()


# parsing call
def find_news(topic):
    # TODO Slava's job here in the other file!!! You have to find the news about the current topic and return text
    return "Slava's job!"


def main() -> None:
    bot = Bot(token=TG_TOKEN)
    updater = Updater(bot=bot)
    #    load_all_data()
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
