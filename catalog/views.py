from django.shortcuts import render
from .models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
import pytz


def index(request):
    movies_count=Movie.objects.all().count()
    directors_count=Director.objects.all().count()
    actors_count=Actor.objects.all().count()

    visits_count=request.session.get('visits_count', 0)
    request.session['visits_count'] = visits_count+1

    return render(
        request,
        'index.html',
        context={'movies_count':movies_count,'directors_count':directors_count,'actors_count':actors_count,'visits_count':visits_count},
    )

class MovieListView(generic.ListView):
    model = Movie
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        movie_list = self.model.objects.all()
        if query:
            movie_list = movie_list.filter(title__icontains=query)
        return movie_list

class MovieDetailView(generic.DetailView):
    model = Movie

    def get_queryset(self):
        query = self.request.GET.get('vote')
        if query:
            print(query)
            movie=query.split('vote')[0]
            user=query.split('vote')[1]
            vote=query.split('vote')[2]
            objects = VotedMovie.objects.filter(movie=movie,user=user)
            if len(objects) > 0:
                objects.update(score=vote,date=timezone.localtime(timezone.now()))
            else:
                new_vote = VotedMovie(movie=Movie.objects.get(id=movie),user=User.objects.get(id=user),score=vote,date=timezone.localtime(timezone.now()))
                new_vote.save()
        movie = self.model.objects.all()
        return movie
        #убрать или исправить (выбор оценки)
        
class ActorListView(generic.ListView):
    model = Actor
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        actor_list = self.model.objects.all()
        if query:
            actor_list = actor_list.filter(name__icontains=query)
        return actor_list

class ActorDetailView(generic.DetailView):
    model = Actor

class DirectorListView(generic.ListView):
    model = Director
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        director_list = self.model.objects.all()
        if query:
            director_list = director_list.filter(name__icontains=query)
        return director_list

class DirectorDetailView(generic.DetailView):
    model = Director
    paginate_by = 10

class VotedMoviesByUserListView(LoginRequiredMixin,generic.ListView):
    model = VotedMovie
    template_name ='catalog/votedmovie_list_user.html'

    def get_queryset(self):
        return VotedMovie.objects.filter(user=self.request.user).order_by("date").reverse()