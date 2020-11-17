from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200, unique=True, null=False)
    year = models.IntegerField(default=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Priority")

    def __str__(self):
        return self.title


class Priority(models.Model):
    WISH = [
        (0, "Not interested"),
        (1, "Maybe I'll play"),
        (2, "I want to play"),
        (3, "I must play!")
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    wish = models.IntegerField(choices=WISH, default=0)


class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opinion = models.TextField()

    def __str__(self):
        return self.opinion


class Rating(models.Model):
    RATES = [
        (0.5, 0.5),
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0),
        (5.5, 5.5),
        (6.0, 6.0),
        (6.5, 6.5),
        (7.0, 7.0),
        (7.5, 7.5),
        (8.0, 8.0),
        (8.5, 8.5),
        (9.0, 9.0),
        (9.5, 9.5),
        (10.0, 10.0),
    ]
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATES, default=1)
