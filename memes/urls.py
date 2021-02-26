from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.user_registration, name='user_registration'),
    path('login/', views.loginPage, name = 'user_login'),
    path('cookie/', views.cookie, name = 'cookie'),
    path('memes/', views.meme_view, name = 'memes'),
    # path('test1/',views.setcookies, name = 'test1'),
    path('logoutpage/', views.logout_view, name = 'logoutpage'),
]