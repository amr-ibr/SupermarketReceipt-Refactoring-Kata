import pytest

from model_objects import SpecialOfferType


def test_offer_not_fulfilled(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 1)
    make_offer('test-product-1', SpecialOfferType.TWO_FOR_AMOUNT, 10)
    handle_offers()
    assert len(receipt.discounts) == 0
    assert receipt.total_price() == 20


def test_offer_description(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 2)
    make_offer('test-product-1', SpecialOfferType.TWO_FOR_AMOUNT, 30)

    handle_offers()

    assert receipt.discounts[0].description == '2 for 30'


def test_offer_fulfilled(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 2)
    make_offer('test-product-1', SpecialOfferType.TWO_FOR_AMOUNT, 26.99)
    handle_offers()
    assert len(receipt.discounts) == 1
    assert pytest.approx(receipt.total_price(), 0.01) == 26.99


@pytest.mark.skip()
def test_offer_fulfilled_with_remainder(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 3)
    make_offer('test-product-1', SpecialOfferType.TWO_FOR_AMOUNT, 30)

    handle_offers()

    assert receipt.total_price() == 50


def test_offer_fulfilled_more_than_once(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 15, 20)
    make_offer('test-product-1', SpecialOfferType.TWO_FOR_AMOUNT, 25)

    handle_offers()

    assert receipt.total_price() == 250
