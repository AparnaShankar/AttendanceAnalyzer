from django import forms

class NameForm(forms.Form):
    faculty_id = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Faculty ID','class': 'login-input'}),max_length=20,initial="")
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'login-input'}),max_length=20,initial="")
