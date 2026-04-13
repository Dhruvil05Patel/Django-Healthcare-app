from django.urls import path
from django.views.generic import RedirectView
from .views import RegisterView, JWTLoginView, JWTRefreshView

urlpatterns = [
    path("", RedirectView.as_view(url="login/", permanent=False)),
    path("register/", RegisterView.as_view()),
    path("login/", JWTLoginView.as_view()),
    path("token/refresh/", JWTRefreshView.as_view()),
]