from django.urls import path

from .views import TransactionAPIView, TransactionWalletAPIView

urlpatterns = [
    path("", TransactionAPIView.as_view({"get": "list", "post": "create"})),
    path("<int:id>/", TransactionAPIView.as_view({"get": "retrieve"})),
    path(
        "wallet/<str:wallet_name>/",
        TransactionWalletAPIView.as_view({"get": "list"}),
    ),
]
