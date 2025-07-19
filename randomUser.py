import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal
import calendar

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from finance.models import UserProfile, Account, Transaction
from django.utils import timezone

def generate_demo_data():
    print("Generating demo data...")
    
    # Create demo users
    users_data = [
        {
            'username': 'ahmet_yilmaz',
            'first_name': 'Ahmet',
            'last_name': 'Yılmaz',
            'email': 'ahmet@example.com',
            'profile': {
                'name': 'Ahmet Yılmaz',
                'birthdate': '1990-05-15',
                'city': 'Istanbul',
                'email': 'ahmet@example.com',
                'risk_score': random.randint(20, 80)
            }
        },
        {
            'username': 'zeynep_demir',
            'first_name': 'Zeynep',
            'last_name': 'Demir',
            'email': 'zeynep@example.com',
            'profile': {
                'name': 'Zeynep Demir',
                'birthdate': '1985-12-03',
                'city': 'Ankara',
                'email': 'zeynep@example.com',
                'risk_score': random.randint(20, 80)
            }
        },
        {
            'username': 'demo_user',
            'first_name': 'Demo',
            'last_name': 'User',
            'email': 'demo@example.com',
            'profile': {
                'name': 'Demo User',
                'birthdate': '1995-08-20',
                'city': 'Izmir',
                'email': 'demo@example.com',
                'risk_score': random.randint(20, 80)
            }
        }
    ]
    
    # Create users and profiles
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'password': 'pbkdf2_sha256$600000$demo$hash'  # Demo password
            }
        )
        
        if created or not hasattr(user, 'userprofile'):
            profile_data = user_data['profile']
            UserProfile.objects.create(
                user=user,
                name=profile_data['name'],
                birthdate=datetime.strptime(profile_data['birthdate'], '%Y-%m-%d').date(),
                city=profile_data['city'],
                email=profile_data['email'],
                risk_score=profile_data['risk_score']
            )
        
        users.append(user)
        print(f"Created user: {user.username}")
    
    # Turkish banks
    banks = [
        'Garanti BBVA', 'İş Bankası', 'Akbank', 'Yapı Kredi', 'Ziraat Bankası',
        'Halkbank', 'VakıfBank', 'QNB Finansbank', 'DenizBank', 'TEB',
        'İNG Bank', 'Şekerbank', 'HSBC', 'Citibank', 'Anadolubank'
    ]
    
    # Create accounts for each user
    accounts = []
    for user in users:
        num_accounts = random.randint(2, 5)
        user_banks = random.sample(banks, num_accounts)
        
        for i, bank in enumerate(user_banks):
            account_types = ['CHECKING', 'SAVINGS', 'BUSINESS', 'CREDIT']
            account_type = random.choice(account_types)
            
            # Generate realistic balance based on account type
            if account_type == 'SAVINGS':
                balance = round(random.uniform(5000, 50000), 2)
            elif account_type == 'BUSINESS':
                balance = round(random.uniform(10000, 100000), 2)
            elif account_type == 'CREDIT':
                balance = round(random.uniform(-5000, 10000), 2)
            else:  # CHECKING
                balance = round(random.uniform(500, 25000), 2)
            
            # Generate unique IBAN
            iban = f"TR{random.randint(10, 99)}{random.randint(1000, 9999)}{random.randint(1000000000000000, 9999999999999999)}"
            
            account = Account.objects.create(
                user=user,
                bank_name=bank,
                account_type=account_type,
                iban=iban,
                currency='TRY',
                balance=Decimal(str(balance))
            )
            accounts.append(account)
            print(f"Created account: {bank} - {account_type} for {user.username}")
    
    # Generate transactions
    generate_transactions_for_accounts(accounts)
    
    print(f"\nDemo data generation complete!")
    print(f"Created {len(users)} users")
    print(f"Created {len(accounts)} accounts")
    print(f"Generated transactions for all accounts")

def generate_transactions_for_accounts(accounts):
    # Turkish merchants and transaction data
    transaction_templates = [
        # Food & Dining
        {'merchant': 'McDonald\'s', 'category': 'FOOD_DINING', 'amount_range': (-15, -50)},
        {'merchant': 'Starbucks', 'category': 'FOOD_DINING', 'amount_range': (-8, -25)},
        {'merchant': 'Pizza Hut', 'category': 'FOOD_DINING', 'amount_range': (-25, -60)},
        {'merchant': 'KFC', 'category': 'FOOD_DINING', 'amount_range': (-20, -45)},
        {'merchant': 'Burger King', 'category': 'FOOD_DINING', 'amount_range': (-15, -40)},
        {'merchant': 'Migros Market', 'category': 'FOOD_DINING', 'amount_range': (-50, -200)},
        {'merchant': 'CarrefourSA', 'category': 'FOOD_DINING', 'amount_range': (-30, -180)},
        {'merchant': 'Şok Market', 'category': 'FOOD_DINING', 'amount_range': (-20, -100)},
        {'merchant': 'A101', 'category': 'FOOD_DINING', 'amount_range': (-15, -80)},
        {'merchant': 'BİM', 'category': 'FOOD_DINING', 'amount_range': (-25, -120)},
        
        # Shopping
        {'merchant': 'LC Waikiki', 'category': 'SHOPPING', 'amount_range': (-30, -200)},
        {'merchant': 'H&M', 'category': 'SHOPPING', 'amount_range': (-40, -300)},
        {'merchant': 'Zara', 'category': 'SHOPPING', 'amount_range': (-80, -500)},
        {'merchant': 'MediaMarkt', 'category': 'SHOPPING', 'amount_range': (-200, -3000)},
        {'merchant': 'Teknosa', 'category': 'SHOPPING', 'amount_range': (-150, -2500)},
        {'merchant': 'Boyner', 'category': 'SHOPPING', 'amount_range': (-60, -400)},
        {'merchant': 'DeFacto', 'category': 'SHOPPING', 'amount_range': (-40, -250)},
        {'merchant': 'Koton', 'category': 'SHOPPING', 'amount_range': (-35, -180)},
        {'merchant': 'Mavi', 'category': 'SHOPPING', 'amount_range': (-50, -300)},
        
        # Transportation
        {'merchant': 'Shell', 'category': 'TRANSPORTATION', 'amount_range': (-80, -400)},
        {'merchant': 'Petrol Ofisi', 'category': 'TRANSPORTATION', 'amount_range': (-90, -450)},
        {'merchant': 'BP', 'category': 'TRANSPORTATION', 'amount_range': (-85, -420)},
        {'merchant': 'İETT', 'category': 'TRANSPORTATION', 'amount_range': (-5, -15)},
        {'merchant': 'Metro İstanbul', 'category': 'TRANSPORTATION', 'amount_range': (-4, -12)},
        {'merchant': 'BiTaksi', 'category': 'TRANSPORTATION', 'amount_range': (-15, -80)},
        {'merchant': 'Uber', 'category': 'TRANSPORTATION', 'amount_range': (-20, -100)},
        
        # Bills & Utilities
        {'merchant': 'Türk Telekom', 'category': 'BILLS_UTILITIES', 'amount_range': (-80, -200)},
        {'merchant': 'Vodafone', 'category': 'BILLS_UTILITIES', 'amount_range': (-60, -150)},
        {'merchant': 'Turkcell', 'category': 'BILLS_UTILITIES', 'amount_range': (-70, -180)},
        {'merchant': 'TEDAŞ', 'category': 'BILLS_UTILITIES', 'amount_range': (-150, -400)},
        {'merchant': 'İGDAŞ', 'category': 'BILLS_UTILITIES', 'amount_range': (-100, -300)},
        {'merchant': 'İSKİ', 'category': 'BILLS_UTILITIES', 'amount_range': (-50, -150)},
        {'merchant': 'Netflix', 'category': 'ENTERTAINMENT', 'amount_range': (-30, -50)},
        {'merchant': 'Spotify', 'category': 'ENTERTAINMENT', 'amount_range': (-18, -25)},
        
        # Entertainment
        {'merchant': 'Cinemaximum', 'category': 'ENTERTAINMENT', 'amount_range': (-35, -80)},
        {'merchant': 'CinePlex', 'category': 'ENTERTAINMENT', 'amount_range': (-30, -70)},
        {'merchant': 'Steam', 'category': 'ENTERTAINMENT', 'amount_range': (-20, -200)},
        {'merchant': 'PlayStation Store', 'category': 'ENTERTAINMENT', 'amount_range': (-50, -300)},
        
        # Income sources (positive amounts)
        {'merchant': 'Maaş Ödemesi', 'category': 'SALARY', 'amount_range': (8000, 25000)},
        {'merchant': 'Freelance Ödeme', 'category': 'TRANSFER', 'amount_range': (1000, 5000)},
        {'merchant': 'Banka Faizi', 'category': 'TRANSFER', 'amount_range': (50, 500)},
        {'merchant': 'İade', 'category': 'TRANSFER', 'amount_range': (20, 800)},
        {'merchant': 'Yatırım Getirisi', 'category': 'TRANSFER', 'amount_range': (200, 3000)},
    ]
    
    # Generate transactions for each account
    for account in accounts:
        print(f"Generating transactions for {account.bank_name}...")
        
        # Generate 50-150 transactions over the last 6 months
        num_transactions = random.randint(50, 150)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=180)
        
        transactions = []
        
        for _ in range(num_transactions):
            template = random.choice(transaction_templates)
            
            # Generate amount
            min_amount, max_amount = template['amount_range']
            amount = round(random.uniform(min_amount, max_amount), 2)
            
            # Generate random date
            random_days = random.randint(0, 180)
            transaction_date = start_date + timedelta(days=random_days)
            transaction_date += timedelta(
                hours=random.randint(6, 23),
                minutes=random.randint(0, 59)
            )
            
            transaction = Transaction(
                user=account.user,
                account=account,
                date=transaction_date,
                amount=Decimal(str(amount)),
                currency='TRY',
                category=template['category'],
                description=template['merchant'],
                merchant=template['merchant']
            )
            transactions.append(transaction)
        
        # Add monthly salary for checking/savings accounts (FIXED DATE HANDLING)
        if account.account_type in ['CHECKING', 'SAVINGS']:
            for month_offset in range(1, 7):  # Last 6 months
                # Calculate target date more safely
                current_date = timezone.now()
                
                # Go back month_offset months
                year = current_date.year
                month = current_date.month - month_offset
                
                while month <= 0:
                    month += 12
                    year -= 1
                
                # Get the last day of that month
                last_day = calendar.monthrange(year, month)[1]
                
                # Pick a random day between 25 and the last day
                salary_day = random.randint(25, min(30, last_day))
                
                salary_date = datetime(year, month, salary_day, 
                                     random.randint(9, 17), random.randint(0, 59))
                salary_date = timezone.make_aware(salary_date)
                
                salary_amount = random.uniform(8000, 20000)
                
                salary_transaction = Transaction(
                    user=account.user,
                    account=account,
                    date=salary_date,
                    amount=Decimal(str(round(salary_amount, 2))),
                    currency='TRY',
                    category='SALARY',
                    description='Maaş Ödemesi',
                    merchant='İşveren'
                )
                transactions.append(salary_transaction)
        
        # Bulk create transactions
        Transaction.objects.bulk_create(transactions)
        print(f"  Created {len(transactions)} transactions")

if __name__ == '__main__':
    generate_demo_data()