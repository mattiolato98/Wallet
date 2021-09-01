from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, FormView, DetailView, CreateView, UpdateView, DeleteView

from asset_management import coinmarketcap, utils
from asset_management.decorators import more_than_one_portfolio_only
from asset_management.forms import AddAssetCrispyForm, UpdateCurrencyCrispyForm, CreatePortfolioCrispyForm, \
    UpdatePortfolioCrispyForm
from asset_management.models import Asset, UserAsset, Fiat, UserPortfolio

from transaction_management.models import Transaction


class AssetDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'asset_management/asset_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(AssetDashboardView, self).get_context_data(**kwargs)
        if self.request.user.assets.count() > 0:
            context['assets'], context['total_fiat'], context['net'], context['net_percentage'] = \
                utils.user_assets_info(self.request.user)
        return context


class AddAssetView(LoginRequiredMixin, CreateView):
    model = UserAsset
    template_name = 'asset_management/add_asset.html'
    form_class = AddAssetCrispyForm
    success_url = reverse_lazy('asset_management:asset-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.pk
        if self.request.user.portfolios.count() == 1:
            self.object.portfolio_id = self.request.user.portfolios.first().pk
        self.object.save()
        return super(AddAssetView, self).form_valid(form)


class AssetDetailView(LoginRequiredMixin, DetailView):
    template_name = "asset_management/asset_detail.html"
    model = Asset

    def get_context_data(self, **kwargs):
        context = super(AssetDetailView, self).get_context_data(**kwargs)
        cmc_ids = self.request.user.assets_ids

        asset = Asset.objects.get(pk=self.kwargs['pk'])
        user_asset = UserAsset.objects.get(user=self.request.user, asset=asset)
        fiat_symbol = self.request.user.fiat.symbol
        quotes = coinmarketcap.asset_quotes(cmc_ids, fiat_symbol)

        context['max_supply'] = quotes[f'{asset.cmc_id}']['max_supply']
        context['circulating_supply'] = quotes[f'{asset.cmc_id}']['circulating_supply']
        context['circulating_percentage'] = (context['circulating_supply'] * 100) / context['max_supply'] \
            if context['max_supply'] is not None else None
        context['market_cap'] = quotes[f'{asset.cmc_id}']['quote'][fiat_symbol]['market_cap']
        context['price'] = quotes[f'{asset.cmc_id}']['quote'][fiat_symbol]['price']
        context['fiat'] = quotes[f'{asset.cmc_id}']['quote'][fiat_symbol]['price'] * user_asset.amount
        context['user_asset'] = user_asset

        total_fiat = sum(
            quotes[f'{user_asset_obj.asset.cmc_id}']['quote'][fiat_symbol]['price'] * user_asset_obj.amount
            for user_asset_obj in self.request.user.asset_relations.all())

        context['percentage'] = (context['fiat'] * 100) / total_fiat if total_fiat != 0 else 0

        context['net'], context['net_percentage'] = utils.net_calc(
            context['fiat'], user_asset.net_volume, user_asset.buy_volume)

        # context['net'] = user_asset.sell_volume - user_asset.buy_volume + context['fiat']
        # context['net_percentage'] = ((context['net'] * 100) / abs(user_asset.buy_volume - user_asset.sell_volume)) \
        #     if user_asset.buy_volume - user_asset.sell_volume != 0 else 0
        # context['net_percentage'] = (((user_asset.sell_volume + context['fiat']) * 100) / user_asset.buy_volume)
        # - 100 if user_asset.buy_volume != 0 else 0

        context['transactions'] = (Transaction.objects.filter(buy__in=user_asset.buys.all()) |
                                   Transaction.objects.filter(sell__in=user_asset.sells.all()))

        return context


class AssetListUpdate(LoginRequiredMixin, TemplateView):
    template_name = "asset_management/asset_list_update.html"


class CurrencyUpdateView(LoginRequiredMixin, FormView):
    template_name = "asset_management/update_currency.html"
    form_class = UpdateCurrencyCrispyForm
    success_url = reverse_lazy('user_management:user-settings')

    def form_valid(self, form):
        cmc_id = form.cleaned_data['fiat']

        if not Fiat.objects.filter(cmc_id=cmc_id).exists():
            fiat_list = coinmarketcap.fiat_list()
            fiat_list = {element['id']: f"{element['name'], element['symbol'], element['sign']}"
                         for element in fiat_list}
            metadata = fiat_list[int(cmc_id)]
            name, symbol, sign = metadata.split('(')[1].split(')')[0].split(',')
            name, symbol, sign = name.split("'")[1], symbol.split("'")[1], sign.split("'")[1]

            fiat = Fiat(
                cmc_id=cmc_id,
                name=name,
                symbol=symbol,
                sign=sign
            )
            fiat.save()
        else:
            fiat = Fiat.objects.get(cmc_id=cmc_id)

        self.request.user.fiat = fiat
        self.request.user.save()

        return super(CurrencyUpdateView, self).form_valid(form)


class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = UserPortfolio
    template_name = 'asset_management/create_portfolio.html'
    form_class = CreatePortfolioCrispyForm
    success_url = reverse_lazy('asset_management:asset-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.pk
        self.object.save()
        return super(PortfolioCreateView, self).form_valid(form)


@method_decorator([login_required, more_than_one_portfolio_only], name='dispatch')
class PortfolioUpdateView(UpdateView):
    model = UserPortfolio
    template_name = 'asset_management/update_portfolio.html'
    form_class = UpdatePortfolioCrispyForm
    context_object_name = 'portfolio'

    def get_object(self, queryset=None):
        return UserPortfolio.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('asset_management:portfolio-detail', kwargs={'pk': self.kwargs['pk']})


@method_decorator([login_required, more_than_one_portfolio_only], name='dispatch')
class PortfolioDeleteView(DeleteView):
    model = UserPortfolio
    template_name = 'asset_management/delete_portfolio.html'
    context_object_name = 'portfolio'

    def get_object(self, queryset=None):
        return UserPortfolio.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('asset_management:asset-list')


@method_decorator([login_required, more_than_one_portfolio_only], name='dispatch')
class PortfolioDetailView(TemplateView):
    template_name = "asset_management/portfolio_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PortfolioDetailView, self).get_context_data(**kwargs)
        portfolio = UserPortfolio.objects.get(pk=self.kwargs['pk'])
        context['portfolio'] = portfolio
        if portfolio.assets_count > 0:
            context['assets'], context['total_fiat'], context['net'], context['net_percentage'] = \
                utils.portfolio_assets_info(UserPortfolio.objects.get(pk=self.kwargs['pk']))
        return context


@method_decorator([login_required, more_than_one_portfolio_only], name='dispatch')
class PortfolioAssetUpdate(TemplateView):
    template_name = 'asset_management/portfolio_asset_update.html'

    def get_context_data(self, **kwargs):
        context = super(PortfolioAssetUpdate, self).get_context_data(**kwargs)
        context['portfolio'] = UserPortfolio.objects.get(pk=self.kwargs['pk'])
        context['portfolios'] = self.request.user.portfolios.all().exclude(pk=context['portfolio'].pk)
        return context


@login_required
@require_POST
@csrf_protect
def ajax_delete_asset(request):
    asset_id = request.POST.get('asset_pk')
    UserAsset.objects.get(user=request.user, asset_id=asset_id).delete()

    return JsonResponse({
        'status': 'deleted'
    })


@login_required
@require_POST
@csrf_protect
def ajax_move_asset(request):
    asset_id = request.POST.get('asset_pk')
    move_to = request.POST.get('move_to')

    portfolio = UserPortfolio.objects.get(pk=move_to)
    user_asset = UserAsset.objects.get(user=request.user, asset_id=asset_id)

    user_asset.portfolio = portfolio
    user_asset.save()

    return JsonResponse({
        'status': 'moved'
    })
