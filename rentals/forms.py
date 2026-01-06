from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Payment, Property

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=[('tenant', 'Tenant'), ('landlord', 'Landlord')], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'role', 'password1', 'password2')

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method', 'proof_image']
        widgets = {
            'method': forms.Select(attrs={'class': 'form-control'}),
            'proof_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AddPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'address', 'rooms', 'rent', 'deposit', 'photos']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'rent': forms.NumberInput(attrs={'class': 'form-control'}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control'}),
            'photos': forms.FileInput(attrs={'class': 'form-control'}),
        }