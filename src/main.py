import logging
import json

from re import findall
from os.path import isfile
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.ext import Filters 

API_TOKEN = "1050680359:AAGtmXnLlyPXNU_dtnXcyHiQzSylq_JZnb4"
USERNAMES_FILE = "usernames.json"

def start(update, context):
	context.bot.send_message(
		chat_id=update.message.chat_id,
		text="Ciao :) ")

def tag_people(match):
	message = ""
	for username in USERNAMES[match[1:]]:
		message += f"@{username} "
	return message

def tag_team(update, context):
	matches = findall(r"#Team\w+|#All",update.message.text)
	if matches:
		for match in matches:
			context.bot.send_message(
				chat_id=update.message.chat_id,
				text=tag_people(match))

if __name__ == "__main__":
	
	if not API_TOKEN: exit("Invalid token!")
	if not USERNAMES_FILE: exit("Missing JSON Filename!")
	if not isfile(USERNAMES_FILE): exit("Missing JSON File")
	
	with open(USERNAMES_FILE,'r') as f:
		USERNAMES = json.load(f)

	updater = Updater(token=API_TOKEN, use_context=True)
	dispatcher = updater.dispatcher
	logging.basicConfig(
		level=logging.DEBUG,
		format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	
	start_handler = CommandHandler("start",start)
	grafiche_handler = MessageHandler(Filters.regex(r"#Team|#All"),tag_team)

	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(grafiche_handler)

	updater.start_polling()
	updater.idle()
	updater.stop()