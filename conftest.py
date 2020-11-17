from wishlist.models import Game, Category, Priority
import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def category():
    category = Category.objects.create(name="FPS")
    return category


@pytest.fixture
def category2():
    category = Category.objects.create(name="Action")
    return category


@pytest.fixture
def game(category):
    game = Game.objects.create(title="DOOM", year=2016, category=category)
    return game


@pytest.fixture
def games(category):
    Game.objects.create(title="DOOM", year=2016, category=category)
    Game.objects.create(title="Call of Duty: Black Ops", year=2010, category=category)
    Game.objects.create(title="Medal of Honor", year=1999, category=category)
    return Game.objects.all()


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def user():
    user = User.objects.create_user(username='grzegorz', password='1234')
    user.save()
    return user


@pytest.fixture
def users():
    User.objects.create_user(username='grzegorz', password='1234')
    User.objects.create_user(username='marta', password='1234')
    User.objects.create_user(username='filip', password='1234')
    return User.objects.all()


@pytest.fixture
def user_priority(game):
    user = User.objects.create_user(username='ggg', password='1234')
    user.save()
    priority = Priority.objects.create(wish=2, game_id=game.id, user_id=user.id)
    priority.save()
    return user


@pytest.fixture
def games_diff_categories(category, category2):
    Game.objects.create(title="DOOM", year=2016, category=category)
    Game.objects.create(title="Call of Duty: Black Ops", year=2010, category=category)
    Game.objects.create(title="Uncharted 4", year=2016, category=category2)
    return Game.objects.all()
