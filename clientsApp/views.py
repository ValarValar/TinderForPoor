from django.shortcuts import render
# Подключаем статус
from rest_framework import status
# Подключаем компонент для ответа
from rest_framework.response import Response
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView

from rest_framework.decorators import api_view, permission_classes

# Подключаем компонент для прав доступа
from rest_framework.permissions import AllowAny
# Подключаем модель User
from .models import User
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, UserSerializer, UserLikedListSerializer

from rest_framework import generics, mixins, permissions

# Создаём класс RegistrUserView
class RegistrUserView(CreateAPIView):
    # Добавляем в queryset
    queryset = User.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = UserRegistrSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]

    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        # Добавляем UserRegistrSerializer
        serializer = UserRegistrSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            # Добавляем в список значение ответа True
            data['response'] = True
            # Возвращаем что всё в порядке
            return Response(data, status=status.HTTP_200_OK)
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)

class UserListView(ListAPIView):
    """
    API endpoint that represents a list of users.
    """

    serializer_class = UserSerializer
    paginate_by = 10
    permission_classes = [AllowAny]

    # Фильтрует queryset по значениям из get запросу
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = User.objects.all()
        keys = ['first_name',
                'last_name',
                'sex'
        ]
        filters = {}
        req = self.request
        for key in keys:
            filter = req.query_params.getlist(key)
            if filter:
                filters['{}__in'.format(key)] = filter

        return queryset.filter(**filters)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def UserMatchView(request, pk):
    if pk == request.user.id:
        data = {}
        data['1'] = "You shouldn't like usrself"
        return Response(data, status=status.HTTP_200_OK)
    user = User.objects.get(id=request.user.id)
    own_liked_list = user.get_liked_list()
    liked_user = User.objects.filter(id=pk)

    if liked_user:
        liked_user = User.objects.get(id=pk)
        if not (pk in own_liked_list):
            own_liked_list.append(pk)
            user.set_liked_list(own_liked_list)  #Добавили к текущему юзеру в список лайков
            user.save(update_fields=['liked_list'])

    data = {}
    if liked_user:
        liked_user_list = liked_user.get_liked_list()
        if user.id in liked_user_list:
            st = "It's a match! His or her email: "
            data['1'] = st + liked_user.email #Если мэтч, показываем в ответе почту
            return Response(data, status=status.HTTP_200_OK)
    else:
        data['1'] = "User not found"
    return Response(data, status=status.HTTP_200_OK)