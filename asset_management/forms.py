from crispy_forms.helper import FormHelper
from django import forms

from asset_management import coinmarketcap
from asset_management.models import Asset, UserAsset, UserPortfolio


class AddAssetCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'add-asset-crispy-form'
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddAssetCrispyForm, self).__init__(*args, **kwargs)

        self.fields['asset'].queryset = Asset.objects.exclude(cmc_id__in=self.user.assets_ids)
        if self.user.portfolios.count() == 1:
            self.fields.pop('portfolio')
        else:
            self.fields['portfolio'].queryset = self.user.portfolios

    class Meta:
        model = UserAsset
        fields = ['asset', 'portfolio']
        widgets = {
            'asset': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                         'data-dropdown-align-right': 'true'}),
            'portfolio': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                             'data-dropdown-align-right': 'true'})
        }


class UpdateCurrencyCrispyForm(forms.Form):
    helper = FormHelper()
    helper.form_id = 'update-currency-crispy-form'
    helper.form_method = 'POST'

    fiat = forms.ChoiceField(choices=[(fiat['id'], f"{fiat['name']}")
                                      for fiat in coinmarketcap.fiat_list()],
                             widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true',
                                                        'data-dropdown-align-right': 'true'}))


class PortfolioCrispyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'placeholder': 'Nome', 'class': 'light-input-full'})

    class Meta:
        model = UserPortfolio
        fields = ['name']
        labels = {'name': 'Nome', }


class CreatePortfolioCrispyForm(PortfolioCrispyForm):
    helper = FormHelper()
    helper.form_id = 'create-portfolio-crispy-form'
    helper.form_method = 'POST'

    class Meta:
        model = UserPortfolio
        fields = ['name']
        labels = {'name': '', }


class UpdatePortfolioCrispyForm(PortfolioCrispyForm):
    helper = FormHelper()
    helper.form_id = 'update-portfolio-crispy-form'
    helper.form_method = 'POST'
