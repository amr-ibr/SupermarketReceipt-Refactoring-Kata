import pytest

from model_objects import SpecialOfferType


def test_offer_not_fulfilled(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 3)
    make_offer('test-product-1', SpecialOfferType.FIVE_FOR_AMOUNT, 10)

    handle_offers()

    assert len(receipt.discounts) == 0
    assert receipt.total_price() == 60


def test_offer_description(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 5)
    make_offer('test-product-1', SpecialOfferType.FIVE_FOR_AMOUNT, 55.99)

    handle_offers()

    assert receipt.discounts[0].description == '5 for 55.99'


def test_offer_fulfilled(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 5)
    make_offer('test-product-1', SpecialOfferType.FIVE_FOR_AMOUNT, 55.99)

    handle_offers()

    assert len(receipt.discounts) == 1
    assert pytest.approx(receipt.total_price(), 0.01) == 55.99


def test_offer_fulfilled_with_remainder(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 8)
    make_offer('test-product-1', SpecialOfferType.FIVE_FOR_AMOUNT, 33.55)

    handle_offers()

    assert pytest.approx(receipt.total_price()) == 93.55


def test_offer_fulfilled_more_than_once(
        make_cart_item, make_offer, handle_offers,
        receipt
):
    make_cart_item('test-product-1', 15, 20)
    make_offer('test-product-1', SpecialOfferType.FIVE_FOR_AMOUNT, 27)

    handle_offers()

    assert receipt.total_price() == 108
