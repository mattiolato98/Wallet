from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, UpdateView

from asset_management import coinmarketcap
from asset_management.models import UserPortfolio
from user_management.decorators import has_not_profile_only, has_profile_only
from user_management.forms import LoginForm, PlatformUserCreationForm, UpdateProfileCrispyForm, \
    UpdateProfilePictureCrispyForm, CreateProfileCrispyForm
from user_management.models import Profile

account_activation_token = PasswordResetTokenGenerator()


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class RegistrationView(CreateView):
    form_class = PlatformUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('user_management:email-verification-needed')

    def form_valid(self, form):
        response = super(RegistrationView, self).form_valid(form)

        mail_subject = _('Wallet, email di conferma account')
        relative_confirm_url = reverse(
            'user_management:verify-user-email',
            args=[
                urlsafe_base64_encode(force_bytes(self.object.pk)),
                account_activation_token.make_token(self.object)
            ]
        )

        self.object.email_user(
            subject=mail_subject,
            message=_(f'''Ciao {self.object.username}, '''
                      + '''ti diamo il benvenuto in Wallet.\n'''
                      + '''\nClicca il seguente link per confermare la tua email:'''
                      + f'''\n{self.request.build_absolute_uri(relative_confirm_url)}\n'''
                      + '''\nA presto, \nil Team di Wallet.''')
        )

        self.object.token_sent = True
        self.object.is_active = False
        self.object.save()

        default_portfolio = UserPortfolio(
            name='Portafoglio principale',
            user=self.object,
        )
        default_portfolio.save()

        return response


def user_login_by_token(request, user_id_b64=None, user_token=None):
    """
    Verifica che il token corrisponda a quello dell'utente che sta cercando di verificare la mail.
    """
    try:
        uid = force_text(urlsafe_base64_decode(user_id_b64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, user_token):
        user.is_active = True
        user.save()
        login(request, user)
        return True

    return False


def verify_user_email(request, user_id_b64=None, user_token=None):
    """
    :return: Pagina di email verificata con successo, se il token corrisponde a quello dell'utente.
    """
    if not user_login_by_token(request, user_id_b64, user_token):
        message = _('Errore. Tentativo di validazione email per l\'utente {user} con token {token}')

    return redirect('user_management:email-verified')


class EmailVerificationNeededView(TemplateView):
    template_name = 'user_management/email_verification_needed.html'


class EmailVerifiedView(LoginRequiredMixin, TemplateView):
    template_name = 'user_management/email_verified.html'


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name = "user_management/user_detail.html"


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "user_management/user_settings.html"


@method_decorator([login_required, has_not_profile_only], name='dispatch')
class ProfileCreateView(CreateView):
    template_name = "user_management/create_profile.html"
    form_class = CreateProfileCrispyForm
    success_url = reverse_lazy('user_management:user-detail')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.pk
        self.object.save()

        return super().form_valid(form)


@method_decorator([login_required, has_profile_only], name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "user_management/update_profile.html"
    form_class = UpdateProfileCrispyForm
    success_url = reverse_lazy('user_management:user-detail')

    def get_object(self, queryset=None):
        return Profile.objects.get(pk=self.request.user.profile.pk)


class ProfilePictureUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "user_management/update_profile_picture.html"
    form_class = UpdateProfilePictureCrispyForm
    success_url = reverse_lazy('user_management:user-detail')

    def get_object(self, queryset=None):
        return Profile.objects.get(pk=self.request.user.profile.pk)


def ajax_check_username_exists(request):
    return JsonResponse({'exists': True}) \
        if get_user_model().objects.filter(username=request.GET.get('username')).exists() \
        else JsonResponse({'exists': False})