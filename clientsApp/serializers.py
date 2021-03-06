# Подключаем класс для работы со сериалайзер
from rest_framework import serializers
# Подключаем модель user
from .models import User




def validate_passwords_similar(pass1, pass2, message='passwords are not equal! '):
    if pass1 != pass2:
        # Если нет, то выводим ошибку
        raise serializers.ValidationError(message)

def validate_letters(check_str, message='Str can contain only letters!'):
    if not (check_str.isalpha()):
        raise serializers.ValidationError(message)


#Создаём класс UserRegistrSerializer
class UserRegistrSerializer(serializers.ModelSerializer):
    # Поле для повторения пароля
    password2 = serializers.CharField()


    # Настройка полей
    class Meta:
        # Поля модели которые будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = ['email', 'first_name', 'last_name', 'sex', 'password', 'password2', 'avatar']
    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(email=self.validated_data['email'])
        user.sex = self.validated_data['sex']
        # Проверяем что поля имени содержат только буквы
        validate_letters(self.validated_data['first_name'],
                         'Name should contain only english letters')
        validate_letters(self.validated_data['first_name'],
                         'Name should contain only english letters')
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
        user.avatar = self.validated_data['avatar']

        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        validate_passwords_similar(password, password2)
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()

        # Возвращаем нового пользователя
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Поля модели которые будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = ['id', 'first_name', 'last_name', 'sex', 'avatar', 'liked_list']

