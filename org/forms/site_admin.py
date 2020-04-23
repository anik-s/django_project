from django import forms


class SiteAdminForm(forms.Form):
    email = forms.EmailField(label='Email*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username*', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=8,
                               label="Password",
                               strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
                               )
