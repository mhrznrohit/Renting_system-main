from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
     path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout',views.logout_user,name='logout'),
    path('postad',views.postad,name='postad'),
    path('search_flat',views.search_flat,name='search-flat'),
    path('filter_flat', views.filter_flats, name='filter-flat'),

    path('flats/<slug:slugs>/<int:id>',views.adDetail,name="flats"),
    path('profile',views.profile,name='profile'),
]