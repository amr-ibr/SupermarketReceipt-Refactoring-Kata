import pytest

from model_objects import Discount


def test_no_items(receipt):
    assert receipt.items == []
    assert receipt.total_price() == 0
    assert receipt.discounts == []


@pytest.mark.skip("Not implemented yet")
def test_add_product_quantity_cant_be_zero(receipt):
    with pytest.raises(ValueError):
        receipt.add_product('test_product', 0, 1, 1)


@pytest.mark.skip("Not implemented yet")
def test_add_product_quantity_cant_be_less_than_zero(receipt):
    with pytest.raises(ValueError):
        receipt.add_product('test_product', -10, 1, 1)


def test_single_item_and_no_discount(receipt):
    receipt.add_product('test_product', 1, 1, 1)
    assert receipt.total_price() == 1


@pytest.mark.skip("Not implemented yet")
def test_total_price_cant_be_less_than_zero_when_a_higher_discount_applied(receipt):
    discount = Discount('test_product', 'test_product_desc', -2)
    receipt.add_product('test_product', 1, 1, 1)
    receipt.add_discount(discount)
    assert pytest.approx(receipt.total_price()) == 0


def test_multiple_items_with_no_discount(receipt):
    receipt.add_product('test_product_1', 2, 1.75, 3.5)
    receipt.add_product('test_product_2', 1, 10, 10)

    assert pytest.approx(receipt.total_price()) == 13.5


def test_multiple_product_with_single_discount(receipt):
    receipt.add_product('test_product_1', 2, 1.75, 3.5)
    receipt.add_product('test_product_2', 1, 10, 10)

    discount = Discount('test_product', 'test_product_desc', -2.1)
    receipt.add_discount(discount)

    assert pytest.approx(receipt.total_price()) == 11.4


def test_multiple_products_with_multiple_discounts(receipt):
    receipt.add_product('test_product_1', 2, 1.75, 3.5)
    receipt.add_product('test_product_2', 1, 10, 10)

    test_discount_1 = Discount('test_product_1', 'test_product_1_desc', -2.1)
    test_discount_2 = Discount('test_product_2', 'test_product_2_desc', -10)

    receipt.add_discount(test_discount_1)
    receipt.add_discount(test_discount_2)

    assert pytest.approx(receipt.total_price(), 0.01) == 1.40
