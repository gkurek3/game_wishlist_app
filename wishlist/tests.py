from django.contrib.auth.models import User
from wishlist.models import Game, Category, Comment, Rating, Priority
import pytest


@pytest.mark.django_db
def test_login(client):
    user = User.objects.create_user(username='grzegorz', password='1234')
    user.save()
    url = "/login/"
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, {'username': 'grzegorz', 'password': '1234'}, follow=True)
    assert response.status_code == 200
    url2 = f'/game_list/'
    response = client.get(url2)
    assert response.status_code == 200


@pytest.mark.django_db
def test_wrong_login(client):
    user = User.objects.create_user(username='grzegorz', password='1234')
    user.save()
    url = "/login/"
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, {'username': 'grzegorz', 'password': '12345'}, follow=True)
    assert response.status_code == 200
    url2 = f'/game_list/'
    response = client.get(url2, follow=True)
    assert response.status_code == 404


@pytest.mark.django_db
def test_logout_correct(client, user):
    client.login(user=user.username, password=user.password)
    url = "/login/"
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_wrong(client):
    url = "/logout/"
    response = client.get(url, follow=True)
    assert response.status_code == 404


@pytest.mark.django_db
def test_add_game_user(client, user):
    client.force_login(user=user)
    url = '/add_game/'
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_game_superuser(client, category):
    user = User.objects.create_superuser(username='grzegorz', password='1234')
    client.force_login(user=user)
    url = '/add_game/'
    response = client.get(url)
    assert response.status_code == 200
    assert Game.objects.count() == 0
    response = client.post(url, {'title': 'DOOM', 'year': 2016, 'category': category.id})
    assert response.status_code == 302
    assert Game.objects.count() == 1


@pytest.mark.django_db
def test_add_category_user(client, user):
    client.force_login(user=user)
    url = f'/add_category/'
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_category_superuser(client):
    user = User.objects.create_superuser(username='grzegorz', password='1234')
    user.save()
    client.force_login(user=user)
    url = '/add_category/'
    response = client.get(url)
    assert response.status_code == 200
    assert Category.objects.count() == 0
    response = client.post(url, {'name': 'Metroidvania'})
    assert response.status_code == 302
    assert Category.objects.count() == 1
    assert Category.objects.get(name="Metroidvania")


@pytest.mark.django_db
def test_game_details(client, game, category):
    user = User.objects.create_user(username='grzegorz', password='1234')
    user.save()
    client.force_login(user=user)
    url = f'/game/{game.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['game'].title == 'DOOM'
    assert response.context['game'].year == 2016
    assert response.context['game'].category == category


@pytest.mark.django_db
def test_game_list(client, games, user):
    client.force_login(user=user)
    url = f'/game_list/'
    response = client.get(url)
    assert response.status_code == 200
    assert Game.objects.count() == 3
    g1 = Game.objects.get(id=3)
    g2 = Game.objects.get(id=4)
    g3 = Game.objects.get(id=5)
    assert g1.title == "DOOM"
    assert g2.title == "Call of Duty: Black Ops"
    assert g3.title == "Medal of Honor"
    assert len(response.context['games']) == 3


@pytest.mark.django_db
def test_user_profile_empty(client, user):
    client.force_login(user=user)
    url = f'/user_profile/{user.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['games']) == 0


@pytest.mark.django_db
def test_user_profile_filled(client, user, user_priority):
    client.force_login(user=user)
    url = f'/user_profile/{user_priority.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['games']) == 1


@pytest.mark.django_db
def test_user_list(client, users):
    user = User.objects.create_user(username='ggg', password='1234')
    user.save()
    client.force_login(user=user)
    url = f'/user_list/'
    response = client.get(url)
    assert response.status_code == 200
    assert User.objects.count() == 4
    assert list(response.context['users']) == list(users)
    assert len(response.context['users']) == 4


@pytest.mark.django_db
def test_main_page(client):
    url = '/main/'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_change_password_correct(client, user):
    client.force_login(user=user)
    url = f"/change_password/{user.id}/"
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, {'password1': 'abc', 'password2': 'abc'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_change_password_wrong(client, user):
    client.force_login(user=user)
    url = f"/change_password/{user.id}/"
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, {'password1': 'abc', 'password2': 'abcd'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_game_details_not_logged(client, game):
    url = f'/game/{game.id}/'
    response = client.get(url, follow=True)
    assert response.status_code == 404


@pytest.mark.django_db
def test_game_list_not_logged(client):
    url = f'/game_list/'
    response = client.get(url, follow=True)
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_list_not_logged(client):
    url = f'/user_list/'
    response = client.get(url, follow=True)
    assert response.status_code == 404


@pytest.mark.django_db
def test_add_rate(client, game, user):
    client.force_login(user=user)
    url = f'/game/{game.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert Rating.objects.count() == 0
    response = client.post(url, {'game_id': game.id, 'user_id': user.id,
                                 'rate': 1.0}, follow=True)
    print(response.content)
    assert response.status_code == 200
    assert Rating.objects.count() == 1


@pytest.mark.django_db
def test_add_wish(client, game, user):
    client.force_login(user=user)
    url = f'/game/{game.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert Priority.objects.count() == 0
    response = client.post(url, {'game_id': game.id, 'user_id': user.id,
                                 'wish': "I want to play"}, follow=True)
    assert response.status_code == 200
    assert Priority.objects.count() == 1


@pytest.mark.django_db
def test_add_comment(client, game, user):
    client.force_login(user=user)
    url = f'/game/{game.id}/'
    response = client.get(url)
    assert response.status_code == 200
    assert Comment.objects.count() == 0
    response = client.post(url, {'game_id': game.id, 'user_id': user.id,
                                 'comment': "Interesting"}, follow=True)
    assert response.status_code == 200
    print(response.content)
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_game_cat_filter(client, games_diff_categories, user, category, category2):
    client.force_login(user=user)
    url = f'/game_list/'
    response = client.get(url)
    assert response.status_code == 200
    assert Game.objects.count() == 3
    response = client.get(url, {'category': category})
    assert Game.objects.count() == 3
    assert len(response.context['games']) == 2
    response = client.get(url, {'category': category2})
    assert len(response.context['games']) == 1
