from django.db import models

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPES = (
        ('user', 'Regular User'),
        ('admin', 'Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)  # Make sure this field exists
    type = models.CharField(max_length=10, choices=USER_TYPES, default='user')
    bio = models.TextField(blank=True, null=True)  # Add the bio field
    birth_date = models.DateField(null=True, blank=True)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



from django.db import models

class LoginTable(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)  # Store hashed password
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.username
