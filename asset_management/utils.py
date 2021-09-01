from asset_management import coinmarketcap
from asset_management.models import Asset, UserAsset


def assets_info(cmc_ids, fiat_symbol, user):
    assets = coinmarketcap.asset_prices(cmc_ids, fiat_symbol)
    for asset in assets:
        asset['object'] = Asset.objects.get(cmc_id=asset['id'])
        user_asset = UserAsset.objects.get(user=user, asset=asset['object'])
        asset['fiat'], asset['net_percentage'] = user_asset_info(asset['price'], user_asset)

    assets = sorted(assets, key=lambda element: element['fiat'], reverse=True)
    total_fiat = sum(asset['fiat'] for asset in assets)

    return assets, total_fiat


def net_calc(fiat, net_volume, buy_volume):
    net = net_volume + fiat

    if fiat == 0:
        net_percentage = ((net * 100) / buy_volume) if buy_volume != 0 else 0
    else:
        net_percentage = ((net * 100) / abs(net_volume)) if net_volume != 0 else 0

    return net, net_percentage


def portfolio_assets_info(portfolio):
    cmc_ids = portfolio.assets_ids
    fiat_symbol = portfolio.user.fiat.symbol

    assets, total_fiat = assets_info(cmc_ids, fiat_symbol, portfolio.user)
    net, net_percentage = net_calc(total_fiat, portfolio.net_volume, portfolio.buy_volume)

    return assets, total_fiat, net, net_percentage


def user_assets_info(user):
    cmc_ids = user.assets_ids
    fiat_symbol = user.fiat.symbol

    assets, total_fiat = assets_info(cmc_ids, fiat_symbol, user)
    net, net_percentage = net_calc(total_fiat, user.net_volume, user.buy_volume)

    return assets, total_fiat, net, net_percentage


def user_asset_info(asset_price, user_asset):
    fiat = asset_price * user_asset.amount
    net, net_percentage = net_calc(fiat, user_asset.net_volume, user_asset.buy_volume)

    return fiat, net_percentage
