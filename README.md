# Finance Mirror - Personal Finance Dashboard / Kişisel Finans Paneli

[English](#english) | [Türkçe](#türkçe)

---

## English

A comprehensive personal finance management application built with Django, featuring advanced analytics, budget tracking, transaction management, and AI-powered insights.

### 🚀 Features

#### Core Functionality
- **User Authentication**: Secure login/logout system with session management
- **Multi-User Support**: Support for multiple users with isolated data
- **Dashboard**: Real-time financial overview with key metrics and visualizations
- **Account Management**: Connect and manage multiple bank accounts
- **Transaction Tracking**: Comprehensive transaction history with filtering and search
- **Budget Management**: Set and track spending limits by category
- **Analytics**: Advanced financial analytics with AI-powered insights
- **Fraud Detection**: Suspicious activity monitoring and reporting

#### Advanced Features
- **AI Assistant**: Interactive chatbot for financial advice
- **Data Visualization**: Dynamic charts using HTML5 Canvas
- **Export Functionality**: CSV export for transactions and analytics
- **Real-time Updates**: Live data synchronization
- **Responsive Design**: Mobile-friendly dark theme interface
- **Security Features**: Bank-level encryption and PCI DSS compliance simulation

### 🛠 Technologies Used

#### Backend
- **Django 4.2+**: Python web framework
- **SQLite**: Default database (easily configurable for PostgreSQL/MySQL)
- **Python 3.8+**: Core programming language

#### Frontend
- **HTML5**: Semantic markup with modern standards
- **CSS3**: Custom styling with CSS Grid and Flexbox
- **JavaScript (Vanilla)**: Interactive features and Canvas-based charts
- **No external CSS/JS frameworks**: Pure custom implementation

#### Design & UI
- **Dark Theme**: Modern, professional interface
- **Inter Font**: Clean, readable typography
- **CSS Custom Properties**: Consistent color scheme and spacing
- **Responsive Grid System**: Mobile-first design approach

#### Data & Analytics
- **Django ORM**: Database queries and aggregations
- **Custom Template Filters**: Data processing and formatting
- **CSV Export**: Data portability features
- **Real-time Calculations**: Dynamic financial metrics

### 📁 Project Structure

```
FibaHackathon/
├── config/                     # Django project configuration
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI application
├── finance/                   # Main application
│   ├── migrations/           # Database migrations
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template
│   │   └── finance/         # App-specific templates
│   │       ├── login.html   # Authentication
│   │       ├── dashboard.html
│   │       ├── accounts.html
│   │       ├── transactions.html
│   │       ├── budgets.html
│   │       ├── analytics.html
│   │       └── settings.html
│   ├── templatetags/        # Custom template filters
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── urls.py             # App URL patterns
│   └── views.py            # View functions
├── venv/                   # Virtual environment (created during setup)
├── manage.py              # Django management script
├── db.sqlite3            # SQLite database (created after migrations)
└── README.md             # This file
```

### 🚀 Installation & Setup

#### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

#### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/FibaHackathon.git
cd FibaHackathon
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install django
```

#### Step 4: Database Setup
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser
```

#### Step 5: Create Demo Users
```bash
# Start Django shell
python manage.py shell
```

In the Django shell, run:
```python
from django.contrib.auth.models import User

# Create demo users with specific IDs
user1 = User.objects.create_user(username='user1', password='password123')
user1.id = 1
user1.save()

user2 = User.objects.create_user(username='user2', password='password123')
user2.id = 2
user2.save()

user3 = User.objects.create_user(username='user3', password='password123')
user3.id = 3
user3.save()

print("Demo users created successfully!")
exit()
```

#### Step 6: Load Sample Data (Optional)
```bash
# Start Django shell again
python manage.py shell
```

```python
from finance.models import Account, Transaction
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random

# Get demo users
user1 = User.objects.get(id=1)
user2 = User.objects.get(id=2)
user3 = User.objects.get(id=3)

# Create sample accounts
accounts_data = [
    {'user': user1, 'bank_name': 'Fibabanka', 'account_type': 'Checking', 'balance': 5250.00},
    {'user': user1, 'bank_name': 'Garanti BBVA', 'account_type': 'Savings', 'balance': 12800.00},
    {'user': user2, 'bank_name': 'İş Bankası', 'account_type': 'Business', 'balance': 8900.00},
    {'user': user3, 'bank_name': 'Akbank', 'account_type': 'Checking', 'balance': 3200.00},
]

for account_data in accounts_data:
    Account.objects.create(**account_data)

# Create sample transactions
categories = ['FOOD_DINING', 'SHOPPING', 'TRANSPORTATION', 'BILLS_UTILITIES', 'ENTERTAINMENT', 'SALARY']
merchants = ['Migros', 'Starbucks', 'Shell', 'Netflix', 'Uber', 'Amazon', 'Zara', 'BKM Mutfak']

accounts = Account.objects.all()
for account in accounts:
    for i in range(50):  # 50 transactions per account
        amount = random.uniform(-500, 2000) if random.random() > 0.7 else random.uniform(-200, -10)
        Transaction.objects.create(
            account=account,
            user=account.user,
            amount=amount,
            category=random.choice(categories),
            merchant=random.choice(merchants),
            description=f"Transaction from {random.choice(merchants)}",
            date=datetime.now() - timedelta(days=random.randint(1, 90))
        )

print("Sample data created successfully!")
exit()
```

#### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

### 🔐 Authentication

#### Demo Accounts
The application comes with three pre-configured demo accounts:

| Username | Password    | User ID |
|----------|-------------|---------|
| user1    | password123 | 1       |
| user2    | password123 | 2       |
| user3    | password123 | 3       |

#### Login Process
1. Navigate to `http://localhost:8000`
2. Enter credentials from the demo accounts above
3. Click "Sign In" to access the dashboard

### 🎯 Usage Guide

#### Dashboard
- **Financial Overview**: View total balance, monthly spending, and savings
- **Quick Metrics**: Key financial indicators with visual progress bars
- **Spending Charts**: Interactive pie charts for category breakdown
- **AI Assistant**: Chat interface for financial advice
- **Recent Activity**: Latest transactions and account updates

#### Accounts Management
- **View Accounts**: See all connected bank accounts with balances
- **Add New Account**: Simulate connecting new bank accounts
- **Transaction History**: Detailed transaction list per account
- **Account Performance**: Monthly inflow/outflow analysis

#### Transaction Tracking
- **Filter & Search**: Advanced filtering by date, category, amount
- **Fraud Detection**: Suspicious transaction alerts
- **Export Data**: Download transaction history as CSV
- **Categorization**: Automatic categorization with icons

#### Budget Management
- **Category Budgets**: Set spending limits for different categories
- **Progress Tracking**: Visual progress bars and percentage indicators
- **AI Insights**: Smart recommendations for budget optimization
- **Monthly Overview**: Track spending against set limits

#### Analytics
- **Spending Trends**: Monthly spending analysis with charts
- **Category Breakdown**: Detailed spending by category
- **Merchant Analysis**: Top merchants and spending patterns
- **AI Recommendations**: Personalized financial advice
- **Export Reports**: Generate and download analytical reports

#### Settings
- **Profile Management**: Update personal information
- **Security Settings**: Manage passwords and authentication
- **Notifications**: Configure alert preferences
- **Data Export**: Download all financial data
- **Account Deletion**: Secure account removal

### 🔧 Configuration

#### Database Configuration
The application uses SQLite by default. To switch to PostgreSQL or MySQL:

1. Install the appropriate database adapter:
```bash
# For PostgreSQL
pip install psycopg2-binary

# For MySQL
pip install mysqlclient
```

2. Update `config/settings.py`:
```python
# PostgreSQL example
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'finance_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

#### Static Files (Production)
For production deployment:
```bash
python manage.py collectstatic
```

### 📊 Data Models

#### User
- Django's built-in User model
- Extended with profile information

#### Account
```python
- user: ForeignKey to User
- bank_name: CharField
- account_type: CharField
- account_number: CharField
- balance: DecimalField
- created_at: DateTimeField
```

#### Transaction
```python
- account: ForeignKey to Account
- user: ForeignKey to User
- amount: DecimalField
- category: CharField
- merchant: CharField
- description: TextField
- date: DateTimeField
- transaction_id: CharField
```

### 🎨 Styling & Theming

#### Color Scheme
```css
--bg-primary: #0a0a0a      /* Main background */
--bg-secondary: #111111     /* Card backgrounds */
--border-color: #27272a     /* Borders and dividers */
--text-primary: #fafafa     /* Primary text */
--text-secondary: #a1a1aa   /* Secondary text */
--text-muted: #71717a       /* Muted text */
--accent-green: #22c55e     /* Success/positive */
--accent-red: #ef4444       /* Error/negative */
--accent-blue: #3b82f6      /* Info/neutral */
--accent-yellow: #f59e0b    /* Warning */
```

#### Typography
- **Font Family**: Inter, system fonts
- **Headings**: 600-700 font weight
- **Body**: 400-500 font weight
- **Code**: Monospace fallbacks

### 🚀 Deployment

#### Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

#### Production Considerations
1. **Security Settings**:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for secrets

2. **Database**:
   - Use PostgreSQL or MySQL for production
   - Configure connection pooling

3. **Static Files**:
   - Configure static file serving
   - Use CDN for better performance

4. **HTTPS**:
   - Enable SSL/TLS encryption
   - Configure secure headers

#### Docker Deployment (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 🔍 API Endpoints

#### Authentication
- `GET /` - Login page
- `POST /login/` - User authentication
- `GET /logout/` - User logout

#### Main Views
- `GET /dashboard/` - Financial dashboard
- `GET /accounts/` - Account management
- `POST /accounts/add/` - Add new account
- `GET /transactions/` - Transaction history
- `GET /budgets/` - Budget management
- `GET /analytics/` - Financial analytics
- `GET /settings/` - User settings

#### Data Export
- `GET /transactions/?export=csv` - Export transactions
- `GET /analytics/?export=report` - Export analytics report

### 🧪 Testing

#### Run Tests
```bash
python manage.py test
```

#### Create Test Data
```bash
python manage.py shell
# Use the sample data creation script above
```

#### Test Coverage
```bash
pip install coverage
coverage run manage.py test
coverage report
```

### 🤝 Contributing

1. **Fork the Repository**
2. **Create Feature Branch**:
   ```bash
   git checkout -b feature/new-feature
   ```
3. **Make Changes**
4. **Commit Changes**:
   ```bash
   git commit -am 'Add new feature'
   ```
5. **Push to Branch**:
   ```bash
   git push origin feature/new-feature
   ```
6. **Create Pull Request**

#### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Maintain consistent indentation (4 spaces)

### 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

### 🐛 Troubleshooting

#### Common Issues

**1. ModuleNotFoundError: No module named 'django'**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install Django
pip install django
```

**2. Database Migration Errors**
```bash
# Reset migrations (if needed)
rm -rf finance/migrations/
python manage.py makemigrations finance
python manage.py migrate
```

**3. Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic
```

**4. Permission Denied Errors**
```bash
# Check file permissions
chmod +x manage.py
```

#### Debug Mode
Enable debug mode in `settings.py`:
```python
DEBUG = True
```

### 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting section

### 🔮 Future Enhancements

- [ ] Mobile app development
- [ ] Real bank API integration
- [ ] Advanced AI features
- [ ] Multi-currency support
- [ ] Investment tracking
- [ ] Bill reminders and notifications
- [ ] Goal setting and achievement tracking
- [ ] Family account sharing
- [ ] Advanced security features (2FA)
- [ ] Custom reporting and dashboards

---

## Türkçe

Django ile geliştirilmiş kapsamlı kişisel finans yönetimi uygulaması. Gelişmiş analitik, bütçe takibi, işlem yönetimi ve yapay zeka destekli öngörüler sunar.

### 🚀 Özellikler

#### Temel Fonksiyonlar
- **Kullanıcı Kimlik Doğrulama**: Oturum yönetimi ile güvenli giriş/çıkış sistemi
- **Çoklu Kullanıcı Desteği**: İzole verilerle birden fazla kullanıcı desteği
- **Panel**: Temel metrikler ve görselleştirmelerle gerçek zamanlı finansal genel bakış
- **Hesap Yönetimi**: Birden fazla banka hesabını bağlayın ve yönetin
- **İşlem Takibi**: Filtreleme ve arama özellikli kapsamlı işlem geçmişi
- **Bütçe Yönetimi**: Kategoriye göre harcama limitlerini belirleme ve takip etme
- **Analitik**: Yapay zeka destekli öngörülerle gelişmiş finansal analitik
- **Dolandırıcılık Tespiti**: Şüpheli aktivite izleme ve raporlama

#### Gelişmiş Özellikler
- **Yapay Zeka Asistanı**: Finansal tavsiye için etkileşimli chatbot
- **Veri Görselleştirme**: HTML5 Canvas kullanarak dinamik grafikler
- **Dışa Aktarma**: İşlemler ve analitik için CSV dışa aktarma
- **Gerçek Zamanlı Güncellemeler**: Canlı veri senkronizasyonu
- **Duyarlı Tasarım**: Mobil uyumlu koyu tema arayüzü
- **Güvenlik Özellikleri**: Banka seviyesi şifreleme ve PCI DSS uyumluluk simülasyonu

### 🛠 Kullanılan Teknolojiler

#### Backend
- **Django 4.2+**: Python web framework'ü
- **SQLite**: Varsayılan veritabanı (PostgreSQL/MySQL için kolayca yapılandırılabilir)
- **Python 3.8+**: Temel programlama dili

#### Frontend
- **HTML5**: Modern standartlarla semantik markup
- **CSS3**: CSS Grid ve Flexbox ile özel stil
- **JavaScript (Vanilla)**: Etkileşimli özellikler ve Canvas tabanlı grafikler
- **Harici CSS/JS framework yok**: Tamamen özel uygulama

#### Tasarım ve UI
- **Koyu Tema**: Modern, profesyonel arayüz
- **Inter Font**: Temiz, okunabilir tipografi
- **CSS Özel Özellikleri**: Tutarlı renk şeması ve aralık
- **Duyarlı Grid Sistemi**: Mobil öncelikli tasarım yaklaşımı

#### Veri ve Analitik
- **Django ORM**: Veritabanı sorguları ve toplamaları
- **Özel Template Filtreleri**: Veri işleme ve biçimlendirme
- **CSV Dışa Aktarma**: Veri taşınabilirlik özellikleri
- **Gerçek Zamanlı Hesaplamalar**: Dinamik finansal metrikler

### 📁 Proje Yapısı

```
FibaHackathon/
├── config/                     # Django proje yapılandırması
│   ├── __init__.py
│   ├── settings.py            # Proje ayarları
│   ├── urls.py               # Ana URL yapılandırması
│   └── wsgi.py               # WSGI uygulaması
├── finance/                   # Ana uygulama
│   ├── migrations/           # Veritabanı migrasyonları
│   ├── templates/           # HTML şablonları
│   │   ├── base.html        # Temel şablon
│   │   └── finance/         # Uygulamaya özel şablonlar
│   │       ├── login.html   # Kimlik doğrulama
│   │       ├── dashboard.html
│   │       ├── accounts.html
│   │       ├── transactions.html
│   │       ├── budgets.html
│   │       ├── analytics.html
│   │       └── settings.html
│   ├── templatetags/        # Özel şablon filtreleri
│   ├── __init__.py
│   ├── admin.py            # Django admin yapılandırması
│   ├── apps.py             # Uygulama yapılandırması
│   ├── models.py           # Veritabanı modelleri
│   ├── urls.py             # Uygulama URL kalıpları
│   └── views.py            # View fonksiyonları
├── venv/                   # Sanal ortam (kurulum sırasında oluşturulur)
├── manage.py              # Django yönetim betiği
├── db.sqlite3            # SQLite veritabanı (migrasyonlardan sonra oluşturulur)
└── README.md             # Bu dosya
```

### 🚀 Kurulum ve Ayarlar

#### Gereksinimler
- Python 3.8 veya üstü
- pip (Python paket yükleyicisi)
- Git (depoyu klonlamak için)

#### Adım 1: Depoyu Klonlayın
```bash
git clone https://github.com/kullaniciadi/FibaHackathon.git
cd FibaHackathon
```

#### Adım 2: Sanal Ortam Oluşturun
```bash
# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı etkinleştir
# Windows'ta:
venv\Scripts\activate

# macOS/Linux'ta:
source venv/bin/activate
```

#### Adım 3: Bağımlılıkları Yükleyin
```bash
pip install django
```

#### Adım 4: Veritabanı Kurulumu
```bash
# Migrasyonları oluştur ve uygula
python manage.py makemigrations
python manage.py migrate

# Süper kullanıcı oluştur (isteğe bağlı, admin erişimi için)
python manage.py createsuperuser
```

#### Adım 5: Demo Kullanıcıları Oluşturun
```bash
# Django shell'ini başlat
python manage.py shell
```

Django shell'inde şunu çalıştırın:
```python
from django.contrib.auth.models import User

# Belirli ID'lerle demo kullanıcıları oluştur
user1 = User.objects.create_user(username='user1', password='password123')
user1.id = 1
user1.save()

user2 = User.objects.create_user(username='user2', password='password123')
user2.id = 2
user2.save()

user3 = User.objects.create_user(username='user3', password='password123')
user3.id = 3
user3.save()

print("Demo kullanıcıları başarıyla oluşturuldu!")
exit()
```

#### Adım 6: Örnek Veri Yükleyin (İsteğe Bağlı)
```bash
# Django shell'ini tekrar başlat
python manage.py shell
```

```python
from finance.models import Account, Transaction
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random

# Demo kullanıcıları al
user1 = User.objects.get(id=1)
user2 = User.objects.get(id=2)
user3 = User.objects.get(id=3)

# Örnek hesaplar oluştur
accounts_data = [
    {'user': user1, 'bank_name': 'Fibabanka', 'account_type': 'Vadesiz', 'balance': 5250.00},
    {'user': user1, 'bank_name': 'Garanti BBVA', 'account_type': 'Vadeli', 'balance': 12800.00},
    {'user': user2, 'bank_name': 'İş Bankası', 'account_type': 'Ticari', 'balance': 8900.00},
    {'user': user3, 'bank_name': 'Akbank', 'account_type': 'Vadesiz', 'balance': 3200.00},
]

for account_data in accounts_data:
    Account.objects.create(**account_data)

# Örnek işlemler oluştur
categories = ['YEMEK_RESTORAN', 'ALISVERIS', 'ULASIM', 'FATURALAR', 'EGLENCE', 'MAAS']
merchants = ['Migros', 'Starbucks', 'Shell', 'Netflix', 'Uber', 'Amazon', 'Zara', 'BKM Mutfak']

accounts = Account.objects.all()
for account in accounts:
    for i in range(50):  # Hesap başına 50 işlem
        amount = random.uniform(-500, 2000) if random.random() > 0.7 else random.uniform(-200, -10)
        Transaction.objects.create(
            account=account,
            user=account.user,
            amount=amount,
            category=random.choice(categories),
            merchant=random.choice(merchants),
            description=f"{random.choice(merchants)} işlemi",
            date=datetime.now() - timedelta(days=random.randint(1, 90))
        )

print("Örnek veriler başarıyla oluşturuldu!")
exit()
```

#### Adım 7: Geliştirme Sunucusunu Çalıştırın
```bash
python manage.py runserver
```

Tarayıcınızda `http://localhost:8000` adresini ziyaret edin.

### 🔐 Kimlik Doğrulama

#### Demo Hesapları
Uygulama üç önceden yapılandırılmış demo hesapla gelir:

| Kullanıcı Adı | Şifre       | Kullanıcı ID |
|----------------|-------------|--------------|
| user1          | password123 | 1            |
| user2          | password123 | 2            |
| user3          | password123 | 3            |

#### Giriş Süreci
1. `http://localhost:8000` adresine gidin
2. Yukarıdaki demo hesaplardan kimlik bilgilerini girin
3. Panele erişmek için "Giriş Yap" butonuna tıklayın

### 🎯 Kullanım Kılavuzu

#### Panel
- **Finansal Genel Bakış**: Toplam bakiye, aylık harcama ve tasarrufları görüntüleyin
- **Hızlı Metrikler**: Görsel ilerleme çubuklarıyla ana finansal göstergeler
- **Harcama Grafikleri**: Kategori dağılımı için etkileşimli pasta grafikleri
- **Yapay Zeka Asistanı**: Finansal tavsiye için sohbet arayüzü
- **Son Aktiviteler**: En son işlemler ve hesap güncellemeleri

#### Hesap Yönetimi
- **Hesapları Görüntüle**: Bakiyelerle birlikte tüm bağlı banka hesaplarını görün
- **Yeni Hesap Ekle**: Yeni banka hesaplarını bağlamayı simüle edin
- **İşlem Geçmişi**: Hesap başına detaylı işlem listesi
- **Hesap Performansı**: Aylık giriş/çıkış analizi

#### İşlem Takibi
- **Filtrele ve Ara**: Tarih, kategori, tutar bazında gelişmiş filtreleme
- **Dolandırıcılık Tespiti**: Şüpheli işlem uyarıları
- **Veri Dışa Aktarma**: İşlem geçmişini CSV olarak indirin
- **Kategorilendirme**: İkonlarla otomatik kategorilendirme

#### Bütçe Yönetimi
- **Kategori Bütçeleri**: Farklı kategoriler için harcama limitleri belirleyin
- **İlerleme Takibi**: Görsel ilerleme çubukları ve yüzde göstergeleri
- **Yapay Zeka Öngörüleri**: Bütçe optimizasyonu için akıllı öneriler
- **Aylık Genel Bakış**: Belirlenen limitlere karşı harcama takibi

#### Analitik
- **Harcama Eğilimleri**: Grafiklerle aylık harcama analizi
- **Kategori Dağılımı**: Kategoriye göre detaylı harcama
- **Satıcı Analizi**: En çok harcama yapılan yerler ve kalıplar
- **Yapay Zeka Önerileri**: Kişiselleştirilmiş finansal tavsiyeler
- **Rapor Dışa Aktarma**: Analitik raporları oluşturun ve indirin

#### Ayarlar
- **Profil Yönetimi**: Kişisel bilgileri güncelleme
- **Güvenlik Ayarları**: Şifre ve kimlik doğrulama yönetimi
- **Bildirimler**: Uyarı tercihlerini yapılandırma
- **Veri Dışa Aktarma**: Tüm finansal verileri indirme
- **Hesap Silme**: Güvenli hesap kaldırma

### 🔧 Yapılandırma

#### Veritabanı Yapılandırması
Uygulama varsayılan olarak SQLite kullanır. PostgreSQL veya MySQL'e geçmek için:

1. Uygun veritabanı adaptörünü yükleyin:
```bash
# PostgreSQL için
pip install psycopg2-binary

# MySQL için
pip install mysqlclient
```

2. `config/settings.py` dosyasını güncelleyin:
```python
# PostgreSQL örneği
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'finance_db',
        'USER': 'kullanici_adi',
        'PASSWORD': 'sifre',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Ortam Değişkenleri
Proje kök dizininde `.env` dosyası oluşturun:
```env
SECRET_KEY=gizli-anahtar-buraya
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

#### Statik Dosyalar (Prodüksiyon)
Prodüksiyon dağıtımı için:
```bash
python manage.py collectstatic
```

### 📊 Veri Modelleri

#### Kullanıcı
- Django'nun yerleşik User modeli
- Profil bilgileriyle genişletilmiş

#### Hesap
```python
- user: User'a ForeignKey
- bank_name: CharField
- account_type: CharField
- account_number: CharField
- balance: DecimalField
- created_at: DateTimeField
```

#### İşlem
```python
- account: Account'a ForeignKey
- user: User'a ForeignKey
- amount: DecimalField
- category: CharField
- merchant: CharField
- description: TextField
- date: DateTimeField
- transaction_id: CharField
```

### 🎨 Stil ve Tema

#### Renk Şeması
```css
--bg-primary: #0a0a0a      /* Ana arka plan */
--bg-secondary: #111111     /* Kart arka planları */
--border-color: #27272a     /* Kenarlıklar ve ayırıcılar */
--text-primary: #fafafa     /* Ana metin */
--text-secondary: #a1a1aa   /* İkincil metin */
--text-muted: #71717a       /* Soluk metin */
--accent-green: #22c55e     /* Başarı/pozitif */
--accent-red: #ef4444       /* Hata/negatif */
--accent-blue: #3b82f6      /* Bilgi/nötr */
--accent-yellow: #f59e0b    /* Uyarı */
```

#### Tipografi
- **Font Ailesi**: Inter, sistem fontları
- **Başlıklar**: 600-700 font ağırlığı
- **Gövde**: 400-500 font ağırlığı
- **Kod**: Monospace yedekleri

### 🚀 Dağıtım

#### Geliştirme Sunucusu
```bash
python manage.py runserver 0.0.0.0:8000
```

#### Prodüksiyon Değerlendirmeleri
1. **Güvenlik Ayarları**:
   - `DEBUG = False` ayarlayın
   - `ALLOWED_HOSTS` yapılandırın
   - Gizli bilgiler için ortam değişkenlerini kullanın

2. **Veritabanı**:
   - Prodüksiyon için PostgreSQL veya MySQL kullanın
   - Bağlantı havuzlaması yapılandırın

3. **Statik Dosyalar**:
   - Statik dosya sunumunu yapılandırın
   - Daha iyi performans için CDN kullanın

4. **HTTPS**:
   - SSL/TLS şifrelemesini etkinleştirin
   - Güvenli başlıkları yapılandırın

#### Docker Dağıtımı (İsteğe Bağlı)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 🔍 API Endpoint'leri

#### Kimlik Doğrulama
- `GET /` - Giriş sayfası
- `POST /login/` - Kullanıcı kimlik doğrulama
- `GET /logout/` - Kullanıcı çıkışı

#### Ana Görünümler
- `GET /dashboard/` - Finansal panel
- `GET /accounts/` - Hesap yönetimi
- `POST /accounts/add/` - Yeni hesap ekleme
- `GET /transactions/` - İşlem geçmişi
- `GET /budgets/` - Bütçe yönetimi
- `GET /analytics/` - Finansal analitik
- `GET /settings/` - Kullanıcı ayarları

#### Veri Dışa Aktarma
- `GET /transactions/?export=csv` - İşlemleri dışa aktar
- `GET /analytics/?export=report` - Analitik raporu dışa aktar

### 🧪 Test Etme

#### Testleri Çalıştır
```bash
python manage.py test
```

#### Test Verisi Oluştur
```bash
python manage.py shell
# Yukarıdaki örnek veri oluşturma betiğini kullanın
```

#### Test Kapsamı
```bash
pip install coverage
coverage run manage.py test
coverage report
```

### 🤝 Katkıda Bulunma

1. **Depoyu Fork Edin**
2. **Özellik Dalı Oluşturun**:
   ```bash
   git checkout -b feature/yeni-ozellik
   ```
3. **Değişiklik Yapın**
4. **Değişiklikleri Commit Edin**:
   ```bash
   git commit -am 'Yeni özellik ekle'
   ```
5. **Dala Push Edin**:
   ```bash
   git push origin feature/yeni-ozellik
   ```
6. **Pull Request Oluşturun**

#### Kod Stili
- Python kodu için PEP 8'i takip edin
- Anlamlı değişken ve fonksiyon isimleri kullanın
- Karmaşık mantık için yorumlar ekleyin
- Tutarlı girinti koruyun (4 boşluk)

### 📝 Lisans

Bu proje Apache Lisansı 2.0 altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

### 🐛 Sorun Giderme

#### Yaygın Sorunlar

**1. ModuleNotFoundError: No module named 'django'**
```bash
# Sanal ortamın etkinleştirildiğinden emin olun
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Django'yu yükleyin
pip install django
```

**2. Veritabanı Migrasyon Hataları**
```bash
# Migrasyonları sıfırlayın (gerekirse)
rm -rf finance/migrations/
python manage.py makemigrations finance
python manage.py migrate
```

**3. Statik Dosyalar Yüklenmiyor**
```bash
# Statik dosyaları toplayın
python manage.py collectstatic
```

**4. İzin Reddedildi Hataları**
```bash
# Dosya izinlerini kontrol edin
chmod +x manage.py
```

#### Hata Ayıklama Modu
`settings.py` dosyasında hata ayıklama modunu etkinleştirin:
```python
DEBUG = True
```

### 📞 Destek

Destek ve sorular için:
- GitHub'da issue oluşturun
- Dokümantasyonu kontrol edin
- Sorun giderme bölümünü inceleyin

### 🔮 Gelecek Geliştirmeler

- [ ] Mobil uygulama geliştirme
- [ ] Gerçek banka API entegrasyonu
- [ ] Gelişmiş yapay zeka özellikleri
- [ ] Çoklu para birimi desteği
- [ ] Yatırım takibi
- [ ] Fatura hatırlatıcıları ve bildirimler
- [ ] Hedef belirleme ve başarı takibi
- [ ] Aile hesabı paylaşımı
- [ ] Gelişmiş güvenlik özellikleri (2FA)
- [ ] Özel raporlama ve paneller



---

# MCP Open Banking Server

A Python-based Model Context Protocol (MCP) server that provides open banking functionalities for financial data processing and analysis. This server integrates with the Finance Mirror dashboard to deliver AI-powered banking insights through Claude AI.

## Overview

This MCP server acts as a bridge between banking data and AI models, enabling sophisticated financial analysis through the Model Context Protocol. It processes banking transactions, account information, and user data to provide intelligent insights and responses through Claude AI integration.

## Project Structure

```
mcp-open-banking/
├── main.py                    # Main MCP server implementation
├── pyproject.toml            # Python project configuration and dependencies
├── README.md                 # This documentation file
├── transactions.csv          # Sample transaction data
├── uv.lock                   # UV package manager lock file
├── datas/                    # Data directory
│   ├── accounts.csv         # Sample account data
│   └── users.csv            # Sample user data
└── helpers/                  # Utility modules
    ├── csvparser.py         # CSV data parsing utilities
    └── __pycache__/         # Python compiled bytecode cache
        ├── csvparser.cpython-311.pyc
        └── csvparser.cpython-312.pyc
```

## Features

- **MCP Protocol Integration**: Implements Model Context Protocol for AI tool interactions
- **Banking Data Processing**: Handles transactions, accounts, and user data
- **CSV Data Management**: Efficient parsing and processing of banking CSV files
- **Financial Analytics**: Provides tools for transaction analysis and insights
- **Claude AI Compatible**: Works seamlessly with Anthropic's Claude AI models
- **Open Banking Standards**: Follows open banking data formats and practices

## Prerequisites

- Python 3.11 or 3.12 (based on compiled bytecode presence)
- UV package manager (recommended) or pip
- Access to banking CSV data files

## Installation

### Using UV (Recommended)
```bash
# Navigate to the project directory
cd /home/yadhere/Documents/FibaHackathon/mcp-open-banking

# Install dependencies with UV
uv sync
```

### Using Pip
```bash
# Navigate to the project directory
cd /home/yadhere/Documents/FibaHackathon/mcp-open-banking

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Usage

### Starting the MCP Server

```bash
# Run the main server
python main.py
```

### Integration with MCP Client

This server is designed to work with the TypeScript MCP client in the parent project:

```bash
# From the main project directory
cd mcp-client-typescript
node build/index.js ../mcp-open-banking/main.py
```

## Data Files

### transactions.csv
Contains sample transaction data with fields like:
- Transaction ID
- Account ID
- Amount
- Date
- Merchant
- Category
- Description

### datas/accounts.csv
Contains account information including:
- Account ID
- User ID
- Bank Name
- Account Type
- Balance
- Account Number

### datas/users.csv
Contains user profile data such as:
- User ID
- Name
- Email
- Phone
- Address
- Registration Date

## Helper Modules

### csvparser.py
Utility module for parsing and processing CSV banking data files. Provides functions for:
- Loading CSV data into Python data structures
- Data validation and cleaning
- Format conversion for MCP protocol
- Error handling for malformed data

## MCP Tools

The server implements various MCP tools for financial analysis:

- **Transaction Analysis**: Analyze spending patterns and trends
- **Account Summary**: Get account balances and status
- **Category Breakdown**: Spending analysis by category
- **Fraud Detection**: Identify suspicious transactions
- **Budget Tracking**: Monitor spending against budgets
- **Financial Insights**: AI-powered financial recommendations

## Configuration

### pyproject.toml
The project configuration file defines:
- Project metadata
- Python dependencies
- Build system requirements
- Development dependencies
- Entry points for the MCP server

Example configuration structure:
```toml
[project]
name = "mcp-open-banking"
version = "1.0.0"
description = "MCP server for open banking functionality"
dependencies = [
    "mcp",
    "pandas",
    "numpy",
    # other dependencies
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Development

### Adding New Tools
To add new MCP tools to the server:

1. Define the tool in `main.py`
2. Implement the tool handler function
3. Register the tool with the MCP server
4. Update data processing in `helpers/csvparser.py` if needed

### Data Processing
To modify data processing:

1. Edit `helpers/csvparser.py` for CSV parsing logic
2. Add new data validation rules
3. Implement new data transformation functions
4. Test with sample data files

### Testing
```bash
# Run tests (if test files are added)
python -m pytest

# Manual testing with sample data
python -c "from helpers.csvparser import *; test_data_loading()"
```

## Integration with Finance Mirror

This MCP server integrates with the main Finance Mirror Django application by:

1. **Data Source**: Providing financial data through MCP protocol
2. **AI Assistant**: Enabling Claude AI to answer financial queries
3. **Real-time Analysis**: Processing transaction data for insights
4. **API Bridge**: Acting as middleware between banking data and AI

### Connection Flow
```
Finance Mirror Dashboard ←→ MCP TypeScript Client ←→ MCP Open Banking Server ←→ Banking Data (CSV)
```

## Security Considerations

- **Data Privacy**: Ensure CSV files contain only anonymized/test data
- **Access Control**: Implement proper authentication for production use
- **Data Validation**: Validate all incoming data before processing
- **Error Handling**: Graceful handling of malformed or missing data

## Troubleshooting

### Common Issues

**1. Module Import Errors**
```bash
# Ensure proper installation
uv sync
# or
pip install -e .
```

**2. CSV File Not Found**
```bash
# Check file paths in main.py
# Ensure CSV files are in correct locations
ls -la datas/
ls -la transactions.csv
```

**3. Python Version Compatibility**
```bash
# Check Python version
python --version
# Ensure using Python 3.11 or 3.12
```

**4. MCP Protocol Errors**
```bash
# Check MCP client connection
# Verify server is responding to MCP requests
# Review server logs for errors
```

### Debugging
```bash
# Run with verbose output
python main.py --verbose

# Check CSV data integrity
python -c "from helpers.csvparser import validate_csv_data; validate_csv_data()"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add new tools or improve data processing
4. Test with sample data
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Add docstrings to all functions
- Include type hints where possible
- Write tests for new functionality

## License

This project is part of the Finance Mirror application and follows the same Apache License 2.0.

## Related Projects

- [Finance Mirror Dashboard](../README.md) - Main Django application
- [MCP Client TypeScript](../mcp-client-typescript/README.md) - TypeScript MCP client
- [Model Context Protocol](https://github.com/modelcontextprotocol) - MCP specification

---

**Built with ❤️ for the Fibabanka Hackathon**

**Version**: 1.0.0  
**Python**: 3.11/3.12  
**MCP Protocol**: Compatible  
**Last Updated**: January 2024

---

# MCP Client TypeScript

A TypeScript client for interacting with Model Context Protocol (MCP) servers through Claude AI. This project provides both a CLI interface and an HTTP API server for processing queries using MCP tools.

## Overview

This MCP (Model Context Protocol) client serves as a bridge between Claude AI and various MCP servers, enabling sophisticated tool interactions and data processing. The client can spawn MCP servers (Python or JavaScript), communicate with them via the MCP protocol, and process user queries through Claude AI using the available tools.

## Features

- **HTTP API Server**: RESTful endpoints for health checks and chat processing
- **MCP Server Management**: Automatic spawning and management of MCP server processes
- **Claude AI Integration**: Seamless integration with Anthropic's Claude AI models
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **TypeScript**: Full type safety and modern JavaScript features
- **Error Handling**: Comprehensive error handling and graceful shutdown

## Prerequisites

Before running this project, ensure you have:

- **Node.js 18+**: Required for running the TypeScript application
- **Python 3.12**: Required for Python MCP servers
- **npm**: For dependency management
- **Anthropic API Key**: Required for Claude AI integration

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd mcp-client-typescript
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   PORT=3000
   ```

4. **Build the project**:
   ```bash
   npm run build
   ```

## Usage

### Starting the Server

Run the application with a path to your MCP server script:

```bash
node build/index.js <path_to_server_script>
```

**Examples:**
```bash
# For a Python MCP server
node build/index.js ./servers/my-python-server.py

# For a JavaScript MCP server
node build/index.js ./servers/my-js-server.js

# Using relative paths
node build/index.js ../mcp-open-banking/main.py
```

### API Endpoints

Once the server is running, you can interact with it through the following endpoints:

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "tools": ["tool1", "tool2", "tool3"]
}
```

#### Chat/Query Processing
```http
POST /chat
Content-Type: application/json

{
  "query": "Your question or request here"
}
```

**Response:**
```json
{
  "response": "Claude's response using MCP tools"
}
```

### Example Usage

```bash
# Start the server
node build/index.js ./my-mcp-server.py

# In another terminal, test the API
curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What tools are available?"}'
```

## Development

### Scripts

- `npm run build`: Compile TypeScript to JavaScript
- `npm test`: Run tests (currently not implemented)

### Project Structure

```
mcp-client-typescript/
├── index.ts          # Main application file
├── package.json      # Dependencies and scripts
├── tsconfig.json     # TypeScript configuration
├── build/            # Compiled JavaScript output
│   └── index.js
└── README.md         # This file
```

### Building from Source

1. Make changes to `index.ts`
2. Rebuild the project:
   ```bash
   npm run build
   ```
3. Run the updated version:
   ```bash
   node build/index.js <server_path>
   ```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (required) | - |
| `PORT` | Port for the HTTP server | 3000 |

### TypeScript Configuration

The project uses the following TypeScript configuration:
- Target: ES2022
- Module: Node16
- Strict mode enabled
- Output directory: `./build`

## Dependencies

### Production Dependencies
- `@anthropic-ai/sdk`: Claude AI integration
- `@modelcontextprotocol/sdk`: MCP protocol implementation
- `express`: HTTP server framework
- `cors`: Cross-origin resource sharing
- `dotenv`: Environment variable management

### Development Dependencies
- `typescript`: TypeScript compiler
- `@types/node`: Node.js type definitions
- `@types/express`: Express type definitions
- `@types/cors`: CORS type definitions

## Error Handling

The application includes comprehensive error handling:
- Missing API key validation
- Server connection failures
- Invalid query processing
- Graceful shutdown on SIGINT

## Platform Support

- **Windows**: Uses `py -3.12` for Python servers
- **Unix/Linux/macOS**: Uses `python3.12` for Python servers
- **JavaScript servers**: Uses Node.js on all platforms

## Integration with Finance Mirror

This MCP client is designed to work with the Finance Mirror dashboard by providing AI-powered financial insights and tool interactions. It can be integrated with the main Django application to enhance the user experience with intelligent financial advice.

### Connection to Main Project

```bash
# From the main project directory
cd mcp-client-typescript
npm install
npm run build

# Start the MCP client server
node build/index.js ../mcp-open-banking/main.py
```

## Troubleshooting

### Common Issues

1. **Missing ANTHROPIC_API_KEY**: Ensure your `.env` file contains a valid API key
2. **Python server not found**: Make sure Python 3.12 is installed and accessible
3. **Port already in use**: Change the PORT environment variable or stop other services using port 3000
4. **MCP server connection fails**: Verify the server script path and that the server is compatible with MCP

### Getting Help

- Check the console output for detailed error messages
- Ensure all dependencies are installed with `npm install`
- Verify your MCP server is working independently
- Test the API endpoints with curl or a REST client

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Build and test
5. Submit a pull request

## License

This project is part of the Finance Mirror application and follows the same Apache License 2.0.

## Related Projects

- [Model Context Protocol](https://github.com/modelcontextprotocol)
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-typescript)
- [Finance Mirror Dashboard](../README.md) - Main Django application

---

**Built with ❤️ for the Fibabanka Hackathon**

