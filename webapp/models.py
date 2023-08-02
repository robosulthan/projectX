from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class User(models.Model):
    ROLES = (
    ('Vendor', 'Vendor'),
    ('AreaMgr', 'AreaMgr'),
    ('Manager', 'Manager'),
    ('Admin','Admin'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    phone_number = models.IntegerField(blank=True)
    roles = models.CharField(max_length=50, choices = ROLES, null=True)
    date_joined = models.DateField(auto_now_add=True)