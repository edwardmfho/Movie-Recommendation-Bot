import logging
import telegram
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, 
	InlineKeyboardMarkup, ParseMode, InlineKeyboardButton)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from google_trans_new import google_translator

from messages import *
from movie_tools import *
from utils import random_number
from configs import TOKEN

import os

PORT = int(os.environ.get('PORT', 5000))


logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level = logging.INFO)

logger = logging.getLogger(__name__)

translator = google_translator()

# Handler Dict
GENRE, DISPLAY = range(2)

# Get Genre List
genre_dict = get_genre()
genre_list = [result['name'] for result in genre_dict]
genre_list.append('cancel')


def start(update, context):
	update.message.reply_text(START_MESSAGE)
	return GENRE

def restart(update, context):
	return GENRE


# def random_movie(genre):
# 	movie_list = get_movie(genre)
# 	if len(movie_list) > 0:
# 		movie = '或者你想睇呢套戲？'
# 		movie += (movie_list[random_selector(movie_list)])
# 	else:
# 		movie = '我搵唔到你想睇嘅戲⋯⋯ 重新嚟過？ /start '
# 	return movie



def display_result(update, context):

	genre_code = None
	for genre in genre_dict:
		if genre['name'] == update.message.text:
			genre_code = genre['id']
			break

	response = get_movie(genre_code)

	movie_list = response['results']
	image_path = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'

	max_movie_num = len(response['results'])
	print(max_movie_num)

	if max_movie_num != 0:

		random_movie_id = random_number(0, max_movie_num)
		poster_path = image_path + response['results'][random_movie_id]['poster_path']
		title = response['results'][random_movie_id]["original_title"]

		overview = response['results'][random_movie_id]['overview']
		overview_zh = translator.translate(overview,lang_tgt='zh-tw') 
		# else:
		# 	overview = '未能提供' 

		print(poster_path)
		release_date = response['results'][random_movie_id]["release_date"]

		message = '或者你可以試下睇呢套《{}》 \n 上映日期： {} \n 故事簡介（英文）： {} \n 故事簡介（中文翻譯—試用）： {}'.format(title, release_date, overview, overview_zh)
		update.message.reply_text(message)
		context.bot.send_photo(chat_id = update.message.chat.id, photo = poster_path)
		update.message.reply_text('唔啱？禁 /discover 睇下一套。')
	else:
		update.message.reply_text('我搵唔到你想睇嘅戲⋯⋯ 重新嚟過？ /start ')
	

def discover(update, context):
	message = '你想睇咩題材型嘅戲呢？用以下既字，覆返你想睇嘅題材：\n \
			   Action \n \
			   Adventure\n \
			   Animation\n \
			   Comedy\n \
			   Crime\n \
			   Documentary \n \
			   Drama\n \
			   Family\n \
			   Fantasy\n \
			   History\n \
			   Horror\n \
			   Music\n \
			   Mystery\n \
			   Romance\n \
   			   Science Fiction\n \
			   TV Movie\n \
			   Thriller\n \
			   War\n \
			   Western\n \
			   '

	update.message.reply_text(text = message)

	return DISPLAY



def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('唔緊要，下次再見！ /restart',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END



def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():

	updater = Updater(TOKEN, use_context = True)

	dp = updater.dispatcher

	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)],
		allow_reentry=True,
		states={

			GENRE: [MessageHandler(Filters.text, discover)],

			DISPLAY: [MessageHandler(Filters.text, display_result)],

		},

		fallbacks=[CommandHandler('cancel', cancel)]
	)


	dp.add_handler(conv_handler)
    # log all errors
	dp.add_error_handler(error)

	updater.start_webhook(listen="0.0.0.0",
							port=int(PORT),
							url_path=TOKEN)
	updater.bot.setWebhook('https://mighty-tundra-13919.herokuapp.com/' + TOKEN)


	updater.idle()

if __name__ == "__main__":
	main()

