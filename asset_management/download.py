import time

from asset_management import coinmarketcap, nomics
from asset_management.models import Tag, Url, Asset


def download_all_assets():
    cmc_ids = [asset['id'] for asset in coinmarketcap.asset_list()]
    a, b = cmc_ids[:1000], cmc_ids[1000:]
    c, d = b[:1000], b[1000:]
    e, f = d[:1000], d[1000:]
    g, h = f[:1000], f[1000:]
    first_metadata = coinmarketcap.multi_asset_metadata(a)
    second_metadata = coinmarketcap.multi_asset_metadata(c)
    third_metadata = coinmarketcap.multi_asset_metadata(e)
    fourth_metadata = coinmarketcap.multi_asset_metadata(g)
    fifth_metadata = coinmarketcap.multi_asset_metadata(h)

    for metadata in (first_metadata, second_metadata, third_metadata, fourth_metadata, fifth_metadata):
        for asset in metadata.values():
            cmc_id = asset['id']
            error_ids = [366, 263, 764, 918]
            if not Asset.objects.filter(cmc_id=cmc_id).exists() and cmc_id not in error_ids:
                print(f"{cmc_id} {asset['name']} NON TROVATO")
                description, logo = nomics.asset_metadata(asset['symbol'])
                if description is not None and logo is not None:
                    asset_obj = Asset(
                        cmc_id=cmc_id,
                        logo=logo,
                        name=asset['name'],
                        symbol=asset['symbol'],
                        slug=asset['slug'],
                        description=description,
                        category=asset['category'],
                    )
                    asset_obj.save()
                    for name, urls in asset['urls'].items():
                        for url in urls:
                            url_obj = Url(
                                value=url,
                                description=name,
                                asset=asset_obj,
                            )
                            url_obj.save()

                    if asset['tags'] is not None:
                        for tag in asset['tags']:
                            if not Tag.objects.filter(name=tag).exists():
                                tag_obj = Tag(
                                    name=tag,
                                )
                                tag_obj.save()
                            else:
                                tag_obj = Tag.objects.get(name=tag)
                            asset_obj.tags.add(tag_obj)
                time.sleep(1.1)
                print("FINITO\n")


def fill_empty_description():
    cmc_ids = [asset.cmc_id for asset in Asset.objects.all()]
    a, b = cmc_ids[:1000], cmc_ids[1000:]
    c, d = b[:1000], b[1000:]
    e, f = d[:1000], d[1000:]
    first_metadata = coinmarketcap.multi_asset_metadata(a)
    second_metadata = coinmarketcap.multi_asset_metadata(c)
    third_metadata = coinmarketcap.multi_asset_metadata(e)
    fourth_metadata = coinmarketcap.multi_asset_metadata(f)

    for metadata in (first_metadata, second_metadata, third_metadata, fourth_metadata):
        for asset in metadata.values():
            asset_obj = Asset.objects.get(cmc_id=asset['id'])
            if asset_obj.description == "":
                asset_obj.description = asset['description']


def count_empty_description():
    # 1478
    count = 0
    for asset in Asset.objects.all():
        if asset.description == "":
            count += 1

    print(count)
