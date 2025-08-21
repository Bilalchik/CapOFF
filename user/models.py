from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from user.constants.models import NULLABLE


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):

        user = self.create_user(
            username=username,
            email=email
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=223)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, **NULLABLE)
    avatar = models.ImageField(upload_to='media/user_avatars', **NULLABLE)
    address = models.CharField(max_length=300, **NULLABLE)

    is_admin = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin
