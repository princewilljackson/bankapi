
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

import random
import uuid

def transaction_id():
    return str(uuid.uuid1())

TRANSACTION_TYPE = (
    ('Withdraw', 'Withdrawal'),
    ('Deposit', 'Deposit'),
)

SEX = (
    ('M', 'Male'),
    ('F', 'Female'),
)

STATUS = (
    ('Active', 'Active'),
    ('Dormant', 'Dormant'),
    ('Deactivated', 'Deactivated')
)
#manager for our custom model 

class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

def random_account():
       return str(random.randint(1000000000, 10000000000))

class User(AbstractBaseUser, PermissionsMixin):

    """Custom user class inheriting AbstractBaseUser class """
    
    passport = models.ImageField(upload_to='photos/%Y/%m/%d/')
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    sex = models.CharField(choices=SEX, max_length=1)
    phone = models.CharField(max_length=50)
    account_number = models.CharField(default=random_account, unique=True, max_length=200)
    available_bal = models.DecimalField(default=0, max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(choices=STATUS, default="Active", max_length=11, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email


class UpdateUser(models.Model):
    """Update user credentials"""
    dob = models.DateField()
    valid_ID_frontview = models.ImageField(upload_to='photos/%Y/%m/%d/')
    valid_ID_backview = models.ImageField(upload_to='photos/%Y/%m/%d/')
    next_of_kin = models.CharField(max_length=100)
    relationship_nok = models.CharField(max_length=50)
    phone_nok = models.CharField(max_length=50)
    date_updated = models.DateTimeField(auto_now_add=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "User Data"
  
    def __str__(self):
        return "{}".format(self.user_id)

class History(models.Model):
    """Users transactions history table"""

    bank_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, default='Deposit', max_length=11, null=True, blank=True)
    transaction_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, null=True, blank=True)
    transaction_description = models.CharField(max_length=100, null=True, blank=True)
    transaction_date = models.DateField()
    transaction_id = models.CharField(default=transaction_id, unique=True, max_length=200)
    user_id = models.ForeignKey(User, related_name='histories', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Transaction History'

    def __str__(self):
        return "{} of {} has been made, account name {}".format(self.transaction_type, self.transaction_amount, self.customer_name)

class PendingTransfer(models.Model):
    """User pending transactions table"""
    customer_name = models.CharField(max_length=100)
    transfer_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2, null=True, blank=True)
    transfer_date = models.DateField()
    user_id = models.ForeignKey(User, related_name='pendingtransfers', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Pending Transfers'

    def __str__(self):
        return "The sum of {} has been made to you by {}".format(self.transfer_amount, self.customer_name)