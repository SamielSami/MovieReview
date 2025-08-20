from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Avg

from movie.models import Movie, Genre, Rating, Review
from actor.models import Actor
from authy.models import Profile
from django.contrib.auth.models import User


from movie.forms import RateForm

import requests


# Create your views here.
def index(request):
	query = request.GET.get('q')

	if query:
		url = 'http://www.omdbapi.com/?apikey=4eb57329&s=' + query
		response = requests.get(url)
		movie_data = response.json()

		context = {
			'query': query,
			'movie_data': movie_data,
			'page_number': 1,
		}

		template = loader.get_template('search_results.html')

		return HttpResponse(template.render(context, request))

	return render(request, 'index.html')


def pagination(request, query, page_number):
    url = 'http://www.omdbapi.com/?apikey=4eb57329&s=' + query + '&page=' + str(page_number)
    response = requests.get(url)
    movie_data = response.json()
    page_number = int(page_number) + 1

    context = {
        'query': query,
        'movie_data': movie_data,
        'page_number': page_number,
    }

    template = loader.get_template('search_results.html')

    return HttpResponse(template.render(context, request))



####   sadia Tasnim, write your movieDetails  part here



def genres(request, genre_slug):
	genre = get_object_or_404(Genre, slug=genre_slug)
	movies = Movie.objects.filter(Genre=genre)

	#Pagination
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_data = paginator.get_page(page_number)

	context = {
		'movie_data': movie_data,
		'genre': genre,
	}


	template = loader.get_template('genre.html')

	return HttpResponse(template.render(context, request))



####   sadia Tasnim, write your addMoviesToWatch, addMoviesWatched part here



def Rate(request, imdb_id):
	movie = Movie.objects.get(imdbID=imdb_id)
	user = request.user

	if request.method == 'POST':
		form = RateForm(request.POST)
		if form.is_valid():
			rate = form.save(commit=False)
			rate.user = user
			rate.movie = movie
			rate.save()
			return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))
	else:
		form = RateForm()

	template = loader.get_template('rate.html')

	context = {
		'form': form, 
		'movie': movie,
	}

	return HttpResponse(template.render(context, request))

