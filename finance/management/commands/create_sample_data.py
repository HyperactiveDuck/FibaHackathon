from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from finance.models import UserProfile, Account, Transaction
from decimal import Decimal
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Create sample data for the finance app'

    def handle(self, *args, **options):
        # Clear existing data
        Transaction.objects.all().delete()
        Account.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.filter(username='ahmet_yilmaz').delete()
        
        # Create sample user
        user = User.objects.create_user(
            username='ahmet_yilmaz',
            email='ahmet.yilmaz@email.com',
            password='password123',
            first_name='Ahmet',
            last_name='Yılmaz'
        )
        
        # Create user profile
        profile = UserProfile.objects.create(
            user=user,
            name='Ahmet Yılmaz',
            birthdate='1990-05-15',
            city='Istanbul',
            email='ahmet.yilmaz@email.com',
            risk_score=25
        )
        
        # Create sample accounts
        accounts = [
            Account.objects.create(
                user=user,
                bank_name='Akbank',
                account_type='BUSINESS',
                iban='TR330006200119000006672315',
                currency='TRY',
                balance=Decimal('2451.05')
            ),
            Account.objects.create(
                user=user,
                bank_name='Garanti BBVA',
                account_type='SAVINGS',
                iban='TR640006200056000006672316',
                currency='TRY',
                balance=Decimal('15750.00')
            ),
            Account.objects.create(
                user=user,
                bank_name='İş Bankası',
                account_type='CREDIT',
                iban='TR330006400000000006672317',
                currency='TRY',
                balance=Decimal('0.00')
            )
        ]
        
        # Sample transactions data
        sample_transactions = [
            # Recent transactions
            {
                'account': accounts[1],  # Garanti Savings
                'date': datetime.now(),
                'amount': Decimal('3250.00'),
                'category': 'SALARY',
                'description': 'Salary Payment',
                'merchant': 'TÜRK TEKNOLOJI A.Ş.'
            },
            {
                'account': accounts[2],  # İş Bankası Credit
                'date': datetime.now() - timedelta(hours=5),
                'amount': Decimal('-24.50'),
                'category': 'FOOD_DINING',
                'description': 'Food Delivery',
                'merchant': 'Yemeksepeti'
            },
            {
                'account': accounts[0],  # Akbank Business
                'date': datetime.now() - timedelta(days=1, hours=10),
                'amount': Decimal('-67.89'),
                'category': 'SHOPPING',
                'description': 'Grocery Shopping',
                'merchant': 'Migros'
            },
            {
                'account': accounts[0],
                'date': datetime.now() - timedelta(days=2, hours=16),
                'amount': Decimal('-120.00'),
                'category': 'BILLS_UTILITIES',
                'description': 'Electricity Bill',
                'merchant': 'TEDAŞ'
            },
            {
                'account': accounts[2],
                'date': datetime.now() - timedelta(days=3, hours=8),
                'amount': Decimal('-12.40'),
                'category': 'TRANSPORTATION',
                'description': 'Public Transport',
                'merchant': 'Istanbul Kart'
            },
            {
                'account': accounts[2],
                'date': datetime.now() - timedelta(days=4, hours=14),
                'amount': Decimal('-29.99'),
                'category': 'ENTERTAINMENT',
                'description': 'Streaming Service',
                'merchant': 'Netflix'
            },
            {
                'account': accounts[0],
                'date': datetime.now() - timedelta(days=5, hours=12),
                'amount': Decimal('-85.00'),
                'category': 'TRANSPORTATION',
                'description': 'Fuel',
                'merchant': 'Shell Petrol'
            },
            # Generate more transactions for the month
        ]
        
        # Add more random transactions for realistic data
        merchants = {
            'FOOD_DINING': ['Yemeksepeti', 'Getir', 'McDonald\'s', 'Starbucks', 'Domino\'s'],
            'SHOPPING': ['Migros', 'CarrefourSA', 'LC Waikiki', 'H&M', 'Teknosa'],
            'TRANSPORTATION': ['Shell', 'BP', 'Istanbul Kart', 'BiTaksi', 'Uber'],
            'BILLS_UTILITIES': ['TEDAŞ', 'İGDAŞ', 'Türk Telekom', 'Vodafone', 'Turkcell'],
            'ENTERTAINMENT': ['Netflix', 'Spotify', 'Cinema Plus', 'PlayStation', 'Steam']
        }
        
        # Generate 30 days of transactions
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            
            # Random number of transactions per day (0-3)
            daily_transactions = random.randint(0, 3)
            
            for _ in range(daily_transactions):
                category = random.choice(list(merchants.keys()))
                merchant = random.choice(merchants[category])
                account = random.choice(accounts[:2])  # Don't use credit for income
                
                if category == 'SALARY':
                    amount = Decimal(str(random.uniform(3000, 4000)))
                else:
                    amount = Decimal(str(-random.uniform(10, 200)))
                
                sample_transactions.append({
                    'account': account,
                    'date': date - timedelta(hours=random.randint(8, 20)),
                    'amount': amount,
                    'category': category,
                    'description': f'{merchant} Transaction',
                    'merchant': merchant
                })
        
        # Create all transactions
        for trans_data in sample_transactions:
            Transaction.objects.create(
                user=user,
                account=trans_data['account'],
                date=trans_data['date'],
                amount=trans_data['amount'],
                currency='TRY',
                category=trans_data['category'],
                description=trans_data['description'],
                merchant=trans_data['merchant']
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- 1 User: {user.username}\n'
                f'- {len(accounts)} Accounts\n'
                f'- {Transaction.objects.count()} Transactions'
            )
        )