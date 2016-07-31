# coding=utf-8

import telebot
import re
import reg_exp
import token

bot = telebot.TeleBot(token.token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Good day. I am CodeSegBot. At your service.")

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.send_message(message.chat.id,
		u'输入.r <roll expression>来投骰。例如，\n\
		.r 1d6+5d6k3\n\
		.r 1+2-3*4/5\n\
		(目前仅支持整数运算，不支持小数)')

nat = '([1-9][0-9]*)'
dice = '(' + nat + 'd' + nat + '(k' + nat + ')?)'
term = '(' + nat + '|' + dice + ')'
exp = '(' + term + '([+|\-]' + term +')*)'
RE = '((\.r)(\s)*'+exp+')$'

@bot.message_handler(regexp=RE)
def calculate_dice(message):
	line = re.search(RE, message.text).group()
	print line
	result = reg_exp.parse_command(line)
	print result
	bot.send_message(message.chat.id, result)

def pull_bot():
	bot.polling()

pull_bot()

