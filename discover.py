from movie_tools import *
from utils import random_selector


genre_list = get_genre()
genre_list.append('cancel')

GENRE, DISPLAY, CONFIRMATION = range(3)


# Return random movie from results
def random_movie(genre):
	try:
		movie_list = get_movie(genre, year)
		movie = movie_list[random_selector(movie_list)]
	except:
		movie = '我搵唔到你想睇嘅戲⋯⋯'
	return movie

def display_result(update, context, movie):
	update.message.reply_text('或者你想睇呢套戲？　<br> {}'.format(movie))
	return CONFIRMATION


def choose_genre(update, context):
	reply_keyboard = [genre_list]
	markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
	update.message.reply_text('你想睇咩題材型嘅戲呢？（喜劇、鬼片、懸疑⋯⋯）', reply_markup = markup)

	return DISPLAY

def confirmation(update, context):
    user_data = context.user_data
    user = update.message.from_user
    update.message.reply_text("Thank you! I will post the information on the channel @" + chat_id + "  now.", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! Hope to see you again next time.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

#	https://www.codementor.io/@karandeepbatra/part-1-how-to-create-a-telegram-bot-in-python-in-under-10-minutes-19yfdv4wrq