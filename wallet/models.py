from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_unique_code():
    length = 6
    
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Account.objects.filter(account_number=code).exists():
            return code

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.AutoField(primary_key=True)
    account_number = models.CharField(max_length=10, unique=True, default=generate_unique_code)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
