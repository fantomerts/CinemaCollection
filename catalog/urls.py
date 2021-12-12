from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movies/$', views.MovieListView.as_view(), name='movies'),
    url(r'^movie/(?P<pk>\d+)$', views.MovieDetailView.as_view(), name='movie-detail'),
    url(r'^actors/$', views.ActorListView.as_view(), name='actors'),
    url(r'^actor/(?P<pk>\d+)$', views.ActorDetailView.as_view(), name='actor-detail'),
    url(r'^directors/$', views.DirectorListView.as_view(), name='directors'),
    url(r'^director/(?P<pk>\d+)$', views.DirectorDetailView.as_view(), name='director-detail'),
    url(r'^mymovies/$', views.VotedMoviesByUserListView.as_view(), name='my-voted'),
]