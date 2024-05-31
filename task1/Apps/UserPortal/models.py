from django.db import models
from django.core.validators import RegexValidator


class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100, validators=[
        RegexValidator(
            regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character.',
            code='invalid_password'
        )
    ])

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "User"
