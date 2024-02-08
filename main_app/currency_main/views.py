from django.shortcuts import render, redirect
from binance.client import Client
from currency_main.forms import UserRegisterForm, UserLoginForm, CurrencyConverterForm, ApiForm, EditForm, BuyForm
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.utils.encoding import force_str, force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from currency_main.token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import *
from binance.exceptions import BinanceAPIException
from decimal import Decimal
from django.http import JsonResponse

client = Client()

additional_symbols = ['ETHUSDT', 'XRPUSDT', 'LTCUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'LINKUSDT', 'DOTUSDT', 'UNIUSDT', 'SOLUSDT']

def update_binance_data(request):
    data = []

    for symbol in ['BTCUSDT'] + additional_symbols:
        try:
            ticker_stats = client.get_ticker(symbol=symbol)
            
            ticker_price = ticker_stats['lastPrice']
            ticker_percentage = ticker_stats['priceChangePercent']
            ticker_volume = ticker_stats['volume']
            ticker_high = ticker_stats['highPrice'] 
            ticker_low = ticker_stats['lowPrice']

            crypto_data = {
                'symbol': symbol,
                'price': ticker_price,
                'percentage': ticker_percentage,
                'volume': ticker_volume,
                'high': ticker_high,
                'low': ticker_low,
            }

            data.append(crypto_data)

        except Exception as e:
            crypto_data = {
                'symbol': symbol,
                'error': f"Error fetching data: {e}",
            }
            data.append(crypto_data)

    context = {
        'crypto_data': data,
    }

    return render(request, 'main-page.html', context)

def main_page(request):
    return update_binance_data(request)

def currency_converter(request):
    coin = request.GET.get('coin', default='BTCUSDT')
    ticker = client.get_ticker(symbol=coin)
    last_price = Decimal(str(ticker['lastPrice']))
    formatted_last_price = "{:,.2f}".format(last_price)

    if request.method == 'POST': 
        form = BuyForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['buy_coin']
            price = form.cleaned_data['sell_usdt']

            converted_amount = Decimal(amount) / last_price
            converted_total = Decimal(amount) * last_price

            return render(request, 'graphics.html', {
                'form': form,
                'amount': amount,
                'converted_amount': converted_amount,
                'converted_total': converted_total,
                'coin': coin,
                'price': price,
                'total': converted_total,
            })
    else:
        form = BuyForm()

    return render(request, 'graphics.html', {'form': form, 'coin': coin, 'ticker': ticker, 'last_price': formatted_last_price})

def last_price(request):
    coin = request.GET.get('coin', default='BTCUSDT')
    ticker = client.get_ticker(symbol=coin)
    last_price = Decimal(str(ticker['lastPrice']))
    formatted_last_price = "{:,.2f}".format(last_price)

    # Возвращаем только цену монеты в формате JSON
    return JsonResponse({'last_price': formatted_last_price})

# def trade_view(request):
#     if request.method == 'POST': 
#         form = BuyForm(request.POST)
#     else:
#         form = BuyForm()
#     return render(request, 'graphics.html', {'form': form})

def profile(request):
    get_api_data = UserApiData.objects.all()
    if request.method == 'POST':
        form = ApiForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            api_key = form.cleaned_data['api_key']
            secret_key = form.cleaned_data['secret_key']

            profile_data = UserApiData.objects.create(
                name=name,
                api_key=api_key,
                secret_key=secret_key,
            )
            return redirect('profile')
        else:
            return '404'
    else:
        form = ApiForm()
    return render(request, 'profile.html', {'form': form, 'profile_data': get_api_data})

def delete(request, id):
    model = UserApiData.objects.get(pk=id)
    model.delete()
    return redirect('profile')

def edit(request, id):
    model = UserApiData.objects.get(pk=id)
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            model.name = form.cleaned_data['name']
            model.api_key = form.cleaned_data['api_key']
            model.secret_key = form.cleaned_data['secret_key']
            model.save()
            return redirect('profile')
    else:
        form = EditForm(instance=model)

    return render(request, 'edit.html', {'form': form, 'model': model})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            api_key = form.cleaned_data['first_name']
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, 'Такая почта уже существует!')
            elif User.objects.filter(first_name__iexact=api_key).exists():
                messages.error(request, 'Такой апи ключ уже существует!')
            else:
                user = form.save()
                auth_login(request, user)
                activateEmail(request, user, form.cleaned_data.get('email'))
                return redirect('main-page')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    return render(request, 'registration/reg.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('main-page')
    else:
        form = UserLoginForm()
    return render(request, 'registration/log.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('main-page')


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('acc_active_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        succes_message = f'Дорогой {user}, пожалуйста перейдите на вашу электронную почту {to_email} входящие и нажмите \ получена ссылка активации для подтверждения и завершения регистрации. Примечание: Посмотрите папку спам.'
        messages.success(request, succes_message)
    else:
        error_message = f'Проблема с отправкой письма с подтверждением на {to_email}, посмотрите всели вы написали коректно.'
        messages.error(request, error_message)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Спасибо за ваше подтверждение почты. Сейчас можете зайти в свой аккаунт.')
        return redirect('login')
    else:
        messages.error(request, 'Ссылка не коректна!')

    return redirect('main-page')