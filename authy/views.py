from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from authy.models import Profile, PersonalList
from movie.models import Movie, Review, Likes

from comment.models import Comment
from comment.forms import CommentForm


from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm



from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
			return redirect('login')
	else:
		form = SignupForm()

	context = {
		'form': form,
	}

	return render(request, 'registration/signup.html', context)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change-password-done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form': form,
	}

	return render(request, 'registration/change_password.html', context)


def PasswordChangeDone(request):
	return render(request, 'registration/change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('index')
	else:
		form = EditProfileForm()

	context = {
		'form': form,
	}

	return render(request, 'edit_profile.html', context)


def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	#MovieBoxData
	mWatched_count = profile.watched.filter(Type='movie').count()
	sWatched_count = profile.watched.filter(Type='series').count()
	watch_list_count = profile.to_watch.all().count()
	m_reviewd_count = Review.objects.filter(user=user).count()
	personal_list_count = PersonalList.objects.filter(user=user).count()


	context = {
		'profile': profile,
		'mWatched_count': mWatched_count,
		'sWatched_count': sWatched_count,
		'watch_list_count': watch_list_count,
		'm_reviewd_count': m_reviewd_count,
		'personal_list_count': personal_list_count,
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(context, request))


# UserProfileMovieswatched,UserProfileSeriesWatched, UserProfileWatchList,  UserProfileMoviesReviewed, ReviewDetail, like, unlike functions are to be added below:
#=================================================================================================


def UserProfileMoviesWatched(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	#MovieBoxData
	mWatched_count = profile.watched.filter(Type='movie').count()
	sWatched_count = profile.watched.filter(Type='series').count()
	watch_list_count = profile.to_watch.all().count()
	m_reviewd_count = Review.objects.filter(user=user).count()

	#Movies List
	movies = profile.watched.filter(Type='movie')
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_data = paginator.get_page(page_number)


	context = {
		'profile': profile,
		'mWatched_count': mWatched_count,
		'sWatched_count': sWatched_count,
		'watch_list_count': watch_list_count,
		'm_reviewd_count': m_reviewd_count,
		'movie_data': movie_data,
		'list_title': 'Movies Watched',
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(context, request))

def UserProfileSeriesWatched(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	#MovieBoxData
	mWatched_count = profile.watched.filter(Type='movie').count()
	sWatched_count = profile.watched.filter(Type='series').count()
	watch_list_count = profile.to_watch.all().count()
	m_reviewd_count = Review.objects.filter(user=user).count()

	#Movies List
	movies = profile.watched.filter(Type='series')
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_data = paginator.get_page(page_number)


	context = {
		'profile': profile,
		'mWatched_count': mWatched_count,
		'sWatched_count': sWatched_count,
		'watch_list_count': watch_list_count,
		'm_reviewd_count': m_reviewd_count,
		'movie_data': movie_data,
		'list_title': 'Series Watched',
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(context, request))

def UserProfileWatchList(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)

	#MovieBoxData
	mWatched_count = profile.watched.filter(Type='movie').count()
	sWatched_count = profile.watched.filter(Type='series').count()
	watch_list_count = profile.to_watch.all().count()
	m_reviewd_count = Review.objects.filter(user=user).count()

	#Movies List
	movies = profile.to_watch.all()
	paginator = Paginator(movies, 9)
	page_number = request.GET.get('page')
	movie_data = paginator.get_page(page_number)


	context = {
		'profile': profile,
		'mWatched_count': mWatched_count,
		'sWatched_count': sWatched_count,
		'watch_list_count': watch_list_count,
		'm_reviewd_count': m_reviewd_count,
		'movie_data': movie_data,
		'list_title': 'Watch list',
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(context, request))

@login_required
def personal_lists(request, username):
	user = get_object_or_404(User, username=username)
	if request.user != user:
		return HttpResponseRedirect(reverse('user-profile', args=[request.user.username]))

	if request.method == 'POST':
		name = request.POST.get('name', '').strip()
		is_private = bool(request.POST.get('is_private'))
		if name:
			if PersonalList.objects.filter(user=user).count() >= 5:
				messages.error(request, 'You have reached the maximum of 5 personal lists.')
				return HttpResponseRedirect(reverse('personal-lists', args=[username]))
			PersonalList.objects.get_or_create(user=user, name=name, defaults={'is_private': is_private})
			messages.success(request, 'Personal list created.')
		return HttpResponseRedirect(reverse('personal-lists', args=[username]))

	lists = PersonalList.objects.filter(user=user)
	context = {
		'profile': user.profile,
		'lists': lists,
	}
	return render(request, 'personal_lists.html', context)


@login_required
def delete_personal_list(request, list_id):
	plist = get_object_or_404(PersonalList, id=list_id)
	if plist.user != request.user:
		return HttpResponseRedirect(reverse('personal-lists', args=[request.user.username]))
	plist.delete()
	messages.success(request, 'Personal list deleted.')
	return HttpResponseRedirect(reverse('personal-lists', args=[request.user.username]))


@login_required
def personal_list_detail(request, username, list_id):
	user = get_object_or_404(User, username=username)
	plist = get_object_or_404(PersonalList, id=list_id, user=user)
	if plist.is_private and request.user != user:
		messages.error(request, 'This list is private.')
		return HttpResponseRedirect(reverse('profile', args=[username]))
	movies = plist.movies.all()
	context = {
		'profile': user.profile,
		'plist': plist,
		'movies': movies,
	}
	return render(request, 'personal_list_detail.html', context)


@login_required
def add_to_personal_list(request, imdb_id):
	if not validate_imdb_id(imdb_id):
		return HttpResponseRedirect(reverse('index'))
	movie = get_object_or_404(Movie, imdbID=imdb_id)
	profile = request.user.profile
	if not profile.watched.filter(id=movie.id).exists():
		messages.error(request, 'You can only add movies you have marked as watched to personal lists.')
		return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))

	if request.method == 'POST':
		list_ids = request.POST.getlist('list_ids')
		added = 0
		for lid in list_ids:
			plist = PersonalList.objects.filter(id=lid, user=request.user).first()
			if plist:
				plist.movies.add(movie)
				added += 1
		if added:
			messages.success(request, 'Movie added to selected list(s).')
		return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))

	lists = PersonalList.objects.filter(user=request.user)
	context = {
		'movie': movie,
		'lists': lists,
	}
	return render(request, 'choose_personal_list.html', context)


@login_required
def remove_from_personal_list(request, list_id, imdb_id):
	plist = get_object_or_404(PersonalList, id=list_id, user=request.user)
	movie = get_object_or_404(Movie, imdbID=imdb_id)
	plist.movies.remove(movie)
	messages.success(request, 'Movie removed from the list.')
	return HttpResponseRedirect(reverse('personal-list-detail', args=[request.user.username, plist.id]))
