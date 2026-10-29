from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# create model for superadmin
class MyAccountManager(BaseUserManager):
    # creating normal user
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User Must have an email address')

        if not username:
            raise ValueError('user must have an username')

        user = self.model(
            # normalize_email means that if someone enter capital letter in email it will automatically normalize it
            email=self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    # creating superuser
    def create_superuser(self, first_name, last_name, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        # set all the permissions
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user

# create model for account
# creating account
class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=100, unique=True)
    phone_number=models.CharField(max_length=50)

    # required
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superadmin=models.BooleanField(default=False)

    # Here we want to login with email in our app
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username', 'first_name', 'last_name']

    # here we have to tell accounts that we are using myAccountManager for all the operations
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # it means that is user is admin then they have all the permission 
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
