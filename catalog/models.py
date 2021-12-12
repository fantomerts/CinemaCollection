from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.mixins import LoginRequiredMixin
from django import template
import locale
import math

class Fact(models.Model):
    description = models.CharField(max_length=1000,help_text="Enter a fact")

    def __str__(self):
        return self.description

class Genre(models.Model):
    name = models.CharField(max_length=30,help_text="Enter a movie genre")

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=30,help_text="Enter a movie country")

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=30,help_text="Enter an actor's name")
    fact=models.ManyToManyField(Fact,help_text="Select a fact about this actor",blank=True)
    date_of_birth=models.DateField(help_text="Choose a date of birth of actor",null=True)
    date_of_death=models.DateField(help_text="Choose a date of death of actor",null=True,blank=True)
    photo=models.CharField(max_length=1000,help_text="Enter URL of a photo for actor",null=True,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor-detail', args=[str(self.id)])

    def get_birth_date(self):
        return self.date_of_birth.strftime("%d.%m.%Y")

    def get_death_date(self):
        return self.date_of_death.strftime("%d.%m.%Y")

class Director(models.Model):
    name = models.CharField(max_length=30,help_text="Enter a director's name")
    fact=models.ManyToManyField(Fact,help_text="Select a fact about this director",blank=True)
    date_of_birth=models.DateField(help_text="Choose a date of birth of director",null=True)
    date_of_death=models.DateField(help_text="Choose a date of death of director",null=True,blank=True)
    photo=models.CharField(max_length=1000,help_text="Enter URL of a photo for director",null=True,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('director-detail', args=[str(self.id)])

    def get_birth_date(self):
        return self.date_of_birth.strftime("%d.%m.%Y")

    def get_death_date(self):
        return self.date_of_death.strftime("%d.%m.%Y")

class Studio(models.Model):
    title = models.CharField(max_length=30,help_text="Enter a studio title")

    def __str__(self):
        return self.title

class Movie(models.Model,LoginRequiredMixin):
    title=models.CharField(max_length=200,help_text="Enter a movie title")
    timing=models.IntegerField(help_text="Enter a movie timing",null=True)
    summary=models.CharField(max_length=1000,help_text="Enter a brief description of the movie",null=True,blank=True)
    release=models.DateField(help_text="Choose a date of movie release",null=True)
    poster=models.CharField(max_length=1000,help_text="Enter URL of a movie poster",null=True,blank=True)
    video=models.CharField(max_length=10000,help_text="Enter URL of a movie video",null=True,blank=True)
    genre=models.ManyToManyField(Genre,help_text="Select a genre for this movie")
    country=models.ManyToManyField(Country,help_text="Select a country for this movie")
    actor=models.ManyToManyField(Actor,help_text="Select an actor for this movie")
    director=models.ManyToManyField(Director,help_text="Select a director for this movie")
    studio=models.ManyToManyField(Studio,help_text="Select a studio for this movie")
    fact=models.ManyToManyField(Fact,help_text="Select a fact about this movie",blank=True)
    kp=models.CharField(max_length=1000,help_text="Enter Id of a movie on Kinopoisk",null=True,blank=True)
    imdb=models.CharField(max_length=1000,help_text="Enter Id of a movie on IMDb",null=True,blank=True)

    def display_genre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'

    def display_director(self):
        return ', '.join([ director.name for director in self.director.all()[:3] ])
    display_director.short_description = 'Director'

    def display_actor(self):
        return ', '.join([ actor.name for actor in self.actor.all()[:3] ])
    display_actor.short_description = 'Actors'

    def display_studio(self):
        return ', '.join([ studio.title for studio in self.studio.all()[:3] ])
    display_studio.short_description = 'Studios'

    def display_fact(self):
        return ', '.join([ fact.description for fact in self.fact.all()[:3] ])
    display_fact.short_description = 'Facts'

    def display_country(self):
        return ', '.join([ country.name for country in self.country.all()[:3] ])
    display_country.short_description = 'Country'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie-detail', args=[str(self.id)])

    def get_middle_vote(self):
        sum = 0.0
        for vote in self.votedmovie_set.all():
            sum += vote.score
        if len(self.votedmovie_set.all()) != 0:
            sum/=len(self.votedmovie_set.all())
            if sum.is_integer():
                return int(sum)
            else:
                return round(sum,1)
        else:
            return '—'

    def get_count_votes(self):
        return len(self.votedmovie_set.all())

    def get_vote_color(self):
        if self.get_middle_vote() == '—':
            return 'gray'
        elif self.get_middle_vote() >= 7:
            return "green"
        elif self.get_middle_vote() < 5:
            return "red"
        else:
            return "yellow"

    def get_release_date(self):
        return self.release.strftime("%d.%m.%Y")

class VotedMovie(models.Model):
    movie=models.ForeignKey('Movie',on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    score=models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    date=models.DateTimeField(help_text="Select a date and time of adding",null=True)

    def __str__(self):
        return f"{self.user}: {self.movie}"

    class Meta:
        permissions = (("can_see_all", "See all votes"),)   

    def get_all(self):
        return VotedMovie.objects.order_by("date").reverse().all()

    def get_vote_color(self):
        if self.score >= 7:
            return "green"
        elif self.score < 5:
            return "red"
        else:
            return "yellow"

    def get_score_date(self):
        return self.date.strftime("%d.%m.%Y %H:%M")

    def __str__(self):
        return str(self.score)
        