# Подключаем статус
from rest_framework import status
# Подключаем компонент для ответа
from rest_framework.response import Response
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.decorators import api_view, permission_classes
# Подключаем компонент для прав доступа
from rest_framework.permissions import AllowAny
# Подключаем модель User
from .models import User
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, UserSerializer
from rest_framework import permissions
from geopy.distance import great_circle
from django.core.mail import send_mail
from django.conf import settings


def send_match_mails(user_list):
    for i in [0,1]:
        safe_i = (i + 1) % 2
        arg1 = user_list[safe_i].first_name
        arg2 = user_list[safe_i].email
        message = "Вы понравились {0}! Почта участника: {1}".format(arg1, arg2)
        recipient = []
        recipient.append(user_list[i].email)
        send_mail('Great news from Tinder for Poor App!',
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  recipient,
                  fail_silently=False,
        )

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
    serializer_class = UserSerializer
    paginate_by = 10
    permission_classes = [AllowAny]

    def filter_queryset1(self, request, queryset):
        alluser = queryset.exclude(id=self.request.user.id)
        exclude_e = alluser
        distparam = request.GET.get('distance')
        if distparam:
            for user in alluser:
                from_loc = (self.request.user.latitude, self.request.user.latitude)
                self_loc = (user.latitude, user.longitude)
                distance = great_circle(from_loc, self_loc).km
                if distance > float(distparam):
                    exclude_e = exclude_e.exclude(id=user.id)
        return exclude_e
    # Фильтрует queryset по значениям из get запросу
    def get_queryset(self):
        keys = ['first_name',
                'last_name',
                'sex',
        ]
        filters = {}
        req = self.request
        for key in keys:
            filter = req.query_params.getlist(key)
            if filter:
                filters['{}__in'.format(key)] = filter
        queryset = User.objects.all()
        if req.GET.get('distance') and req.user.is_authenticated:
            queryset = self.filter_queryset1(req, queryset)
        return queryset.filter(**filters)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def UserMatchView(request, pk):
    if pk == request.user.id:
        data = {}
        data['1'] = "You shouldn't like usrself"
        return Response(data, status=status.HTTP_200_OK)
    user = User.objects.get(id=request.user.id)
    own_liked_list = user.liked_list
    liked_user = User.objects.filter(id=pk)

    if liked_user:
        liked_user = User.objects.get(id=pk)
        if not (pk in own_liked_list):
            own_liked_list.append(pk)
            user.liked_list = own_liked_list  #Добавили к текущему юзеру в список лайков
            user.save(update_fields=['liked_list'])

    data = {}
    if liked_user:
        liked_user_list = liked_user.liked_list
        if user.id in liked_user_list:
            st = "It's a match! His or her email: "
            data['1'] = st + liked_user.email #Если мэтч, показываем в ответе почту
            send_match_mails([user, liked_user])
            return Response(data, status=status.HTTP_200_OK)
    else:
        data['1'] = "User not found"
    return Response(data, status=status.HTTP_200_OK)
