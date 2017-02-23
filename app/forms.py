from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class CustomAuthenticationForm(AuthenticationForm):
    """Authentication form."""
    username = forms.CharField(label="Nazwa użytkownika",
                               widget=forms.TextInput({
                                   'placeholder': 'Wpisz nazwę użytkownika'}))
    password = forms.CharField(label="Hasło",
                               widget=forms.PasswordInput({
                                   'placeholder': 'Wpis hasło'}))


class AddGroupForm(forms.Form):
    def validate_upload_grp_ext(value):
        if not value.name.endswith('.grp'):
            raise ValidationError('Złe rozszerzenie pliku.')

    def validate_upload_sem_ext(value):
        if not value.name.endswith('.sem'):
            raise ValidationError('Złe rozszerzenie pliku.')

    upload_grp = forms.FileField(label="Wybierz plik danych z grupą (.grp)", validators=[validate_upload_grp_ext])
    upload_sem = forms.FileField(label="Wybierz plik danych semestru (.sem)", validators=[validate_upload_sem_ext])


class ImportTopicsForm(forms.Form):
    def validate_upload_lst_ext(value):
        if not value.name.endswith('.lst'):
            raise ValidationError('Złe rozszerzenie pliku.')

    upload_topic = forms.FileField(label="Wybierz plik (.lst)", validators=[validate_upload_lst_ext])
