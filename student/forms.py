from django import forms
from .models import Student, Profile
from django.contrib.auth.models import User


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):

    username = forms.CharField( widget=forms.TextInput(attrs={
                 'class':'form-control',
                 'placeholder':'User Name'

                }))
    password = forms.CharField( widget=forms.PasswordInput(attrs={
                 'class':'form-control',
                 'placeholder':'Password'

                }))

class RegisterForm(forms.ModelForm):
    password = forms.CharField( widget=forms.PasswordInput(attrs={
                 'class':'form-control',
                 'placeholder':'Password'

                }))
    role = forms.ChoiceField(
        choices=Profile.Role_CHOICES,
        widget=forms.Select(attrs={
            'class':'form-control'
        })
    )
    class Meta:
        model = User 
        fields = ['username', 'email','password']
    
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {
                'class':'form-control',
                 'placeholder':'User Name'

            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'class':'form-control',
                'placeholder':'Email'

            }
        )
