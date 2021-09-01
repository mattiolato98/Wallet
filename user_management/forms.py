from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from asset_management import coinmarketcap
from asset_management.models import Fiat
from user_management.models import Profile


class LoginForm(AuthenticationForm):
    helper = FormHelper()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


class PlatformUserCreationForm(UserCreationForm):
    helper = FormHelper()
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = None

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Ripeti la password'})

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class CreateProfileCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'create-profile-crispy-form'
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'light-input-full'})
        self.fields['last_name'].widget.attrs.update({'class': 'light-input-full'})

        self.helper.layout = Layout(
            Row(
              Column('picture', css_class='form-group mb-3'),
              css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group mb-0'),
                Column('last_name', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group mb-0'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = Profile
        fields = (
            'picture',
            'first_name',
            'last_name',
        )
        labels = {
            'picture': 'Immagine del profilo',
            'first_name': 'Nome',
            'last_name': 'Cognome',
        }


class UpdateProfileCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'update-profile-crispy-form'
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'light-input-full'})
        self.fields['last_name'].widget.attrs.update({'class': 'light-input-full'})

        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group mb-0'),
                Column('last_name', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group mb-0'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
        )
        labels = {
            'first_name': 'Nome',
            'last_name': 'Cognome',
        }


class UpdateProfilePictureCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'update-profile-picture-crispy-form'
    helper.form_method = 'POST'

    class Meta:
        model = Profile
        fields = 'picture',
        labels = {'picture': 'Immagine del profilo'}

