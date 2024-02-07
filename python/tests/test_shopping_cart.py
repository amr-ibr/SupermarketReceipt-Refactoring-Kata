from model_objects import Product, ProductUnit, SpecialOfferType


def test_add_item_without_quantity(cart):
    product = Product('test-product-1', ProductUnit.EACH)
    cart.add_item(product)

    expected = [(product, 1)]
    actual = [(pq.product, pq.quantity) for pq in cart.items]

    assert expected == actual
    assert cart.product_quantities == {product: 1}


def test_add_duplicate_items(cart):
    product = Product('test-product-1', ProductUnit.EACH)
    cart.add_item(product)
    cart.add_item(product)

    expected = [(product, 1), (product, 1)]
    actual = [(pq.product, pq.quantity) for pq in cart.items]

    assert expected == actual
    assert cart.product_quantities == {product: 2}


def test_add_item_with_quantity(cart):
    product = Product('test-product-1', ProductUnit.EACH)
    cart.add_item_quantity(product, 3)

    expected = [(product, 3)]
    actual = [(pq.product, pq.quantity) for pq in cart.items]

    assert expected == actual
    assert cart.product_quantities == {product: 3}


def test_handle_offers_empty_catalog_and_empty_cart(
    handle_offers, receipt
):
    handle_offers()
    assert receipt.total_price() == 0


def test_handle_offers_item_not_in_catalog(
    receipt, cart, handle_offers
):
    product = Product('test-product-1', ProductUnit.EACH)
    cart.add_item(product)

    handle_offers()

    assert receipt.total_price() == 0


def test_handle_offers_single_item_and_no_offers(
    receipt, make_cart_item, handle_offers
):
    make_cart_item('test-product-1', 20, 1)
    handle_offers()

    assert receipt.discounts == []
    assert receipt.total_price() == 20


def test_handle_offers_only_single_offer_per_product_applied(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 3)
    make_offer('test-product-1', SpecialOfferType.THREE_FOR_TWO, 40)
    make_offer('test-product-1', SpecialOfferType.TEN_PERCENT_DISCOUNT, 10)

    handle_offers()
    assert len(receipt.discounts) == 1
    assert receipt.total_price() == 54


def test_handle_offers_with_multi_order_and_multi_offers(
    receipt, make_cart_item, make_offer, handle_offers
):
    make_cart_item('test-product-1', 20, 3)
    make_offer('test-product-1', SpecialOfferType.THREE_FOR_TWO, 40)

    make_cart_item('test-product-2', 20, 5)
    make_offer('test-product-2', SpecialOfferType.FIVE_FOR_AMOUNT, 66.66)

    make_cart_item('test-product-3', 20, 5)
    make_offer('test-product-3', SpecialOfferType.TEN_PERCENT_DISCOUNT, 10)

    handle_offers()

    assert len(receipt.discounts) == 3
    assert receipt.total_price() == 196.66
