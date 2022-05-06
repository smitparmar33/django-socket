from django.db import models

# Create your models here.
class UserStatus(models.Model):
    name=models.CharField(max_length=20)
    status=models.BooleanField(default=True)
