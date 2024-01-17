from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>/<int:operation>", views.profile, name="profile"),
    path("edit/<str:parameter>", views.edit, name="edit"),
    path("start_workout", views.start_workout, name="start_workout"),
    path("workout_saver",  views.workout_saver, name="workout_saver"),
    path("loader", views.loader, name="loader"),
]
