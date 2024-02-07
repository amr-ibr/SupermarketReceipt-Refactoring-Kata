import pytest

from model_objects import Product, ProductUnit


def test_checkout_empty_cart(cart, teller):
    receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == 0


def test_checkout_item_not_in_catalog(cart, teller):
    cart.add_item(Product('test-product-4', ProductUnit.EACH))
    with pytest.raises(KeyError):
        teller.checks_out_articles_from(cart)


def test_checkout_single_item_with_no_discount(cart, teller, make_cart_item):
    make_cart_item("test-product-1", 12.3, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == 24.6


def test_checkout_single_item_with_multiple_quantity(cart, teller, make_cart_item):
    make_cart_item("test-product-1", 5, 7)

    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == 35


def test_checkout_multiple_items(cart, teller, make_cart_item):
    make_cart_item("test-product-1", 5, 1)
    make_cart_item("test-product-2", 10, 2)
    make_cart_item("test-product-3", 25, 1)

    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == 50
