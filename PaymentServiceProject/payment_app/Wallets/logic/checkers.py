import environ
from payment_app.Wallets.models import Wallet

env = environ.Env()


def user_wallets_count_checker(request_user):
    if Wallet.objects.filter(user=request_user).count() >= float(
        env("MAX_WALLETS_PER_USER")
    ):
        return False
    return True
