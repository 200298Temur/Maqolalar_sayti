from django.contrib.auth.forms  import AuthenticationForm,UserCreationForm
from django import forms 
from django.contrib.auth import get_user_model

class LoginUserForm(AuthenticationForm):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={"class":'form-input'}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-input"}))

    class Meta:
        model=get_user_model()
        fields=['username','password']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Parol", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Parol", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Bu E-pochta allaqachon mavjud!")
        return email
    
class ProfileUserForm(forms.ModelForm):
    username=forms.CharField(disabled=True,label="Login",widget=forms.TextInput(attrs={'class':"form-input"}))
    email=forms.CharField(disabled=True,label="Email",widget=forms.TextInput(attrs={'class':"form-input"}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

