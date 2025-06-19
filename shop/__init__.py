from shop.gift import Gift
from shop.pandora import PandoraBox
from shop.air import Air
from shop.hamster_coin import HamsterCoin
from shop.mcdonalds_box import MacDonaldsBox
from shop.promo_welcome import PromoWelcome

gifts: list[Gift] = [Air(), PandoraBox(), HamsterCoin(), MacDonaldsBox()]

promos: dict[str, Gift] = {
    "#welcome": PromoWelcome()
}