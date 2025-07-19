from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Account, Transaction

def get_financial_data(user):
    """Get consistent financial data for a user"""
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Accounts
    accounts = Account.objects.filter(user=user)
    total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0
    
    # Monthly transactions
    monthly_transactions = Transaction.objects.filter(user=user, date__gte=current_month)
    monthly_spending = abs(monthly_transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0)
    monthly_income = monthly_transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # All-time transactions
    all_transactions = Transaction.objects.filter(user=user)
    all_inflow = all_transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
    all_outflow = abs(all_transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0)
    
    return {
        'accounts': accounts,
        'total_balance': float(total_balance),
        'monthly_spending': float(monthly_spending),
        'monthly_income': float(monthly_income),
        'all_inflow': float(all_inflow),
        'all_outflow': float(all_outflow),
        'monthly_transactions': monthly_transactions,
        'all_transactions': all_transactions,
        'current_month': current_month,
    }