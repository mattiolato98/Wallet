from django.urls import path

from transaction_management import views

app_name = 'transaction_management'

urlpatterns = [
    path('add/<int:pk>', views.AddTransactionView.as_view(), name="add-transaction"),
    path('update/<int:pk>/<int:asset_pk>', views.UpdateTransactionView.as_view(), name="update-transaction"),
    path('delete/<int:pk>/<int:asset_pk>', views.DeleteTransactionView.as_view(), name="delete-transaction"),
]