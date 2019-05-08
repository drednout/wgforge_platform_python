# -*- coding: utf8 -*-
"""Telegram test bot

Available commands:
    /ping - always return pong
    /start - start conversation
    /help - print list of available commands + some other info
    /dump - dump incoming message as JSON
    /who - return info about bot
    /joke - return random joke
"""
import telebot
import shlex
import subprocess
import random

# load jokes database
jokes = open("jokes.txt").readlines()

# init bot
bot = telebot.TeleBot('884583232:AAE6oowux9KEA7l-R9tql1UdG4jNhth2mvI')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    from_user = 'anonymous'
    if message.from_user:
        from_user = message.from_user.first_name

    bot.reply_to(message, 'Hi {}, how are you doing?'.format(from_user))


@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, 'pong')

@bot.message_handler(commands=['dump'])
def dump(message):
    bot.reply_to(message, str(message.json))

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, __doc__)

@bot.message_handler(commands=['who'])
def who(message):
    bot.reply_to(message, bot.get_me())

def get_random_joke():
    joke_count = len(jokes)
    joke_num = random.randint(0, joke_count - 1)
    return jokes[joke_num].replace('\\n', '\n')

@bot.message_handler(commands=['joke'])
def who(message):
    bot.reply_to(message, get_random_joke())


@bot.message_handler(regexp=".*joke.*")
def handle_message(message):
    bot.reply_to(message, get_random_joke())


#@bot.message_handler(commands=['exec'])
#def execute_command(message):
#    args = shlex.split(message.text)
#
#    # remove Telegram command name (/exec)
#    args.pop(0)
#    print("INFO: args are {}".format(args))
#    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    (stdout_data, stderr_data) = p.communicate()
#    bot.reply_to(message, 'stdout:\n{}\nstderr:\n{}\n'.format(stdout_data, stderr_data))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    bot.polling()
