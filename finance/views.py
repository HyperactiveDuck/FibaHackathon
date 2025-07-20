from django.db import models
from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Account, Transaction
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
import csv

def dashboard(request):
    # Try to get the logged in user, otherwise use demo user
    if request.user.is_authenticated:
        user = request.user
    else:
        try:
            user = User.objects.filter(id=2).first()
            if not user:
                user = User.objects.first()
        except:
            user = None
    
    if user:
        # Get all accounts for this user
        accounts = Account.objects.filter(user=user)
        
        # Add up all account balances
        total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        
        # Find transactions from this month
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_transactions = Transaction.objects.filter(
            user=user,
            date__gte=current_month
        )
        
        # Calculate how much was spent this month (negative amounts are expenses)
        monthly_spending = monthly_transactions.filter(amount__lt=0).aggregate(
            Sum('amount')
        )['amount__sum'] or 0
        monthly_spending = abs(monthly_spending)
        
        # Calculate income this month (positive amounts)
        monthly_income = monthly_transactions.filter(amount__gt=0).aggregate(
            Sum('amount')
        )['amount__sum'] or 0
        savings_this_month = monthly_income - monthly_spending
        
        # Mock data for upcoming bills
        upcoming_bills = 340.00
        
        # Group spending by category
        category_spending = monthly_transactions.filter(amount__lt=0).values('category').annotate(
            total=Sum('amount')
        ).order_by('total')
        
        # Prepare data for spending chart
        spending_categories = []
        total_spending_amount = sum([abs(float(cat['total'])) for cat in category_spending])
        
        # Colors for each spending category
        category_colors = {
            'FOOD_DINING': '#ef4444',
            'SHOPPING': '#f59e0b',
            'TRANSPORTATION': '#3b82f6',
            'BILLS_UTILITIES': '#8b5cf6',
            'ENTERTAINMENT': '#22c55e',
            'SALARY': '#22c55e',
        }
        
        # Nice labels for categories
        category_labels = {
            'FOOD_DINING': 'Food & Dining',
            'SHOPPING': 'Shopping',
            'TRANSPORTATION': 'Transportation',
            'BILLS_UTILITIES': 'Bills & Utilities',
            'ENTERTAINMENT': 'Entertainment',
            'SALARY': 'Income',
        }
        
        # Build chart data
        for cat in category_spending:
            amount = abs(float(cat['total']))
            percentage = (amount / total_spending_amount * 100) if total_spending_amount > 0 else 0
            spending_categories.append({
                'label': category_labels.get(cat['category'], cat['category']),
                'value': amount,
                'percentage': round(percentage, 1),
                'color': category_colors.get(cat['category'], '#64748b')
            })
        
        # Prepare data for account distribution chart
        account_distribution = []
        total_balance_float = float(total_balance) if total_balance else 0
        colors = [
            '#ef4444','#6366f1' , '#14b8a6', '#eab308', '#22c55e',
            '#84cc16', '#10b981', '#f59e0b', '#06b6d4', '#0ea5e9',
            '#3b82f6', '#f97316', '#8b5cf6', '#a855f7', '#d946ef',
            '#ec4899', '#f43f5e'
        ]
        
        for index, account in enumerate(accounts):
            account_balance = float(account.balance)
            percentage = (account_balance / total_balance_float * 100) if total_balance_float > 0 else 0
            
            # Create account label
            label = f"{account.bank_name}"
            if hasattr(account, 'account_type') and account.account_type:
                label += f" ({account.account_type})"
            elif hasattr(account, 'account_number') and account.account_number:
                last_four = str(account.account_number)[-4:]
                label += f" ***{last_four}"
            
            account_distribution.append({
                'label': label,
                'value': account_balance,
                'percentage': round(percentage, 1),
                'color': colors[index % len(colors)]
            })
        
        # Get the 3 most recent transactions
        recent_transactions = Transaction.objects.filter(user=user).order_by('-date')[:3]
        
        user_name = user.first_name or user.username
        
        # Convert all decimal values to floats for the template
        context = {
            'user_name': user_name,
            'total_balance': float(total_balance) if total_balance else 0,
            'monthly_spending': float(monthly_spending) if monthly_spending else 0,
            'monthly_budget': 2800.00,
            'savings_this_month': float(savings_this_month) if savings_this_month else 0,
            'savings_goal': 400.00,
            'upcoming_bills': upcoming_bills,
            'spending_categories': json.dumps(spending_categories),
            'account_distribution': json.dumps(account_distribution),
            'recent_transactions': recent_transactions,
        }
    else:
        # Show demo data if no user found
        context = {
            'user_name': "Demo User",
            'total_balance': 18201.05,
            'monthly_spending': 2420.85,
            'monthly_budget': 2800.00,
            'savings_this_month': 829.15,
            'savings_goal': 400.00,
            'upcoming_bills': 340.00,
            'spending_categories': json.dumps([]),
            'account_distribution': json.dumps([]),
            'recent_transactions': [],
        }
    
    return render(request, 'finance/dashboard.html', context)

def accounts(request):
    # Try to get user, fallback to demo
    if request.user.is_authenticated:
        user = request.user
    else:
        try:
            user = User.objects.filter(id=2).first()
            if not user:
                user = User.objects.first()
        except:
            user = None
    
    if user:
        # Get all accounts for this user
        user_accounts = Account.objects.filter(user=user)
        
        # Calculate total across all accounts
        total_balance = user_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        
        # Get stats for each account
        accounts_data = []
        for account in user_accounts:
            # Get recent transactions for this account
            recent_transactions = Transaction.objects.filter(
                account=account
            ).order_by('-date')[:5]
            
            # Calculate this month's activity
            current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            monthly_transactions = Transaction.objects.filter(
                account=account,
                date__gte=current_month
            )
            
            monthly_inflow = monthly_transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
            monthly_outflow = abs(monthly_transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0)
            
            accounts_data.append({
                'account': account,
                'recent_transactions': recent_transactions,
                'monthly_inflow': monthly_inflow,
                'monthly_outflow': monthly_outflow,
                'transaction_count': monthly_transactions.count()
            })
        
        context = {
            'accounts_data': accounts_data,
            'total_balance': total_balance,
            'account_count': user_accounts.count(),
        }
    else:
        context = {
            'accounts_data': [],
            'total_balance': 0,
            'account_count': 0,
        }
    
    return render(request, 'finance/accounts.html', context)

def transactions(request):
    # Get user like before
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.filter(id=2).first()
        if not user:
            user = User.objects.first()
    
    if not user:
        return render(request, 'finance/transactions.html', {'transactions': []})
    
    # Start with all user transactions
    transactions = Transaction.objects.filter(user=user)
    
    # Filter by account if selected
    account_filter = request.GET.get('account')
    if account_filter:
        try:
            account_id = int(account_filter)
            transactions = transactions.filter(account__pk=account_id)
            print(f"Filtering by account PK: {account_id}")
            print(f"Transactions found: {transactions.count()}")
        except (ValueError, TypeError):
            print(f"Invalid account filter: {account_filter}")
            pass
    
    # Filter by date range
    date_range = request.GET.get('date_range', '30')
    now = timezone.now()
    
    if date_range == '7':
        start_date = now - timedelta(days=7)
        transactions = transactions.filter(date__gte=start_date)
    elif date_range == '30':
        start_date = now - timedelta(days=30)
        transactions = transactions.filter(date__gte=start_date)
    elif date_range == '90':
        start_date = now - timedelta(days=90)
        transactions = transactions.filter(date__gte=start_date)
    elif date_range == 'this_month':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        transactions = transactions.filter(date__gte=start_date)
    elif date_range == 'last_month':
        first_day_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        transactions = transactions.filter(
            date__gte=first_day_last_month,
            date__lt=first_day_this_month
        )
    
    # Filter by category if selected
    category_filter = request.GET.get('category')
    if category_filter:
        transactions = transactions.filter(category=category_filter)
    
    # Search in merchant, description, or transaction ID
    search_query = request.GET.get('search')
    if search_query:
        transactions = transactions.filter(
            models.Q(merchant__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(transaction_id__icontains=search_query)
        )
    
    # Export to CSV if requested
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Merchant', 'Category', 'Amount', 'Account', 'Transaction ID'])
        
        for transaction in transactions.order_by('-date'):
            writer.writerow([
                transaction.date.strftime('%Y-%m-%d %H:%M'),
                transaction.merchant or transaction.description,
                transaction.get_category_display(),
                str(transaction.amount),
                f"{transaction.account.bank_name}",
                transaction.transaction_id
            ])
        
        return response
    
    # Sort by newest first
    transactions = transactions.order_by('-date')
    
    # Calculate summary stats for filtered data
    total_inflow = transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
    total_outflow = transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0
    net_change = total_inflow + total_outflow
    transaction_count = transactions.count()
    
    # Get accounts for filter dropdown
    accounts = Account.objects.filter(user=user)
    
    # Debug: show available accounts
    print("Available accounts:")
    for acc in accounts:
        print(f"  PK: {acc.pk}, Bank: {acc.bank_name}")
    
    context = {
        'transactions': transactions,
        'accounts': accounts,
        'total_inflow': float(total_inflow),
        'total_outflow': float(abs(total_outflow)),
        'net_change': float(net_change),
        'transaction_count': transaction_count,
    }
    
    return render(request, 'finance/transactions.html', context)

def settings(request):
    return render(request, 'finance/settings.html')

def budgets(request):
    # Get user like other views
    if request.user.is_authenticated:
        user = request.user
    else:
        try:
            user = User.objects.filter(id=2).first()
            if not user:
                user = User.objects.first()
        except:
            user = None
    
    if user:
        # Get this month's spending transactions
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_transactions = Transaction.objects.filter(
            user=user,
            date__gte=current_month,
            amount__lt=0
        )
        
        # Set budget limits for each category
        budget_limits = {
            'FOOD_DINING': 800.00,
            'SHOPPING': 600.00,
            'TRANSPORTATION': 400.00,
            'BILLS_UTILITIES': 500.00,
            'ENTERTAINMENT': 200.00,
        }
        
        # Calculate how much was spent in each category
        category_spending = monthly_transactions.values('category').annotate(
            total=Sum('amount')
        )
        
        # Build budget data for each category
        budget_data = []
        total_budget = sum(budget_limits.values())
        total_spent = 0
        
        # Nice labels and icons for categories
        category_labels = {
            'FOOD_DINING': 'Food & Dining',
            'SHOPPING': 'Shopping',
            'TRANSPORTATION': 'Transportation',
            'BILLS_UTILITIES': 'Bills & Utilities',
            'ENTERTAINMENT': 'Entertainment',
        }
        
        category_icons = {
            'FOOD_DINING': '🍕',
            'SHOPPING': '🛒',
            'TRANSPORTATION': '🚇',
            'BILLS_UTILITIES': '⚡',
            'ENTERTAINMENT': '🎬',
        }
        
        for category, limit in budget_limits.items():
            # Find how much was spent in this category
            spent = 0
            for cat_data in category_spending:
                if cat_data['category'] == category:
                    spent = abs(float(cat_data['total']))
                    break
            
            total_spent += spent
            percentage_used = (spent / limit * 100) if limit > 0 else 0
            remaining = limit - spent
            
            # Determine status color based on usage
            if percentage_used >= 100:
                status = 'over'
                status_color = '#ef4444'
            elif percentage_used >= 80:
                status = 'warning'
                status_color = '#f59e0b'
            else:
                status = 'good'
                status_color = '#22c55e'
            
            budget_data.append({
                'category': category,
                'label': category_labels.get(category, category),
                'icon': category_icons.get(category, '💳'),
                'limit': limit,
                'spent': spent,
                'remaining': remaining,
                'percentage_used': round(percentage_used, 1),
                'status': status,
                'status_color': status_color,
            })
        
        # Sort by percentage used (worst first)
        budget_data.sort(key=lambda x: x['percentage_used'], reverse=True)
        
        # Get recent transactions for each category
        recent_by_category = {}
        for category in budget_limits.keys():
            recent_by_category[category] = Transaction.objects.filter(
                user=user,
                category=category,
                amount__lt=0,
                date__gte=current_month
            ).order_by('-date')[:3]
        
        # Calculate overall budget health
        overall_percentage = (total_spent / total_budget * 100) if total_budget > 0 else 0
        days_in_month = timezone.now().day
        days_total = 30
        expected_percentage = (days_in_month / days_total * 100)
        
        if overall_percentage <= expected_percentage:
            budget_health = 'on_track'
            health_message = 'You\'re on track with your spending this month!'
        elif overall_percentage <= expected_percentage + 10:
            budget_health = 'slightly_over'
            health_message = 'You\'re slightly ahead of your expected spending pace.'
        else:
            budget_health = 'over_budget'
            health_message = 'You\'re spending faster than expected this month.'
        
        context = {
            'budget_data': budget_data,
            'total_budget': total_budget,
            'total_spent': total_spent,
            'total_remaining': total_budget - total_spent,
            'overall_percentage': round(overall_percentage, 1),
            'budget_health': budget_health,
            'health_message': health_message,
            'recent_by_category': recent_by_category,
            'current_month_name': current_month.strftime('%B %Y'),
        }
    else:
        # No user data available
        context = {
            'budget_data': [],
            'total_budget': 0,
            'total_spent': 0,
            'total_remaining': 0,
            'overall_percentage': 0,
            'budget_health': 'no_data',
            'health_message': 'No budget data available',
            'recent_by_category': {},
            'current_month_name': timezone.now().strftime('%B %Y'),
        }
    
    return render(request, 'finance/budgets.html', context)

def analytics(request):
    # Get user like other views
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.filter(id=2).first()
        if not user:
            user = User.objects.first()
    
    if not user:
        return render(request, 'finance/analytics.html', {})
    
    # Get time period from filter
    period = request.GET.get('period', '12')
    now = timezone.now()
    
    # Calculate date range based on selected period
    if period == '3':
        start_date = now - timedelta(days=90)
        months_count = 3
    elif period == '6':
        start_date = now - timedelta(days=180)
        months_count = 6
    elif period == '12':
        start_date = now - timedelta(days=365)
        months_count = 12
    elif period == 'ytd':
        start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        months_count = now.month
    elif period == 'all':
        start_date = None
        # Calculate how many months of data we have
        first_transaction = Transaction.objects.filter(user=user).order_by('date').first()
        if first_transaction:
            months_diff = (now.year - first_transaction.date.year) * 12 + (now.month - first_transaction.date.month)
            months_count = max(1, months_diff)
        else:
            months_count = 12
    else:
        start_date = now - timedelta(days=365)
        months_count = 12
    
    # Filter transactions by date range
    transactions = Transaction.objects.filter(user=user)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    
    # Export report if requested
    if request.GET.get('export') == 'report':
        return export_analytics_report(request, transactions, period)
    
    # Compare current period vs previous period
    if period == 'ytd':
        # Compare this year vs same period last year
        current_period_start = start_date
        current_period_end = now
        
        prev_period_start = start_date.replace(year=start_date.year - 1)
        prev_period_end = now.replace(year=now.year - 1)
        
        prev_period_transactions = Transaction.objects.filter(
            user=user,
            date__gte=prev_period_start,
            date__lt=prev_period_end
        )
    elif period == 'all':
        # Compare first half vs second half of all data
        total_days = (now - start_date).days if start_date else 365
        mid_point = start_date + timedelta(days=total_days // 2) if start_date else now - timedelta(days=182)
        
        current_period_transactions = transactions.filter(date__gte=mid_point)
        prev_period_transactions = transactions.filter(date__lt=mid_point)
    else:
        # Compare with previous equal period
        current_period_start = start_date
        current_period_end = now
        
        period_length = current_period_end - current_period_start
        prev_period_start = current_period_start - period_length
        prev_period_end = current_period_start
        
        current_period_transactions = transactions.filter(date__gte=current_period_start)
        prev_period_transactions = Transaction.objects.filter(
            user=user,
            date__gte=prev_period_start,
            date__lt=prev_period_end
        )
    
    # Calculate spending for current and previous periods
    if period in ['all']:
        current_spending = current_period_transactions.filter(amount__lt=0).aggregate(
            total=Sum('amount'))['total'] or 0
        prev_spending = prev_period_transactions.filter(amount__lt=0).aggregate(
            total=Sum('amount'))['total'] or 0
    else:
        current_spending = transactions.filter(amount__lt=0).aggregate(
            total=Sum('amount'))['total'] or 0
        prev_spending = prev_period_transactions.filter(amount__lt=0).aggregate(
            total=Sum('amount'))['total'] or 0
    
    current_spending = abs(float(current_spending))
    prev_spending = abs(float(prev_spending))
    
    # Calculate percentage change in spending
    if prev_spending > 0:
        spending_change = ((current_spending - prev_spending) / prev_spending) * 100
    else:
        spending_change = 0 if current_spending == 0 else 100
    
    # Calculate average monthly spending
    total_spending = transactions.filter(amount__lt=0).aggregate(
        total=Sum('amount'))['total'] or 0
    avg_monthly_spending = abs(float(total_spending)) / months_count if months_count > 0 else 0
    
    # Total transactions in filtered period
    total_transactions = transactions.count()
    
    # Build monthly spending trends
    monthly_trends = []
    if period == 'all':
        # Get all months with data
        months_data = transactions.values(
            'date__year', 'date__month'
        ).annotate(
            total_spending=Sum('amount', filter=models.Q(amount__lt=0))
        ).order_by('date__year', 'date__month')
        
        for month_data in months_data:
            month_name = datetime(month_data['date__year'], month_data['date__month'], 1).strftime('%b %Y')
            spending = abs(float(month_data['total_spending'] or 0))
            monthly_trends.append({'month': month_name, 'spending': spending})
    else:
        # Generate months for the selected period
        current_date = start_date if start_date else now - timedelta(days=365)
        while current_date <= now:
            month_start = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = (month_start + timedelta(days=32)).replace(day=1)
            
            if next_month > now:
                next_month = now
            
            month_spending = transactions.filter(
                date__gte=month_start,
                date__lt=next_month,
                amount__lt=0
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            monthly_trends.append({
                'month': month_start.strftime('%b %Y') if period == 'ytd' or period == 'all' else month_start.strftime('%b'),
                'spending': abs(float(month_spending))
            })
            
            current_date = next_month
            if current_date >= now:
                break
    
    # Find top merchants by spending
    top_merchants = transactions.filter(amount__lt=0).values('merchant').annotate(
        total=Sum('amount'),
        count=Count('transaction_id')
    ).exclude(merchant__isnull=True).exclude(merchant='').order_by('total')[:10]
    
    # Convert to positive amounts and format
    for merchant in top_merchants:
        merchant['total'] = abs(float(merchant['total']))
        merchant['name'] = merchant['merchant']
    
    # Calculate spending by category
    category_trends = transactions.filter(amount__lt=0).values('category').annotate(
        total=Sum('amount'),
        count=Count('transaction_id'),
        avg_transaction=models.Avg('amount')
    ).order_by('total')
    
    # Nice labels for categories
    category_labels = {
        'FOOD_DINING': 'Food & Dining',
        'SHOPPING': 'Shopping', 
        'TRANSPORTATION': 'Transportation',
        'BILLS_UTILITIES': 'Bills & Utilities',
        'ENTERTAINMENT': 'Entertainment',
        'TRANSFER': 'Transfer',
        'OTHER': 'Other'
    }
    
    formatted_category_trends = []
    for cat in category_trends:
        formatted_category_trends.append({
            'label': category_labels.get(cat['category'], cat['category']),
            'total': abs(float(cat['total'])),
            'count': cat['count'],
            'avg_transaction': abs(float(cat['avg_transaction'] or 0))
        })
    
    # Get performance data for each account
    accounts = Account.objects.filter(user=user)
    account_performance = []
    
    for account in accounts:
        account_transactions = transactions.filter(account=account)
        inflow = account_transactions.filter(amount__gt=0).aggregate(
            total=Sum('amount'))['total'] or 0
        outflow = account_transactions.filter(amount__lt=0).aggregate(
            total=Sum('amount'))['total'] or 0
        
        account_performance.append({
            'name': f"{account.bank_name} {getattr(account, 'account_type', '')}",
            'balance': float(account.balance),
            'inflow': float(inflow),
            'outflow': abs(float(outflow)),
            'net_change': float(inflow + outflow),
            'transaction_count': account_transactions.count()
        })
    
    # Calculate additional metrics
    total_inflow = transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
    total_outflow = transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0
    net_change = float(total_inflow) + float(total_outflow)
    
    # Average transaction amount for the period
    avg_transaction_amount = transactions.aggregate(models.Avg('amount'))['amount__avg'] or 0
    
    # Create nice labels for periods
    period_labels = {
        '3': 'Last 3 Months',
        '6': 'Last 6 Months', 
        '12': 'Last 12 Months',
        'ytd': 'Year to Date',
        'all': 'All Time'
    }
    period_label = period_labels.get(period, 'Last 12 Months')
    
    context = {
        'current_spending': current_spending,
        'last_spending': prev_spending,
        'spending_change': spending_change,
        'avg_monthly_spending': avg_monthly_spending,
        'total_transactions': total_transactions,
        'total_inflow': float(total_inflow),
        'total_outflow': abs(float(total_outflow)),
        'net_change': net_change,
        'avg_transaction_amount': abs(float(avg_transaction_amount)),
        'period_label': period_label,
        'months_count': months_count,
        'monthly_trends': json.dumps(monthly_trends),
        'daily_spending': json.dumps([]),
        'top_merchants': top_merchants,
        'category_trends': formatted_category_trends,
        'account_performance': account_performance,
    }
    
    return render(request, 'finance/analytics.html', context)

def export_analytics_report(request, transactions, period):
    """Export analytics data to CSV file"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="analytics_report_{period}_months.csv"'
    
    writer = csv.writer(response)
    
    # Write report header
    writer.writerow(['Analytics Report'])
    writer.writerow(['Period', f'{period} months' if period.isdigit() else period])
    writer.writerow(['Generated', timezone.now().strftime('%Y-%m-%d %H:%M')])
    writer.writerow([])
    
    # Write all transactions
    writer.writerow(['Date', 'Merchant', 'Category', 'Amount', 'Account'])
    for transaction in transactions.order_by('-date'):
        writer.writerow([
            transaction.date.strftime('%Y-%m-%d %H:%M'),
            transaction.merchant or transaction.description,
            transaction.get_category_display() if hasattr(transaction, 'get_category_display') else transaction.category,
            str(transaction.amount),
            transaction.account.bank_name
        ])
    
    return response

def add_account(request):
    if request.method == 'POST':
        # Get user like other views
        if request.user.is_authenticated:
            user = request.user
        else:
            user = User.objects.filter(username='ahmet_yilmaz').first()
        
        if not user:
            return redirect('accounts')
        
        # Get form data
        bank_name = request.POST.get('bank_name')
        account_type = request.POST.get('account_type')
        account_number = request.POST.get('account_number')
        iban = request.POST.get('iban')
        balance = request.POST.get('balance')
        
        try:
            # Create the new account
            Account.objects.create(
                user=user,
                bank_name=bank_name,
                account_type=account_type,
                iban=iban or f"TR{account_number}",
                balance=balance or 0.00
            )
            return redirect('accounts')
        except Exception as e:
            # Something went wrong creating the account
            print(f"Error creating account: {e}")
            return redirect('accounts')
    
    # Not a POST request, just go back to accounts
    return redirect('accounts')

def delete_account(request):
    if request.method == 'POST':
        # Get user like other views
        if request.user.is_authenticated:
            user = request.user
        else:
            user = User.objects.filter(username='ahmet_yilmaz')
        
        if not user:
            return redirect('accounts')
        
        account_id = request.POST.get('account_id')
        
        try:
            # Find the account to delete
            account = Account.objects.get(pk=account_id, user=user)
            
            # Delete all transactions for this account first
            Transaction.objects.filter(account=account).delete()
            
            # Now delete the account
            account.delete()
            
        except Account.DoesNotExist:
            # Account not found or doesn't belong to user
            pass
        except Exception as e:
            # Some other error happened
            print(f"Error deleting account: {e}")
    
    return redirect('accounts')