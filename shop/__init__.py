from shop.gift import Gift
from shop.pandora import PandoraBox
from shop.air import Air
from shop.hamster_coin import HamsterCoin
from shop.mcdonalds_box import MacDonaldsBox
from shop.promo_welcome import PromoWelcome
from shop.promo_empty import PromoEmpty
from shop.shotgun import Shotgun

gifts: list[Gift] = [PandoraBox(), HamsterCoin(), MacDonaldsBox(), Shotgun()]

promos: dict[str, Gift] = {
    "#welcome": PromoWelcome(),
    "#": PromoEmpty(),
}
