from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control form-control-user',
                                                             }))
    password = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control form-control-user',
                                                                }))
    #remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password']

##---------------------------------------------------------------------------------------------------------------
class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control form-control-user',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control form-control-user',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control form-control-user',
                                                             }))
    mobile = forms.CharField(max_length=10,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Mobile',
                                                             'class': 'form-control form-control-user',
                                                             }))
    email = forms.EmailField(required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control form-control-user',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control form-control-user',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control form-control-user',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile','username', 'password1', 'password2', 'email']
##---------------------------------------------------------------------------------------------------------------
class ProfileForm(UserChangeForm):
    password = None
    password1 = None
    password2 = None
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control form-control-user',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control form-control-user',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control form-control-user',
                                                             }))
    mobile = forms.CharField(max_length=10,
                               required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Mobile',
                                                             'class': 'form-control form-control-user',
                                                             }))
    email = forms.EmailField(required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control form-control-user',
                                                           }))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile','username', 'email']
#---------------------------------------------------------------------------------------------------------
