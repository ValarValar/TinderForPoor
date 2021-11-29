from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .watermark import watermark
from geopy.distance import great_circle
import json

### Обертка для накладывания вотермарки. Принимает File, возвращает файл BytesIO
def watermarkImage(image_file):
    mark = 'images/watermark/200-star.png'
    return watermark(image_file, mark, 'scale', 0.45)


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    # Метод для создания пользователя
    def _create_user(self, email, password, **extra_fields):
        # Проверяем есть ли Email
        if not email:
            # Выводим сообщение в консоль
            raise ValueError("Вы не ввели Email")
        # Делаем пользователя
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем всё остальное
        user.save(using=self._db)
        # Возвращаем пользователя
        return user

    # Делаем метод для создание обычного пользователя
    def create_user(self, email, password):
        return self._create_user(email, password)

    # Делаем метод для создание админа сайта
    def create_superuser(self, email, password):
        return self._create_user(email, password, is_staff=True, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30,)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    liked_list = models.TextField(blank=True, default="[-1, -2]")
    longitude = models.DecimalField(default=0, decimal_places=3, max_digits=6)
    latitude = models.DecimalField(default=0, decimal_places=3, max_digits=6)

    def user_directory_path(instance, filename):
        # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>_<filename>
        return 'images/user_{0}_{1}'.format(instance, filename)
    avatar = models.ImageField(verbose_name="Avatar", null=True, blank=True, upload_to=user_directory_path)

    Male = 'M'
    Female = 'F'
    sex_Choices = (
        (Male, 'Male'),
        (Female, 'Female'),
    )
    sex = models.CharField(
        max_length=1,
        choices=sex_Choices,
        default=Female,
        help_text="Enter your gender",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()  # Добавляем методы класса MyUserManager

    # Метод для отображения в админ панели
    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):

        if self.avatar:
            print(self.avatar)
            #Сохраняем аватарку на лету с вотермаркой
            self.avatar = watermarkImage(self.avatar.file)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def set_liked_list(self, x):
        self.liked_list = json.dumps(x)

    def get_liked_list(self):
        return json.loads(self.liked_list)