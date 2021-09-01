from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, DeleteView

from asset_management.models import Asset, UserAsset
from transaction_management.forms import AddTransactionCrispyForm, UpdateTransactionCrispyForm
from transaction_management.models import Buy, Sell, Transaction


class AddTransactionView(LoginRequiredMixin, FormView):
    template_name = "transaction_management/add_transaction.html"
    form_class = AddTransactionCrispyForm

    def get_context_data(self, **kwargs):
        context = super(AddTransactionView, self).get_context_data(**kwargs)
        context['asset'] = Asset.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        user_asset = UserAsset.objects.get(user=self.request.user, asset=Asset.objects.get(pk=self.kwargs['pk']))

        if form.cleaned_data['type'] == 'buy':
            transaction = Buy(
                amount=form.cleaned_data['amount'],
                price=form.cleaned_data['price'],
                fee=form.cleaned_data['fee'],
                date=form.cleaned_data['date'],
                user_asset=user_asset,
            )
        else:
            transaction = Sell(
                amount=form.cleaned_data['amount'],
                price=form.cleaned_data['price'],
                fee=form.cleaned_data['fee'],
                date=form.cleaned_data['date'],
                user_asset=user_asset,
            )

        transaction.save()
        return super(AddTransactionView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('asset_management:asset-detail', kwargs={'pk': self.kwargs['pk']})


class UpdateTransactionView(LoginRequiredMixin, UpdateView):
    template_name = "transaction_management/update_transaction.html"
    form_class = UpdateTransactionCrispyForm

    def get_object(self, queryset=None):
        return Transaction.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(UpdateTransactionView, self).get_context_data(**kwargs)
        context['asset'] = Asset.objects.get(pk=self.kwargs['asset_pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('asset_management:asset-detail', kwargs={'pk': self.kwargs['asset_pk']})


class DeleteTransactionView(LoginRequiredMixin, DeleteView):
    template_name = "transaction_management/delete_transaction.html"
    model = Transaction

    def get_object(self, queryset=None):
        return Transaction.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DeleteTransactionView, self).get_context_data(**kwargs)
        context['asset'] = Asset.objects.get(pk=self.kwargs['asset_pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('asset_management:asset-detail', kwargs={'pk': self.kwargs['asset_pk']})