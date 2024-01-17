from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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
