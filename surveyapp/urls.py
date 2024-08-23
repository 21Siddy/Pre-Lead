from django.urls import path
from surveyapp import views
urlpatterns = [
    path('', views.loginview, name="login"),
    path('survey/', views.surveyview, name="survey"),
    path('logout/', views.logoutview, name="logout"),
    path('suggestion/', views.get_latest_suggestion, name="suggestion"),
    path('ratings/', views.post_suggestion_ratings, name="ratings"),
]