from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RegistrUserView, UserList

urlpatterns = [

    path('create', RegistrUserView.as_view(), name='registr'),
    path('list', UserList.as_view(), name='list')
]


