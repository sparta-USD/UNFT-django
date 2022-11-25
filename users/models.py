from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, usd=None):
        if not username:
            raise ValueError('아이디 입력은 필수입니다!')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            usd=usd,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, usd=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            usd=usd,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length=254, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    usd = models.IntegerField(default=100000, blank=True, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'username'  # 로그인하고 싶은 필드
    REQUIRED_FIELDS = ['email','usd']  # 필수로 받고 싶은 필드
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin