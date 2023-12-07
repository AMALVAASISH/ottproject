from django.contrib import admin
from .models import Post, genre, media_genre, Episode, Favorite, WatchHistory
# Register your models here.
admin.site.register(Post)
admin.site.register(genre)
admin.site.register(media_genre)
admin.site.register(Episode)
admin.site.register(Favorite)
admin.site.register(WatchHistory)