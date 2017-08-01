"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
import math
import webbrowser

# initial greeting keywords
GREETING_WORDS = ["hello", "hey", "hi", "yo", "sup", "whatsup", "hi there","sup dude","how's it going?","hey there",
                  "yoo","hi!","hello!","hey!","thanks!","thanks","shalom","good","ok","alright","arite","fine","ok thanks"
                  "not bad","solid","awesome!","awesome","not much","i'm good","just chilling","not great","been better",
                  "eh","sick","not too good", "beseder", "sababa", "sababa achi","achla","chilling","good man","good bro"]
BOT_GREETING_WORDS = ["how are you?", "ma koreh?", "how you doin?", "how can I help you today?", "wazzzup??",
                      "sup dawg","what's going on?","ma nishma achi?","my man! what's going on?","sup dog?"
                      "whats good?","whats new?","how we doin today?"]

#alert user if any of these words are used
BAD_WORDS = ['fuck', 'shit', 'bitch', 'asshole', 'douchebag', 'fag', 'dick','idiot','fucker','piece of shit']

#used to get user to choose an initial keyword
KEYWORD_LIST = ["weather","sports","israel","time","day","date","night","food","restaurant","tel aviv","jerusalem","beach",
              "summer","vacation","hiking","shopping","clothing","movies"]
BOT_KEYWORD_SUGGEST = "Could you please suggest a keyword that relates to what you would like me to help you with? (ex: " + random.choice(KEYWORD_LIST) +")"

# narrow down keywords with a specific topic
TOPIC_LIST = ["weather, shopping","food","tel aviv","movies","vacation","time"]
BOT_TOPIC_SUGGEST = "Could you please suggest a keyword that is more specific to our current topic?"

#if user does not input a relevant keyword/topic
DONT_UNDERSTAND_YOU = "Sorry, I don't understand you"
RESET_CHAT = "Let's chat about a new topic"

#keywords for each specific topic
WEATHER_LIST = ["weather","summer","tel aviv","temperature","high","low","humidity","average","cloudy","clouds","rain","sun",
                "sunshine","snow","hail","hot","cold","mild"]
SHOPPING_LIST = ["shopping","clothing","dress","jeans","buy","clothes","shorts","shoes","towels","bed","bathing suit","hat","pants","t-shirt",
                 "tshirt","socks","sandals","flip flops","buy","shop"]
MOVIES_LIST = ["movies","action","comedy","thriller","scary","funny","kids","adult","long","superhero","series","popcorn","theatre","film",
               "famous","celebrity","movie","television","cinema"]
FOOD_LIST = ["food," "falafel","israeli","burgers","italian","indian","healthy","salad","breakfast","lunch","dinner","snack","shwarma",
             "pizza","bite","eat","eating","brunch","munch"]
TEL_AVIV_LIST = ["tel aviv","beach","bike","biking","hiking","haifa","jerusalem","eilat","negev","north","golan","city","cities"]
VACATION_LIST = ["vacation","greece","italy","cyprus","relax","family","boyfriend","girlfriend","where should I go",
                 "europe","asia","usa","united states","new york","visit","abroad"]
TIME_LIST = ["time","hour","minute","sleep","hours","minutes","clock","watch"]
RESET_LIST = ["reset", "yes","restart","sure","yea","definitely","yep","yup","please","ok", "new topic", "change","topic","please reset","yes please","please"]

#level
level = {"Key":1}

@route('/', method='GET')
def index():
    return template("chatbot.html")

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    bad_word(user_message)
    return json.dumps(checker(user_message))

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg') #user_message?
    return json.dumps({"animation": "inlove", "msg": user_message})

@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')

@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')

@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def bad_word(user_message):
    for bad_word in BAD_WORDS:
        if bad_word in user_message:
             return {"animation": "no", "msg": "Watch your language! I found the word '{}' in the text".format(bad_word)}

def check_input(user_message_words,word_list):
    for word in word_list:
        if word in user_message_words:
            return True

    return False

def checker (user_message):
    user_message_words = user_message.split(" ")

    if level["Key"] == 1:
        if check_input(user_message_words,GREETING_WORDS):
            level["Key"]+=1
            return {"animation": "excited", "msg": random.choice(BOT_GREETING_WORDS)}
        else:
            return {"animation": "confused", "msg": dont_understand(user_message)}
    if level["Key"] == 2:
        if check_input(user_message_words,KEYWORD_LIST):
            return {"animation": "laughing", "msg": "Great, how can I help with " + user_message + " ?" }
        elif check_input(user_message_words,WEATHER_LIST):
            return {"animation": "ok", "msg": weather(user_message)}
        elif check_input(user_message_words,SHOPPING_LIST):
            return {"animation": "money", "msg": shopping(user_message)}
        elif check_input(user_message_words,FOOD_LIST):
            return {"animation": "laughing", "msg": food(user_message)}
        elif check_input(user_message_words,TEL_AVIV_LIST):
            return {"animation": "dancing", "msg": tel_aviv(user_message)}
        elif check_input(user_message_words,MOVIES_LIST):
            return {"animation": "giggling", "msg": movies(user_message)}
        elif check_input(user_message_words,VACATION_LIST):
            return {"animation": "takeoff", "msg": vacation(user_message)}
        elif check_input(user_message_words,TIME_LIST):
            return {"animation": "heartbroke", "msg": time(user_message)}
        elif check_input(user_message_words, RESET_LIST):
            return {"animation": "afraid", "msg": reset(user_message)}
        else:
            return {"animation": "confused", "msg": dont_understand(user_message)}


#once have narrowed down specific keywords & topic, give user answer
def weather(user_message):
    return "It's summer - it is hot and humid with lots of sunshine"

def shopping(user_message):
    return "I'd recommend checking out Rothschild Blvd or Dizengoff Center - they should have everything you need"

def food(user_message):
    return "Miznon, Hakosem and Port Said are great restaurants. They're all reasonably priced too! " \
           "(btw make sure to order the techina at Port Said - you won't regret it!)"

def tel_aviv(user_message):
    return "There's lots to do in Tel Aviv - beach, restaurants, and bars are all great options if that's what you're into"

def movies(user_message):
    return "Lev Cinema near Dizengoff Center is a great theatre! Here's all the info you need: " + webbrowser.open("http://www.dizengof-center.co.il/en/")

def vacation(user_message):
    return "Greece and Cyprus are great summer vacation spots that should be relatively inexpensive from TLV"

def time(user_message):
    return "Check your watch or your smartphone buddy"

def reset(user_message):
    level["Key"] = 1
    return RESET_CHAT + ". " + random.choice(BOT_GREETING_WORDS)

def dont_understand(user_message):
    return DONT_UNDERSTAND_YOU + ". Please choose a topic (ex: " + random.choice(TOPIC_LIST) + ") " \
           " or let me know if you want to reset the conversation"

def main():
    run(host='localhost', port=8000)

if __name__ == '__main__':
    main()
