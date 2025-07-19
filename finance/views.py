from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Account, Transaction
from django.contrib.auth.models import User
import json

def dashboard(request):
    # For demo purposes, get the first user if not authenticated
    if request.user.is_authenticated:
        user = request.user
    else:
        try:
            user = User.objects.first()
            if not user:
                # Create a demo user if none exists
                user = User.objects.create_user(username='demo_user', password='demo')
        except:
            user = None
    
    if user:
        # Get user accounts
        accounts = Account.objects.filter(user=user)
        
        # Calculate total balance
        total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        
        # Get current month transactions
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_transactions = Transaction.objects.filter(
            user=user,
            date__gte=current_month
        )
        
        # Calculate monthly spending (negative amounts)
        monthly_spending = monthly_transactions.filter(amount__lt=0).aggregate(
            Sum('amount')
        )['amount__sum'] or 0
        monthly_spending = abs(monthly_spending)
        
        # Calculate savings this month (positive amounts)
        monthly_income = monthly_transactions.filter(amount__gt=0).aggregate(
            Sum('amount')
        )['amount__sum'] or 0
        savings_this_month = monthly_income - monthly_spending
        
        # Upcoming bills (mock data for now)
        upcoming_bills = 340.00
        
        # Spending by category
        category_spending = monthly_transactions.filter(amount__lt=0).values('category').annotate(
            total=Sum('amount')
        ).order_by('total')
        
        # Convert to chart data
        spending_categories = []
        total_spending_amount = sum([abs(float(cat['total'])) for cat in category_spending])
        
        category_colors = {
            'FOOD_DINING': '#ef4444',
            'SHOPPING': '#f59e0b',
            'TRANSPORTATION': '#3b82f6',
            'BILLS_UTILITIES': '#8b5cf6',
            'ENTERTAINMENT': '#22c55e',
            'SALARY': '#22c55e',
        }
        
        category_labels = {
            'FOOD_DINING': 'Food & Dining',
            'SHOPPING': 'Shopping',
            'TRANSPORTATION': 'Transportation',
            'BILLS_UTILITIES': 'Bills & Utilities',
            'ENTERTAINMENT': 'Entertainment',
            'SALARY': 'Income',
        }
        
        for cat in category_spending:
            amount = abs(float(cat['total']))  # Convert Decimal to float
            percentage = (amount / total_spending_amount * 100) if total_spending_amount > 0 else 0
            spending_categories.append({
                'label': category_labels.get(cat['category'], cat['category']),
                'value': amount,  # Now it's a float
                'percentage': round(percentage, 1),
                'color': category_colors.get(cat['category'], '#64748b')
            })
        
        # Account distribution
        account_distribution = []
        total_balance_float = float(total_balance) if total_balance else 0
        colors = [
            '#ef4444','#6366f1' , '#14b8a6', '#eab308', '#22c55e',
            '#84cc16', '#10b981', '#f59e0b', '#06b6d4', '#0ea5e9',
            '#3b82f6', '#f97316', '#8b5cf6', '#a855f7', '#d946ef',
            '#ec4899', '#f43f5e'
        ]
        
        for index, account in enumerate(accounts):
            account_balance = float(account.balance)  # Convert Decimal to float
            percentage = (account_balance / total_balance_float * 100) if total_balance_float > 0 else 0
            
            # Create unique label for each account
            label = f"{account.bank_name}"
            if hasattr(account, 'account_type') and account.account_type:
                label += f" ({account.account_type})"
            elif hasattr(account, 'account_number') and account.account_number:
                last_four = str(account.account_number)[-4:]
                label += f" ***{last_four}"
            
            account_distribution.append({
                'label': label,
                'value': account_balance,  # Now it's a float
                'percentage': round(percentage, 1),
                'color': colors[index % len(colors)]  # Ensure unique color per account
            })
        
        # Recent transactions
        recent_transactions = Transaction.objects.filter(user=user).order_by('-date')[:3]
        
        user_name = user.first_name or user.username
        
        # Convert all Decimal values to float for template
        context = {
            'user_name': user_name,
            'total_balance': float(total_balance) if total_balance else 0,
            'monthly_spending': float(monthly_spending) if monthly_spending else 0,
            'monthly_budget': 2800.00,
            'savings_this_month': float(savings_this_month) if savings_this_month else 0,
            'savings_goal': 400.00,
            'upcoming_bills': upcoming_bills,
            'spending_categories': json.dumps(spending_categories),  # Now JSON serializable
            'account_distribution': json.dumps(account_distribution),  # Now JSON serializable
            'recent_transactions': recent_transactions,
        }
    else:
        # Fallback data if no user
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
    # Get demo user if not authenticated
    if request.user.is_authenticated:
        user = request.user
    else:
        try:
            user = User.objects.first()
        except:
            user = None
    
    if user:
        # Get all user accounts
        user_accounts = Account.objects.filter(user=user)
        
        # Calculate total balance across all accounts
        total_balance = user_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        
        # Get account statistics
        accounts_data = []
        for account in user_accounts:
            # Get recent transactions for this account
            recent_transactions = Transaction.objects.filter(
                account=account
            ).order_by('-date')[:5]
            
            # Calculate monthly activity
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
    # Get demo user if not authenticated
    if request.user.is_authenticated:
        user = request.user
    else:
        try:
            user = User.objects.first()
        except:
            user = None
    
    if user:
        # Get ALL user transactions FIRST (before slicing)
        all_user_transactions = Transaction.objects.filter(user=user)
        
        # Calculate summary stats from ALL transactions
        total_inflow = all_user_transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
        total_outflow = abs(all_user_transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0)
        net_change = total_inflow - total_outflow
        
        # NOW slice for display (this goes LAST)
        user_transactions = all_user_transactions.order_by('-date')[:40]
        
        accounts = Account.objects.filter(user=user)
        
        context = {
            'transactions': user_transactions,
            'accounts': accounts,
            'total_inflow': total_inflow,
            'total_outflow': total_outflow,
            'net_change': net_change,
            'transaction_count': all_user_transactions.count(),
        }
    else:
        context = {
            'transactions': [],
            'accounts': [],
            'total_inflow': 0,
            'total_outflow': 0,
            'net_change': 0,
            'transaction_count': 0,
        }
    
    return render(request, 'finance/transactions.html', context)

def settings(request):
    return render(request, 'finance/settings.html')

def budgets(request):
    # Get demo user if not authenticated
    if request.user.is_authenticated:
        user = request.user
    else:
        try:
            user = User.objects.first()
        except:
            user = None
    
    if user:
        # Get current month transactions
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_transactions = Transaction.objects.filter(
            user=user,
            date__gte=current_month,
            amount__lt=0  # Only spending (negative amounts)
        )
        
        # Define budget limits (these could come from a Budget model later)
        budget_limits = {
            'FOOD_DINING': 800.00,
            'SHOPPING': 600.00,
            'TRANSPORTATION': 400.00,
            'BILLS_UTILITIES': 500.00,
            'ENTERTAINMENT': 200.00,
        }
        
        # Calculate spending by category
        category_spending = monthly_transactions.values('category').annotate(
            total=Sum('amount')
        )
        
        # Create budget data
        budget_data = []
        total_budget = sum(budget_limits.values())
        total_spent = 0
        
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
            # Find spending for this category
            spent = 0
            for cat_data in category_spending:
                if cat_data['category'] == category:
                    spent = abs(float(cat_data['total']))  # Convert Decimal to float
                    break
            
            total_spent += spent
            percentage_used = (spent / limit * 100) if limit > 0 else 0  # Now both are floats
            remaining = limit - spent
            
            # Determine status
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
                'spent': spent,  # Already converted to float
                'remaining': remaining,
                'percentage_used': round(percentage_used, 1),
                'status': status,
                'status_color': status_color,
            })
        
        # Sort by percentage used (highest first)
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
        days_total = 30  # Approximate
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
            'total_budget': total_budget,  # This is the limit (₺2,500)
            'total_spent': total_spent,    # This should be ₺2,397
            'total_remaining': total_budget - total_spent,
            'overall_percentage': round(overall_percentage, 1),
            'budget_health': budget_health,
            'health_message': health_message,
            'recent_by_category': recent_by_category,
            'current_month_name': current_month.strftime('%B %Y'),
        }
    else:
        # Fallback data
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
    # Get demo user if not authenticated
    if request.user.is_authenticated:
        user = request.user
    else:
        try:
            user = User.objects.first()
        except:
            user = None
    
    if user:
        # Get date ranges
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month = (current_month - timedelta(days=1)).replace(day=1)
        six_months_ago = current_month - timedelta(days=180)
        
        # Get transactions for analysis
        current_month_transactions = Transaction.objects.filter(
            user=user,
            date__gte=current_month
        )
        
        last_month_transactions = Transaction.objects.filter(
            user=user,
            date__gte=last_month,
            date__lt=current_month
        )
        
        # Monthly spending comparison
        current_spending = abs(current_month_transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0)
        last_spending = abs(last_month_transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0)
        
        spending_change = ((current_spending - last_spending) / last_spending * 100) if last_spending > 0 else 0
        
        # Get 6-month spending trend
        monthly_trends = []
        for i in range(6):
            month_start = current_month - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            
            month_spending = abs(Transaction.objects.filter(
                user=user,
                date__gte=month_start,
                date__lt=month_end,
                amount__lt=0
            ).aggregate(Sum('amount'))['amount__sum'] or 0)
            
            monthly_trends.append({
                'month': month_start.strftime('%b'),
                'spending': float(month_spending)
            })
        
        monthly_trends.reverse()  # Show oldest to newest
        
        # Top merchants by spending - FIXED: Use transaction_id instead of id
        top_merchants = Transaction.objects.filter(
            user=user,
            date__gte=six_months_ago,
            amount__lt=0
        ).values('merchant').annotate(
            total=Sum('amount'),
            count=Count('transaction_id')  # Changed from Count('id')
        ).order_by('total')[:5]
        
        # Format top merchants
        top_merchants_data = []
        for merchant in top_merchants:
            if merchant['merchant']:
                top_merchants_data.append({
                    'name': merchant['merchant'],
                    'total': abs(merchant['total']),
                    'count': merchant['count']
                })
        
        # Category analysis - FIXED: Use transaction_id instead of id
        category_analysis = Transaction.objects.filter(
            user=user,
            date__gte=six_months_ago,
            amount__lt=0
        ).values('category').annotate(
            total=Sum('amount'),
            count=Count('transaction_id')  # Changed from Count('id')
        ).order_by('total')
        
        category_labels = {
            'FOOD_DINING': 'Food & Dining',
            'SHOPPING': 'Shopping',
            'TRANSPORTATION': 'Transportation',
            'BILLS_UTILITIES': 'Bills & Utilities',
            'ENTERTAINMENT': 'Entertainment',
        }
        
        category_trends = []
        for cat in category_analysis:
            if cat['category']:
                category_trends.append({
                    'category': cat['category'],
                    'label': category_labels.get(cat['category'], cat['category']),
                    'total': abs(cat['total']),
                    'count': cat['count'],
                    'avg_transaction': abs(cat['total']) / cat['count'] if cat['count'] > 0 else 0
                })
        
        # Daily spending pattern (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_spending = []
        for i in range(30):
            day = thirty_days_ago + timedelta(days=i)
            day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            day_total = abs(Transaction.objects.filter(
                user=user,
                date__gte=day_start,
                date__lt=day_end,
                amount__lt=0
            ).aggregate(Sum('amount'))['amount__sum'] or 0)
            
            daily_spending.append({
                'date': day.strftime('%m/%d'),
                'spending': float(day_total)
            })
        
        # Account performance
        accounts = Account.objects.filter(user=user)
        account_performance = []
        for account in accounts:
            account_transactions = Transaction.objects.filter(
                account=account,
                date__gte=current_month
            )
            
            inflow = account_transactions.filter(amount__gt=0).aggregate(Sum('amount'))['amount__sum'] or 0
            outflow = abs(account_transactions.filter(amount__lt=0).aggregate(Sum('amount'))['amount__sum'] or 0)
            
            account_performance.append({
                'name': f"{account.bank_name} {account.get_account_type_display()}",
                'balance': float(account.balance),
                'inflow': float(inflow),
                'outflow': float(outflow),
                'net_change': float(inflow - outflow)
            })
        
        context = {
            'current_spending': current_spending,
            'last_spending': last_spending,
            'spending_change': round(spending_change, 1),
            'monthly_trends': json.dumps(monthly_trends),
            'daily_spending': json.dumps(daily_spending),
            'top_merchants': top_merchants_data,
            'category_trends': category_trends,
            'account_performance': account_performance,
            'total_transactions': Transaction.objects.filter(user=user, date__gte=six_months_ago).count(),
            'avg_monthly_spending': sum([trend['spending'] for trend in monthly_trends]) / len(monthly_trends) if monthly_trends else 0,
        }
    else:
        # Fallback data
        context = {
            'current_spending': 0,
            'last_spending': 0,
            'spending_change': 0,
            'monthly_trends': json.dumps([]),
            'daily_spending': json.dumps([]),
            'top_merchants': [],
            'category_trends': [],
            'account_performance': [],
            'total_transactions': 0,
            'avg_monthly_spending': 0,
        }
    
    return render(request, 'finance/analytics.html', context)