from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, CreateView
from django.db.models import Avg, Func
from django.urls import reverse_lazy

from wishlist.forms import LoginForm, RegisterForm, ChangePasswordForm
from wishlist.models import Game, Category, Priority, Comment, Rating


class MainView(View):

    def get(self, request):
        """
        Presents main view/menu of the website.

        :param: context - user, depending on whether user is logged, not logged or is superuser,
        some elements of menu are or are not displayed.

        :return: main page
        """
        user = request.user
        return render(request, 'base1.html', {'user': user})


class RegisterView(FormView):
    """
    Provides user with a form that creates an account to the website.
    After that, user can successfully login.
    """
    template_name = 'add_user_form.html'
    form_class = RegisterForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email']
                                        )
        group = Group.objects.get(name='Users')
        user.groups.add(group)
        return super(RegisterView, self).form_valid(form)


class LoginView(FormView):
    """
    Provides user with a form with fields 'username' and 'password'. If user has been created, he/she
    can successfully login and have access to certain views and functionalities of the website.

    Button Login is visible only for not logged users.
    """
    template_name = 'login1.html'
    form_class = LoginForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            return redirect(reverse_lazy('login'))
        return super(LoginView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        """
        Logs out currently logged user.
        Button 'Logout' is visible only for logged users.
        """
        logout(request)
        return render(request, 'logout.html')


class AddGame(PermissionRequiredMixin, CreateView):
    """
    Available for superuser only.
    Provides superuser with a form that creates object of a Game model.
    """
    model = Game
    fields = ['title', 'year', 'category']
    success_url = reverse_lazy('main')
    permission_required = 'wishlist.add_game'


class AddCategory(PermissionRequiredMixin, CreateView):
    """
    Available for superuser only.
    Provides superuser with a form that creates object of a Game model.
    """
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('main')
    permission_required = 'wishlist.add_category'


class UserView(LoginRequiredMixin, View):

    def get(self, request, id):
        """
        View presents table with list of games that user added to his account (if he did). Each game's title is
        a link to its details. There is also info about priority of how badly user wants to play the game
        and game's average rating.
        User can sort games by priority in a descending and ascending way.
        If user has more than 10 games, there is a pagination function

        :param request:
        :param id: id of a chosen User model object
        :return: context - 'user' - current user, 'games' - list of games user has chosen, 'average' - rates of games
        """
        user = User.objects.get(id=id)
        if request.GET.get('sort') == 'Priority descending':
            games = Priority.objects.filter(user_id=user.id).order_by('-wish')
        elif request.GET.get('sort') == 'Priority ascending':
            games = Priority.objects.filter(user_id=user.id).order_by('wish')
        else:
            games = Priority.objects.filter(user_id=user.id).order_by('-wish')
        rates = {}
        for game in games:
            if Rating.objects.filter(game_id=game.game_id).count() > 0:
                rate_sum = Rating.objects.filter(game_id=game.game_id).aggregate(Avg('rate'))
                game2 = Game.objects.get(id=game.game_id)
                rates[game2.title] = round(rate_sum['rate__avg'], 2)
            else:
                game2 = Game.objects.get(id=game.game_id)
                rates[game2.title] = 0.0
        paginator = Paginator(games, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'user_profile.html', {'profile_user': user, 'games': games, 'average': rates,
                                                     'page_obj': page_obj})

    def post(self, request, id):
        """
        For each game on a list, there is a "delete" button. If clicked, the game will be deleted
        from user's account.

        :param request:
        :param id: id of a chosen User model object
        :return:
        """
        user = User.objects.get(id=id)
        if request.POST.get('game_delete'):
            game_delete = Priority.objects.get(id=int(request.POST.get('game_delete')))
            game_delete.delete()
            return redirect(f'/user_profile/{user.id}/')


class ChangePasswordView(LoginRequiredMixin, FormView):
    """
    Provides user with a form that changes user's password. User must type 2 equal passwords to fill
    the form correctly.
    """
    template_name = 'change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        u = self.request.user
        u.set_password(form.cleaned_data['password1'])
        u.save()
        return super(ChangePasswordView, self).form_valid(form)


class GameList(LoginRequiredMixin, View):

    def get(self, request):
        """
        View presents table with all games added to website. Each game's title is a link to game's details.
        Additional info for each game: game's category, average rating.
        User can filter through games by selecting games' category.

        :param request:
        :return:
        """
        categories = Category.objects.all()
        if request.GET.get("category"):
            category_choice = request.GET.get("category")
            category = Category.objects.get(name=category_choice)
            games = Game.objects.filter(category_id=category.id).order_by('title')
        else:
            games = Game.objects.all().order_by('title')
        rates = {}
        for game in games:
            if Rating.objects.filter(game_id=game.id).count() > 0:
                rate_sum = Rating.objects.filter(game_id=game.id).aggregate(Avg('rate'))
                game2 = Game.objects.get(id=game.id)
                rates[game2.title] = round(rate_sum['rate__avg'], 2)
            else:
                game2 = Game.objects.get(id=game.id)
                rates[game2.title] = 0.0
        paginator = Paginator(games, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'game_list.html', {'games': games, 'categories': categories, 'average': rates,
                                                  'page_obj': page_obj})

    def post(self, request):
        """
        Only superuser can see and click the button that deletes game from list of games.

        :param request:
        :return:
        """
        if request.POST.get('game_delete'):
            game_id = request.POST.get('game_delete')
            game_to_delete = Game.objects.get(id=int(game_id))
            game_to_delete.delete()
            return redirect(reverse_lazy('game-list'))


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'


class GameDetails(LoginRequiredMixin, View):

    def get(self, request, id):
        """
        Displays info of a Game object such as: title, year and category. It also provides user with a form.
        Additionally, it can display average rating of a game (if it has been rated) and comments (if there are any)

        :param request:
        :param id: id of a current object of a Game model
        :return:
        """
        game = Game.objects.get(id=id)
        comments = Comment.objects.filter(game_id=id)
        no_of_rates = Rating.objects.filter(game_id=id).count()
        if no_of_rates > 0:
            average = Rating.objects.filter(game_id=id).aggregate(rating=Round(Avg('rate')))
        else:
            average = 0
        return render(request, 'game_details.html', {'game': game, 'comments': comments, 'average': average})


    def post(self, request, id):
        """
        Each game has a form, where user can rate a game, add a comment to a game or add a game to his account.
        :param request:
        :param id: id of a model Game object.
        :return:
        """
        opinion = request.POST.get("comment")
        rate = request.POST.get("rate")
        user = request.user
        game = Game.objects.get(id=id)
        wish = request.POST.get("wish")
        wish_text_to_id = {
            'Not interested': 0,
            'Maybe I\'ll play': 1,
            'I want to play': 2,
            'I must play!': 3,
        }
        wish_id = wish_text_to_id.get(wish)
        if opinion:
            Comment.objects.create(opinion=opinion, game_id=game.id, user_id=user.id)
        if rate:
            Rating.objects.update_or_create(user_id=user.id, game_id=game.id, defaults={'rate': float(rate)})
        if wish_id:
            Priority.objects.update_or_create(user=user, game=game, defaults={'wish': wish_id})
        return redirect(f'/game/{id}')


class UserList(LoginRequiredMixin, View):
    permission_required = 'wishlist.delete_user'

    def get(self, request):
        """
        Displays list of all users registered to the website. Each user's username is a link to user's account.

        :param request:
        :return:
        """
        users = User.objects.all()
        return render(request, 'user_list.html', {'users': users})
