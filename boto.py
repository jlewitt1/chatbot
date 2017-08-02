"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
import webbrowser

# initial greeting keywords
GREETING_WORDS = ["hello", "hey", "hi", "yo", "sup", "whatsup", "hi there","sup dude","how's it going?","hey there",
                  "yoo","hi!","hello!","hey!","thanks!","thanks","shalom","good","ok","alright","arite","fine","ok thanks",
                  "not bad","solid","awesome!","awesome","i'm good","im good","just chilling","not great","been better",
                  "eh","sick","not too good", "not much", "beseder","hakol beseder", "sababa", "sababa achi","achla","chilling","good man","good bro",
                  "great","amazing","not so good","terrible","horrible","bad","awful","hey man","hey dude","nothing"]

BOT_GREETING_WORDS = ["how are you?", "ma koreh?", "how you doin?", "how can I help you today?", "wazzzup??",
                      "sup dawg","what's going on?","ma nishma achi?","my man! what's going on?","sup dog?",
                      "whats good?","whats new?","how we doin today?"]

#alert user if any of these words are used
BAD_WORDS = ['fuck', 'shit', 'bitch', 'asshole', 'douchebag', 'fag', 'dick','idiot','fucker','ass']

# narrow down keywords with a specific topic
TOPIC_LIST = ["weather, shopping","food","tel_aviv","movies","vacation","time"]
BOT_TOPIC_SUGGEST = "Could you please suggest a keyword that is more specific to our current topic?"

#if user does not input a relevant keyword/topic
DONT_UNDERSTAND_YOU = "Sorry, I don't understand you"
RESET_CHAT = "Let's chat about a new topic"

#keywords for each specific topic
WEATHER_LIST = ["temperature","weather","high","low","humidity","average","cloudy","clouds","rain","sun",
                "sunshine","snow","hail","hot","cold","mild"]
SHOPPING_LIST = ["wear","clothing","clothes","shopping","dress","jeans","buy","shorts","shoes","towels","bed","bathing suit","hat","pants","t-shirt",
                 "tshirt","socks","sandals","flip flops","buy","shop"]
MOVIES_LIST = ["movies","movie","action","comedy","thriller","scary","funny","kids","adult","long","superhero","series","popcorn","theatre","film",
               "famous","celebrity","television","cinema"]
FOOD_LIST = ["hungry","eat","restaurant","food","falafel","israeli","burgers","italian","indian","healthy","salad","breakfast","lunch","dinner","snack","shwarma",
             "pizza","bite","brunch","munch"]
TEL_AVIV_LIST = ["israel","tel_aviv","bike","biking","hiking","haifa","jerusalem","eilat","negev","north","golan","city","cities"]
VACATION_LIST = ["beach","hiking", "swimming","travel","vacation","greece","italy","cyprus","relax","family","boyfriend","girlfriend","where should I go",
                 "europe","asia","usa","united states","new york","visit","abroad"]
TIME_LIST = ["tired","sleep","time","hour","minute","sleep","hours","minutes","clock","watch", "day","date","night"]
RESET_LIST = ["reset", "yes","restart","sure","yea","definitely","yep","yup","please","ok", "new topic", "change","topic"]
HELP_LIST = ["help","Help","HELP"]

#set level to prevent conversation from going back to initial starting point
level = {"Key":0}
# double_q = '"'

@route('/', method='GET')
def index():
    return template("chatbot.html")

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    print user_message
    bad_word_indicator = bad_word(user_message)
    if (bad_word_indicator is False):
        return json.dumps(checker(user_message))
    else:
        return json.dumps(bad_word(user_message))

@route("/user", method='POST')
#save message as a variable

#do get request to see if there is something in browser

#timeout on js to see if there is a new message
#if there is a new message post it on the server

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
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

#if user uses curse word let him know
def bad_word(user_message):
    user_message_words = user_message.split(" ")
    for bad_word in BAD_WORDS:
        if bad_word in user_message_words:
            return {"animation": "no", "msg": "Wooah watch your language! {} is a pretty dirty word!".format(bad_word)}
    return False

#check if user input matches any keywords in given list
def check_input(user_message_words,word_list):
    for word in word_list:
        if word in user_message_words:
            return True
    return False

#function to set animation and message for each list
def chatbot_response(animation, message):
    return {"animation": animation,
            "msg": message}

#once have narrowed down specific keywords & topic, give user answer
def name(user_message):
    level["Key"] = 1
    return "Hi " + user_message + "! " + random.choice(BOT_GREETING_WORDS)+ "\n(FYI - if you feel like I'm not " \
                                  "helping, please enter HELP)"

def weather(user_message):
    level["Key"] = 1
    return "It's summer - it is hot and humid with lots of sunshine"

def shopping(user_message):
    level["Key"] = 1
    return "I'd recommend checking out Rothschild Blvd or Dizengoff Center - they should have everything you need"

def food(user_message):
    level["Key"] = 1
    return "Miznon, Hakosem and Port Said are great restaurants. " \
           "(btw make sure to order the techina at Port Said - it's unreal)"

def tel_aviv(user_message):
    level["Key"] = 1
    return "There's lots to do in Tel Aviv - beach, restaurants, and bars are all great options"

def movies(user_message):
    level["Key"] = 1
    return "Lev Cinema near Dizengoff Center is a great theatre! Here's all the info you need: " + webbrowser.open("http://www.dizengof-center.co.il/en/")

def vacation(user_message):
    level["Key"] = 1
    return "Greece and Cyprus are great summer vacation spots that should be relatively inexpensive from Tel Aviv"

def time(user_message):
    level["Key"] = 1
    return "Check your watch or your smartphone buddy"

def reset(user_message):
    level["Key"] = 1
    return RESET_CHAT + ". " + random.choice(BOT_GREETING_WORDS)

def dont_understand(user_message):
    level["Key"] = 1
    return DONT_UNDERSTAND_YOU + ". Please choose a topic (ex: " + random.choice(TOPIC_LIST) + ") " \
           " or let me know if you want to reset the conversation. "

def help(user_message):
    level["Key"] = 1
    return  webbrowser.open("http://www.google.com")

#return appropriate message based on topic user chooses
def checker (user_message):
    user_message_words = user_message.split(" ")

    if (level["Key"] == 0):
        return chatbot_response(animation="inlove",
                                message=name(user_message))

    elif check_input(user_message_words,GREETING_WORDS):
        level["Key"] = 1
        return chatbot_response(animation="excited",
                                message=random.choice(BOT_GREETING_WORDS))

    elif check_input(user_message_words,WEATHER_LIST):
        level["Key"] = 2
        return chatbot_response(animation="ok",
                                message=weather(user_message))

    elif check_input(user_message_words,SHOPPING_LIST):
        level["Key"] = 2
        return chatbot_response(animation="money",
                                message=shopping(user_message))

    elif check_input(user_message_words,FOOD_LIST):
        level["Key"] = 2
        return chatbot_response(animation="laughing",
                                message=food(user_message))

    elif check_input(user_message_words,TEL_AVIV_LIST):
        level["Key"] = 2
        return chatbot_response(animation="dancing",
                                message=tel_aviv(user_message))

    elif check_input(user_message_words,MOVIES_LIST):
        level["Key"] = 2
        return chatbot_response(animation="giggling",
                                message=movies(user_message))

    elif check_input(user_message_words,VACATION_LIST):
        level["Key"] = 2
        return chatbot_response(animation="takeoff",
                                message=vacation(user_message))

    elif check_input(user_message_words,TIME_LIST):
        level["Key"] = 2
        return chatbot_response(animation="heartbroke",
                                message=time(user_message))

    elif check_input(user_message_words,RESET_LIST):
        level["Key"] = 2
        return chatbot_response(animation="bored",
                                message=reset(user_message))

    elif check_input(user_message_words,HELP_LIST):
        level["Key"] = 2
        return chatbot_response(animation="afraid",
                                message=help(user_message))
    else:
        return chatbot_response(animation="confused",
                                message=dont_understand(user_message))

def main():
    run(host='192.168.0.70', port=8070)

if __name__ == '__main__':
    main()
