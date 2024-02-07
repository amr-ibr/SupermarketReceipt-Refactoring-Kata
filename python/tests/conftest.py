import approvaltests
import pytest
from approvaltests.reporters import PythonNativeReporter

from model_objects import Offer, Product, ProductUnit
from receipt import Receipt
from shopping_cart import ShoppingCart
from teller import Teller

from .fake_catalog import FakeCatalog


@pytest.fixture(scope="session", autouse=True)
def set_default_reporter_for_all_tests():
    approvaltests.set_default_reporter(PythonNativeReporter())


@pytest.fixture()
def catalog():
    yield FakeCatalog()


@pytest.fixture()
def cart():
    yield ShoppingCart()


@pytest.fixture()
def receipt():
    yield Receipt()


@pytest.fixture()
def teller(catalog):
    return Teller(catalog)


@pytest.fixture()
def offers():
    yield {}


@pytest.fixture()
def make_cart_item(catalog, cart, receipt):
    def make(product_name: str, product_price: float, quantity: int):
        product = Product(product_name, ProductUnit.EACH)
        catalog.add_product(product, product_price)
        cart.add_item_quantity(product, quantity)
        receipt.add_product(product, quantity, product_price, product_price * quantity)

    return make


@pytest.fixture()
def make_offer(catalog, offers):
    def make(product_name, offer_type, argument):
        product = catalog.products[product_name]
        offers[product] = Offer(offer_type, catalog, argument)

    return make


@pytest.fixture()
def handle_offers(cart, receipt, catalog, offers):
    def handle():
        cart.handle_offers(receipt, offers, catalog)

    return handle
