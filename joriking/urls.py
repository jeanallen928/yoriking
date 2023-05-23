from django.urls import path
from . import views

urlpatterns = [
    path('', views.JorikingView.as_view(), name='joriking'),
]