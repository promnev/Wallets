from django.urls import path

from .views import TransactionAPIView

urlpatterns = [
    path("", TransactionAPIView.as_view({"get": "list", "post": "create"})),
    path("<int:id>/", TransactionAPIView.as_view({"get": "retrieve"})),
    # path("<str:sender>/", TransactionAPIView.as_view({"get": "retrieve"}))
]
