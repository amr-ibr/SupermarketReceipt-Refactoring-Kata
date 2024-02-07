from model_objects import SpecialOfferType


def test_offer_description(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 5)
    make_offer('test-product-1', SpecialOfferType.TEN_PERCENT_DISCOUNT, 10)

    handle_offers()

    assert receipt.discounts[0].description == '10% off'


def test_offer_fulfilled_on_single_item(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 1)
    make_offer('test-product-1', SpecialOfferType.TEN_PERCENT_DISCOUNT, 10)

    handle_offers()

    assert len(receipt.discounts) == 1
    assert receipt.total_price() == 18


def test_offer_fulfilled_on_multiple_items(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 2)
    make_offer('test-product-1', SpecialOfferType.TEN_PERCENT_DISCOUNT, 10)

    handle_offers()

    assert len(receipt.discounts) == 1
    assert receipt.total_price() == 36
