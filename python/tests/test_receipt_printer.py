import pytest
from approvaltests.approvals import verify

from model_objects import Discount, Product, ProductUnit
from receipt_printer import ReceiptPrinter


@pytest.fixture
def receipt_with_no_items(receipt):
    yield receipt


@pytest.fixture
def receipt_with_single_item(receipt):
    receipt.add_product(Product('test-product-1', ProductUnit.EACH), 1, 12, 12)
    yield receipt


@pytest.fixture
def receipt_with_single_item_multiple_quantity(receipt):
    receipt.add_product(Product('test-product-1', ProductUnit.EACH), 3, 12, 48)
    yield receipt


@pytest.fixture
def receipt_with_multiple_items(receipt):
    receipt.add_product(Product('test-product-1', ProductUnit.EACH), 1, 12.5, 12.5)
    receipt.add_product(Product('test-product-2', ProductUnit.EACH), 3, 12, 36)
    receipt.add_product(Product('test-product-3', ProductUnit.EACH), 1, 12, 12)
    receipt.add_product(Product('test-product-4', ProductUnit.KILO), 2, 12, 24)
    yield receipt


def test_print_receipt_with_no_items(receipt_with_no_items):
    verify(ReceiptPrinter().print_receipt(receipt_with_no_items))


def test_print_receipt_indent_size(receipt_with_single_item):
    verify(ReceiptPrinter(columns=20).print_receipt(receipt_with_single_item))


def test_print_receipt_discount_approximation(receipt_with_no_items):
    product = Product('test-product-1', ProductUnit.EACH)
    discount = Discount(product, 'discount-desc', 3.33333333333333333)

    receipt_with_no_items.add_product(product, 2, 12.33, 12.33)
    receipt_with_no_items.add_discount(discount)

    verify(ReceiptPrinter().print_receipt(receipt_with_no_items))


def test_print_receipt_price_rounding_up(receipt_with_no_items):
    receipt_with_no_items.add_product(Product('test-product-1', ProductUnit.EACH), 1, 12.333333333333221,
                                      12.333333333333221)
    verify(ReceiptPrinter().print_receipt(receipt_with_no_items))


def test_print_receipt_with_single_item(receipt_with_single_item):
    verify(ReceiptPrinter().print_receipt(receipt_with_single_item))


def test_print_receipt_with_single_item_multi_quantities(receipt_with_single_item_multiple_quantity):
    verify(ReceiptPrinter().print_receipt(receipt_with_single_item_multiple_quantity))


def test_print_receipt_with_multi_items(receipt_with_multiple_items):
    verify(ReceiptPrinter().print_receipt(receipt_with_multiple_items))


def test_print_receipt_with_single_discount(receipt_with_multiple_items):
    product = Product('test-product-1', ProductUnit.EACH)
    discount = Discount(product, 'discount', -6)

    receipt_with_multiple_items.add_discount(discount)

    verify(ReceiptPrinter().print_receipt(receipt_with_multiple_items))


def test_print_receipt_with_multiple_discounts(receipt_with_multiple_items):
    test_product_1 = Product('test-product-1', ProductUnit.EACH)
    test_product_2 = Product('test-product-2', ProductUnit.EACH)

    test_discount_1 = Discount(test_product_1, 'test_discount_1', -6)
    test_discount_2 = Discount(test_product_2, 'test_discount_2', -3.5)

    receipt_with_multiple_items.add_discount(test_discount_1)
    receipt_with_multiple_items.add_discount(test_discount_2)

    verify(ReceiptPrinter().print_receipt(receipt_with_multiple_items))
