from django.urls import path

from asset_management import views

app_name = 'asset_management'

urlpatterns = [
    path('list', views.AssetDashboardView.as_view(), name='asset-list'),
    path('add', views.AddAssetView.as_view(), name='asset-add'),
    path('detail/<int:pk>', views.AssetDetailView.as_view(), name='asset-detail'),
    path('list/update', views.AssetListUpdate.as_view(), name='asset-list-update'),
    path('currency/update', views.CurrencyUpdateView.as_view(), name='currency-update'),
    path('portfolio/create', views.PortfolioCreateView.as_view(), name='create-portfolio'),
    path('portfolio/<int:pk>/update', views.PortfolioUpdateView.as_view(), name='update-portfolio'),
    path('portfolio/<int:pk>/delete', views.PortfolioDeleteView.as_view(), name='delete-portfolio'),
    path('portfolio/<int:pk>/detail', views.PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('portfolio/<int:pk>/asset/update', views.PortfolioAssetUpdate.as_view(), name='portfolio-asset-update'),
    path('ajax-delete-asset', views.ajax_delete_asset, name='ajax-delete-asset'),
    path('ajax-move-asset', views.ajax_move_asset, name='ajax-move-asset'),
]