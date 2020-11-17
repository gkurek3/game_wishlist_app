"""game_wishlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from wishlist.views import MainView, LoginView, LogoutView, AddGame, AddCategory, UserView, GameList, GameDetails, \
    UserList, RegisterView, ChangePasswordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', MainView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_game/', AddGame.as_view(), name='add-game'),
    path('add_category/', AddCategory.as_view(), name='add-category'),
    path('user_profile/<int:id>/', UserView.as_view(), name='user-profile'),
    path('game_list/', GameList.as_view(), name='game-list'),
    path('game/<int:id>/', GameDetails.as_view(), name='game-details'),
    path('user_list/', UserList.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change_password/<int:id>/', ChangePasswordView.as_view(), name='change-password'),
]
