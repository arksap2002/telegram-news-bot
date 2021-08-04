import time

all_users = dict()
current_users = dict()
save_frequency = 10
data_filename = "user_data.pkl"
curr_time = time.time()


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
