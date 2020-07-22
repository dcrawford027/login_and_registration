from django.db import models
from django.core.validators import validate_email
import bcrypt
from datetime import *
from dateutil.relativedelta import *
import re

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "You must enter a first name at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "You must enter a last name at least 2 characters long."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "The email you entered is not valid."
        usedEmail = User.objects.filter(email=postData['email'])
        if usedEmail:
            errors['email'] = "That email is already registered."
        if datetime.strptime(postData['birthdate'], '%Y-%m-%d') >= datetime.now():
            errors['birthdate'] = "Your birthdate must be in the past."
        userBirthday = datetime.strptime(postData['birthdate'], '%Y-%m-%d')
        if relativedelta(datetime.now(), userBirthday).years < 13:
            errors['birthdate'] = "You must be older than 13 years of age."
        if len(postData['pw']) < 8:
            errors['pw'] = "Your password must be 8 characters or more."
        if postData['confirm_pw'] != postData['pw']:
            errors['match'] = "Your passwords do not match."
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['pw']) < 8:
            errors['pw'] = "Your password is incorrect."
        validUser = User.objects.filter(email=postData['email'])
        if not validUser:
            errors['email'] = "Could not find that email."
        else:
            user = User.objects.get(email=postData['email'])
            if not bcrypt.checkpw(postData['pw'].encode(), user.password.encode()):
                errors['pw'] = "Your password is incorrect"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    birthdate = models.DateField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()