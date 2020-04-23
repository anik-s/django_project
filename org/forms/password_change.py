from django import forms


class PasswordChangeForm(forms.Form):
    password = forms.CharField(min_length=8,
                               label="New Password*",
                               strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
                               )
