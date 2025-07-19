from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birthdate = models.DateField()
    city = models.CharField(max_length=100)
    email = models.EmailField()
    risk_score = models.IntegerField(default=0, help_text="Risk score from 0-100")
    
    def __str__(self):
        return self.name

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('CHECKING', 'Checking Account'),
        ('SAVINGS', 'Savings Account'),
        ('BUSINESS', 'Business Account'),
        ('CREDIT', 'Credit Card'),
    ]
    
    CURRENCIES = [
        ('TRY', 'Turkish Lira'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]
    
    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    bank_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    iban = models.CharField(max_length=34, unique=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='TRY')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_type}"

class Transaction(models.Model):
    CATEGORIES = [
        ('FOOD_DINING', 'Food & Dining'),
        ('SHOPPING', 'Shopping'),
        ('TRANSPORTATION', 'Transportation'),
        ('BILLS_UTILITIES', 'Bills & Utilities'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('SALARY', 'Salary'),
        ('TRANSFER', 'Transfer'),
        ('OTHER', 'Other'),
    ]
    
    CURRENCIES = [
        ('TRY', 'Turkish Lira'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]
    
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='TRY')
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.CharField(max_length=200)
    merchant = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.description} - {self.amount} {self.currency}"
