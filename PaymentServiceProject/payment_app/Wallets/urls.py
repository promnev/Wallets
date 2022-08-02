from django.urls import path

from .views import WalletAPIView

urlpatterns = [
    path("", WalletAPIView.as_view({"get": "list", "post": "create"})),
    path(
        "<str:name>/",
        WalletAPIView.as_view({"get": "retrieve", "delete": "destroy"}),
    ),
]
