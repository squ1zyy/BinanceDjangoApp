from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from currency_main.get_coin import get_coin

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш никнейм'}))
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя:", widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Введите ваш никнейм'}))
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={"class": 'form-control', 'placeholder': 'Введите пароль'}))

class EmailNotificationForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

class CurrencyConverterForm(forms.Form):
    amount = forms.DecimalField(initial=1)
    conversion_type = forms.ChoiceField(choices=[
        ('coin_to_usd', 'Coin to USD'),
        ('usd_to_coin', 'USD to Coin'),
    ])

class ApiForm(forms.Form):
    name = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Введите ваш никнейм'}))
    api_key = forms.CharField(max_length=32, required=True, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Введите ваш api_key'}))
    secret_key = forms.CharField(max_length=32, required=True, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Введите ваш secret_key'}))

class EditForm(forms.Form):
    name = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Введите ваш новый никнейм'}))
    api_key = forms.CharField(max_length=32, required=True, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Введите ваш новый api_key'}))
    secret_key = forms.CharField(max_length=32, required=True, widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Введите ваш новый secret_key'}))

class BuyForm(forms.Form):
    buy_coin = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={"class": 'form-field', 'id': 'amount', 'placeholder': 'Amount'}),
    )
    
    sell_usdt = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={"class": 'form-field', 'id': 'price', 'placeholder': 'Price'}),
    )
    
    avg_price_coin = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={"class": 'form-field', 'id': 'total', 'placeholder': 'Total'}),
    )
