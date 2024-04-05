from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager
from django.conf import settings
import uuid
from datetime import datetime
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin,models.Model):
    email = models.EmailField(max_length=100,unique=True,primary_key = True)
    user_name = models.CharField(max_length=100,unique=True)
    profileimg = models.ImageField(upload_to="profile_img",default="blank-profile-picture.png")
    password = models.CharField(max_length = 100)
    first_name = models.CharField(max_length=20,blank=True,null=True)
    last_name = models.CharField(max_length=20,blank=True,null=True)
    bio = models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=50,blank=True,null=True)
    occupation = models.CharField(max_length=20,blank=True,null=True)
    relationship = models.CharField(max_length=20)

    has_joined = models.DateField(default = datetime.now)  

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        # return str(self.userId)
        return self.email    
    class Meta(AbstractBaseUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        

class Post(models.Model):
    email = models.ForeignKey(CustomUser,on_delete=models.Case,related_name = "posted_by")
    postId = models.UUIDField(default=uuid.uuid4, editable=False)
    no_of_likes = 0
    caption = models.TextField()
    created_at  = models.DateTimeField(default = datetime.now)
    postImage = models.ImageField(upload_to="post_img")
    def __str__(self) -> str:
        return str(self.postId)
