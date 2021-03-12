import requests
from configs import TMDB_API_KEY
from utils import random_number



def get_movie(genre):
	url = 'https://api.themoviedb.org/3/discover/movie'
	page_num = random_number(1, 500)
	query = {
		'api_key' : TMDB_API_KEY,
		# 'year' : year,
		'page' : page_num,
		'with_genres' : genre,
		'vote_average.gte' : 0.8,
	}
	print(page_num)
	response = requests.get(url, params = query).json()
	# movie_name = [result['original_title'] for result in response['results']]

	# keys = range(len(movie_name))

	# movies = {}
	# for i in keys:
	# 	movies[i]  = movie_name[i]

	# return movies, response
	return response

def get_genre():

	url = 'https://api.themoviedb.org/3/genre/movie/list'
	query = {
		'api_key' : TMDB_API_KEY
	}

	response = requests.get(url, params = query).json()
	genre_list = response['genres']
	
	return genre_list