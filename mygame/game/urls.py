from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('onboarding_intro/', views.onboarding_intro, name='onboarding_intro'),
    path('onboarding_location/', views.onboarding_location, name='onboarding_location'),
    path('main/', views.main, name='main'),
    path("news/", views.news_list, name="news_list"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path('under_construction/', views.under_construction, name='under_construction'),
]