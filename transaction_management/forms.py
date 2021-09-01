from datetime import datetime

from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field
from django import forms
from django.utils.safestring import mark_safe

from transaction_management.models import Transaction


class TransactionCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'add-transaction-crispy-form'
    helper.form_method = 'POST'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['amount'].widget.attrs.update({'class': 'light-input-full', 'placeholder': 'Quantità',
                                                   'step': 0.00000001})
        self.fields['price'].widget.attrs.update({'class': 'light-input-full', 'placeholder': 'Prezzo'})
        self.fields['fee'].widget.attrs.update({'class': 'light-input-full', 'placeholder': 'Commissioni',
                                                'step': 0.001})
        self.fields['date'].widget.attrs.update({'class': 'light-input-full', 'placeholder': 'Data'})

        self.helper.layout = Layout(
            Row(
                Column(Field(AppendedText(
                    'amount',
                    mark_safe('<span id="asset-amount-input" class="font-5 bg-outline-secondary"></span>'))),
                    css_class='form-group mb-0'),
                Column(Field(AppendedText(
                    'price',
                    mark_safe('<span id="asset-price-input" class="font-5 bg-outline-secondary"></span>'))),
                    css_class='form-group mb-0'),
                Column(Field(AppendedText(
                    'fee',
                    mark_safe('<span class="font-5 bg-outline-secondary">%</span>'))),
                    css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date', css_class='form-group mb-0'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = Transaction
        fields = ['amount', 'price', 'fee', 'date', ]
        labels = {
            'amount': '',
            'price': '',
            'fee': '',
            'date': '',
        }
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'light-input-full',
                                                              'value': datetime.now().strftime("%Y-%m-%d")}),
        }


class AddTransactionCrispyForm(TransactionCrispyForm):
    type = forms.ChoiceField(choices=[('buy', 'Acquisto'), ('sell', 'Vendita')],
                             widget=forms.Select(attrs={'class': 'selectpicker'}), label='')

    def __init__(self, **kwargs):
        super(AddTransactionCrispyForm, self).__init__(**kwargs)

        self.helper.layout = Layout(
            Row(
                Column(Field(AppendedText(
                    'amount',
                    mark_safe('<span id="asset-amount-input" class="font-5 bg-outline-secondary"></span>'))),
                    css_class='form-group mb-0'),
                Column(Field(AppendedText(
                    'price',
                    mark_safe('<span id="asset-price-input" class="font-5 bg-outline-secondary"></span>'))),
                    css_class='form-group mb-0'),
                Column(Field(AppendedText(
                    'fee',
                    mark_safe('<span class="font-5 bg-outline-secondary">%</span>'))),
                    css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date', css_class='form-group mb-0'),
                Column('type', css_class='form-group mb-0'),
                css_class='form-row'
            ),
        )


class UpdateTransactionCrispyForm(TransactionCrispyForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'price', 'fee', 'date', ]
        labels = {
            'amount': 'Quantità',
            'price': 'Prezzo',
            'fee': 'Commissioni',
            'date': 'Data esecuzione',
        }
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'light-input-full',
                                                              'value': datetime.now().strftime("%Y-%m-%d")}),
        }