import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

from blogIT.apps.core.models import TimestampedModel

class UserManager(BaseUserManager):
    """
    Django needs a Manager class for users, so we inherit from
    `BaseUserManager`, which is a built in Manager class.

    we must override the `create_user` function as per the documentation requirements
    """

    def create_user(self, username, email, password=None):
        """Create and returns a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
      """
      Create and return a `User` with admin level auth. If you know django, you know
      exactly what Superusers are. if not please take the time to review how to create
      a super user in cmd. python manage.py createsuperuser
      """
      if password is None:
          raise TypeError('Superusers must have a password.')

      user = self.create_user(username, email, password)
      user.is_superuser = True
      user.is_staff = True
      user.save()

      return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    #index this column in the
    # database to be able to lookup easily.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    #use the email for logging in because it is
    # the most common form of login credential, i.e facebook, gmail
    #my next goal, learn how to do Oauth social logins
    email = models.EmailField(db_index=True, unique=True)
    '''
    data is $$, we can't just let users delete their account, the data we collect is
    needed to analyze for future plans. So we just let them deactivate their account instead.
     '''
    # i know you do this FACEBOOOK, CODING HAS TAUGHT ME YOUR WAYS!
    is_active = models.BooleanField(default=True)

    # self-explantory, the BooleanField lets us know who is authorized to be admin and who
    # is a regular user
    is_staff = models.BooleanField(default=False)


    #The following fields are required by Django when you make a custom user model
    # The `USERNAME_FIELD` property tells us which field you would use to log in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that our UserManager manages
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        The @property on top of this def allows us to do user.token instead of
        user.generate_jwt_token()
        """
        return self._generate_jwt_token()

    def get_full_name(self):
      """
      This method is required by Django for things like handling emails.
      this app does not care for user's full name.
      """
      return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        same thing, I dont need their first name, rather just return their username
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)
        #if i pass in dt error occurs so i just wrote it out below and it worked

        token = jwt.encode({
            'id': self.pk,
            'exp': datetime.now() + timedelta(days=60)
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
