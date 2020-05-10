from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
AbstractBaseUser, BaseUserManager, PermissionsMixin
)

#from django.utils.translation import gettext_lazy as _
from fees.models import Fees
from django.db.models import Sum

class StudentManager(BaseUserManager):
    def create_user(self, code, username, password=None):
        if not code:
            raise ValueError("Users must have a code")
        if not username:
            raise ValueError("Users must have a name")
        user = self.model(
               code = code,
               username = username,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, code, username, password):
        user = self.create_user(
               code = code,
               password = password,
               username = username,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Student(AbstractBaseUser, PermissionsMixin):
    SCHOOL_CHOICES = (
        (None, ""),
        ('بنين', 'بنين'),
        ('بنات', 'بنات'),
    )

    GRADE_CHOICES = (
        (None, ""),
        ('KG1', 'KG1'),
        ('KG2', 'KG2'),
        ('الأول الابتدائي', 'الأول الابتدائي'),
        ('الثاني الابتدائي', 'الثاني الابتدائي'),
        ('الثالث الابتدائي', 'الثالث الابتدائي'),
        ('الرابع الابتدائي', 'الرابع الابتدائي'),
        ('الخامس الابتدائي', 'الخامس الابتدائي'),
        ('الخامس الابتدائي', 'الخامس الابتدائي'),
        ('الأول الإعدادي', 'الأول الإعدادي'),
        ( 'الثاني الإعدادي', 'الثاني الإعدادي'),
        ('الثالث الإعدادي', 'الثالث الإعدادي'),
        ( 'الأول الثانوي', 'الأول الثانوي'),
        ('الثاني الثانوي', 'الثاني الثانوي'),
        ('الثالث الثانوي', 'الثالث الثانوي'),
    )
    AREA_CHOICES = (
        (None, ""),
        ('التجمع الخام', 'التجمع الخامس'),
        ( 'مدينة نصر', 'مدينة نصر'),
        ('القاهرة الجديدة','القاهرة الجديدة'),
        ('مصر الجديدة', 'مصر الجديدة'),

    )
    BUS_CHOICES = (
        (None, ""),
        ('1001', '1001'),
        ('1002', '1002'),
        ('1003', '1003'),
        ('1004', '1004'),
        ('1005', '1005'),
    )

    code = models.CharField(max_length=7, unique=True)
    username = models.CharField(verbose_name='student name', max_length=36)
    school = models.CharField( max_length=4, choices=SCHOOL_CHOICES, blank=True)
    grade = models.CharField( max_length=16, choices=GRADE_CHOICES, blank=True)

    payment_1 = models.PositiveSmallIntegerField(default=0)
    payment_2 = models.PositiveSmallIntegerField(default=0)
    study_paid = models.PositiveSmallIntegerField( default=0)
    def study_status(self):
        return self.payment_1 + self.payment_2 - self.study_paid

    study_status

    bus_active = models.BooleanField( default=False)
    bus_fees = models.PositiveSmallIntegerField( default=0)
    bus_paid = models.PositiveSmallIntegerField(default=0)
    def bus_status(self):
        return self.bus_fees - self.bus_paid
    bus_status

    area = models.CharField( max_length=16, choices=AREA_CHOICES, blank=True)
    adress = models.CharField( max_length=32, blank=True)
    old_bus = models.CharField( max_length=4, choices=BUS_CHOICES, blank=True)
    message = models.CharField(max_length=260, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # last_login = models.DateTimeField( auto_now_add=True)
    is_admin  = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    objects = StudentManager()

    USERNAME_FIELD = 'code'
    REQUIRED_FIELDS = ['username',]


    def __str__(self):
        return self.username + " " + self.code
    # # def __str__(self):
    # #     return self.code
    #
    #
    def has_perm(self, perm, obj=None):
        return self.is_admin
        # return True

    def has_module_perms(self, app_label):
        return True

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #         "Does the user have permissions to view the app `app_label`?"
    #         # Simplest possible answer: Yes, always
    #         return True



# @property
# def is_staff(self):
#     "Is the user a member of staff?"
#     return self.is_staff
#
# @property
# def is_admin(self):
#     "Is the user a admin member?"
#     return self.is_admin
#
# @property
# def is_active(self):
#     "Is the user active?"
#     return self.is_active
