from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.fields import URLField


class UserProfile(AbstractUser):
    bio = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='instagram_images/', null=True, blank=True)
    website = URLField()
    nike_name = models.CharField(max_length=16)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)],
                                           null=True, blank=True)
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Follow(models.Model):
    follower = models.ManyToManyField(UserProfile, related_name='follower')
    following = models.ManyToManyField(UserProfile, related_name='following')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower}, {self.following}'


class Hashtag(models.Model):
    hashtag = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.hashtag}'


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user')
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_video/', null=True, blank=True)
    description = models.TextField()
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE,  null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


    class Meta:
        unique_together = ('user', 'post',)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comment_user')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    like = models.ForeignKey(PostLike, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment',)


class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    story_image = models.ImageField(upload_to='story_images/')
    story_video = models.FileField(upload_to='story_video/')
    created_date = models.DateTimeField(auto_now_add=True)


class Save(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class SaveItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    save = models.ForeignKey(Save, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
