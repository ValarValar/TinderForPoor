from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RegistrUserView, UserListView, UserMatchView

urlpatterns = [
    path('create', RegistrUserView.as_view(), name='registr'),
    path('list', UserListView.as_view(), name='list'),
    path('<int:pk>/match/', UserMatchView, name = 'match'),
]


