from model_objects import SpecialOfferType


def test_discount_not_fulfilled(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 1)
    make_offer('test-product-1', SpecialOfferType.THREE_FOR_TWO, None)

    handle_offers()

    assert len(receipt.discounts) == 0
    assert receipt.total_price() == 20


def test_offer_description(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 3)
    make_offer('test-product-1', SpecialOfferType.THREE_FOR_TWO, None)

    handle_offers()

    assert receipt.discounts[0].description == '3 for 2'


def test_offer_fulfilled(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 3)
    make_offer('test-product-1', SpecialOfferType.THREE_FOR_TWO, None)

    handle_offers()

    assert len(receipt.discounts) == 1
    assert receipt.total_price() == 40


def test_offer_fulfilled_with_remainder(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 5)
    make_offer('test-product-1', SpecialOfferType.THREE_FOR_TWO, None)

    handle_offers()

    assert receipt.total_price() == 80


def test_offer_fulfilled_more_than_once(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 15, 20)
    make_offer('test-product-1', SpecialOfferType.THREE_FOR_TWO, None)

    handle_offers()

    assert receipt.total_price() == 210
