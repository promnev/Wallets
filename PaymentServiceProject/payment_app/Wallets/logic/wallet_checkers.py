import environ
from payment_app.Wallets.wallet_models import Wallet

env = environ.Env()


def user_wallets_count_checker(request_user) -> bool:
    """Takes in request_user, checks the number of his wallets, returns whether the user can create a new wallet"""
    if Wallet.objects.filter(user=request_user).count() >= float(
        env("MAX_WALLETS_PER_USER")
    ):
        return False
    return True
