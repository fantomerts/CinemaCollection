from django.contrib import admin
from .models import *

admin.site.register(Fact)
admin.site.register(Genre)
admin.site.register(Country)
#admin.site.register(Actor)
#admin.site.register(Director)
admin.site.register(Studio)
#admin.site.register(VotedMovie)
#admin.site.register(Movie)

class MovieAdmin(admin.ModelAdmin):
    list_display=('title','release','display_director', 'display_country','display_genre','timing','summary','display_actor','display_studio','display_fact')
    list_filter = ('director','genre')
    fields = ['title',('release','timing'),('country','genre'),('director','actor'),'studio','summary','fact','poster','video','kp','imdb']

admin.site.register(Movie, MovieAdmin)

class ActorAdmin(admin.ModelAdmin):
    list_display=('name','date_of_birth','date_of_death')
    fields = ['name', ('date_of_birth', 'date_of_death'),'fact','photo']

admin.site.register(Actor,ActorAdmin)

class DirectorAdmin(admin.ModelAdmin):
    list_display=('name','date_of_birth','date_of_death')
    fields = ['name', ('date_of_birth', 'date_of_death'),'fact','photo']

admin.site.register(Director,DirectorAdmin)

class VotedMovieAdmin(admin.ModelAdmin):
    list_display=('movie','user','score','date')

admin.site.register(VotedMovie,VotedMovieAdmin)