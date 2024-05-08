from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager): 
    def create_superuser(self, email, username, password=None):

        return self.create_user(username, email, password)
      

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Please provide an email address")
   

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    objects = create_user, create_superuser

class User(AbstractBaseUser):
    
    email           = models.EmailField(('email address'), unique = True)
    username        = models.CharField(max_length=50, unique=True)
    is_active       = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

class Todo(models.Model):
    userId = models.IntegerField()
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)