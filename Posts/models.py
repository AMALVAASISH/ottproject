from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class genre(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

class media_genre(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    description = models.TextField()
    Image = models.ImageField(upload_to='post/images')
    shortname = models.SlugField(max_length=255, unique=True)
    published_date = models.DateField(auto_now_add=True)
    cast = models.TextField()
    movie_genre = models.ForeignKey(genre,default=1,related_name='genre_category',on_delete=models.CASCADE)
    movie_media_genre = models.ForeignKey(media_genre,default=1, related_name='mediagenre_category', on_delete=models.CASCADE)
    video_url = models.CharField(blank=True,max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=2 )
    favorited_by = models.ManyToManyField(User, related_name='favorite_posts', blank=True)

    def __str__(self):
        return self.title
#
# ======================================================================

class Episode(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    post = models.ForeignKey(Post,related_name= 'episodeofpost', default=1, on_delete=models.CASCADE)
    video_url = models.CharField(max_length=255,blank=True)
    cast = models.TextField()
    published_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Post, on_delete=models.CASCADE)  # Replace ContentModel with your actual content model
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"


