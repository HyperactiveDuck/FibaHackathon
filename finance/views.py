from django.shortcuts import render

def dashboard(request):
    return render(request, 'finance/dashboard.html')

def accounts(request):
    return render(request, 'finance/accounts.html')

def transactions(request):
    return render(request, 'finance/transactions.html')

def budgets(request):
    return render(request, 'finance/budgets.html')

def analytics(request):
    return render(request, 'finance/analytics.html')

def settings(request):
    return render(request, 'finance/settings.html')