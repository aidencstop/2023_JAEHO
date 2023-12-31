from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, member_id, authority=None, name=None, age=None, gender=None, password=None, height=None):
        if not member_id:
            raise ValueError('Users must have an member_id.')

        user = self.model(
            member_id=member_id,
        )
        if authority:
            user.authority = authority
        if name:
            user.name = name
        if age:
            user.age = age
        if gender:
            user.gender = gender
        if height:
            user.height = height

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, member_id, password):
        user = self.create_user(
            member_id,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    member_id = models.CharField(
        verbose_name='member_id',
        max_length=80,
        unique=True,
        blank=False,
    )
    authority = models.IntegerField(
        default=0,
    )
    name = models.CharField(
        max_length=30,
        default='noname',
    )
    age = models.IntegerField(
        default=20,
    )
    gender = models.CharField(
        max_length=6,
        default='Male',
        choices=(('Male', 'Male'), ('Female', 'Female'))
    )
    height = models.IntegerField(
        default=170,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'member_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.member_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def setMemberId(self, member_id):
        self.member_id = member_id
        self.save()

    def setAuthority(self, authority):
        self.authority = authority
        self.save()
    def setName(self, name):
        self.name = name
        self.save()


    def setAge(self, age):
        self.age = age
        self.save()

    def setGender(self, gender):
        self.gender = gender
        self.save()

    def setHeight(self, height):
        self.height = height
        self.save()

    @property
    def is_staff(self):
        return self.is_admin
