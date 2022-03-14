from equalexperts import __version__

from equalexperts.shopping_cart import ShoppingCart, Product
from decimal import Decimal
import pytest
import itertools

# Acceptance Criteria AC0-AC2


def test_ac0():
    cart = ShoppingCart()
    dove = Product("Dove Soap", "39.99")
    cart.add_item(dove)
    assert cart.number_of_line_items() == 1
    assert dove in cart and cart[dove] == 1
    assert cart.total_price() == Decimal("39.99")


def test_ac1():
    cart = ShoppingCart()
    dove = Product("Dove Soap", "39.99")
    cart.add_multiple_items(dove, 5)
    cart.add_multiple_items(dove, 3)
    assert cart.number_of_line_items() == 1
    assert dove in cart and cart[dove] == 8
    assert cart.total_price() == Decimal("319.92")


def test_ac2():
    cart = ShoppingCart()
    dove = Product("Dove Soap", "39.99")
    axe = Product("Axe Deo", "99.99")
    cart.add_multiple_items(dove, 2)
    cart.add_multiple_items(axe, 2)
    cart.set_sales_tax_rate("0.125")
    assert cart.number_of_line_items() == 2
    assert dove in cart and cart[dove] == 2
    assert axe in cart and cart[axe] == 2
    assert cart.sales_tax() == Decimal("35.00")
    assert cart.total_price() == Decimal("314.96")


# Product Tests


def test_create_product_OK():
    names = ("my item", "a", "looooooooooooooooooooooong striiiiiiiiiiiing")
    prices = ("12.34", 5.01, 2, Decimal("4.87"))
    for name, price in itertools.product(names, prices):
        item = Product(name, price)
        assert item.name == name and item.unit_price == round(Decimal(price), 2)


def test_product_equality():
    dove_name = "dove"
    dove_price = Decimal("39.99")

    not_dove_name = "not dove"
    not_dove_price = Decimal("10.00")

    dove = Product(dove_name, dove_price)
    dove_copy = Product(dove_name, dove_price)

    assert dove is not dove_copy
    assert dove == dove_copy

    same_name_different_price = Product(dove_name, not_dove_price)
    assert same_name_different_price != dove

    different_name_same_price = Product(not_dove_name, dove_price)
    assert different_name_same_price != dove

    different_name_different_price = Product(not_dove_name, not_dove_price)
    assert different_name_different_price != dove


# Shopping Cart Tests


def test_round_up_sales_tax():
    """
    We should round up 0.5 cents to 1 cent
    when computing sales tax; therefore, 10.5% tax
    on a $1 item should be 11 cents.
    """
    cart = ShoppingCart()
    one_dollar_item = Product("My Lovely Test Product", Decimal("1.00"))
    cart.set_sales_tax_rate(Decimal("0.105"))
    cart.add_item(one_dollar_item)
    assert cart.sales_tax() == Decimal("0.11")
    assert cart.total_price() == Decimal("1.11")


def test_round_down_sales_tax():
    """
    We should round anything below 0.5 cents down to 0 cents.
    when computing sales tax; therefore, 10.499% tax
    on a $1 item should be 10 cents.
    """
    cart = ShoppingCart()
    one_dollar_item = Product("Another Great Test Product", Decimal("1.00"))
    cart.set_sales_tax_rate(Decimal("0.10499"))
    cart.add_item(one_dollar_item)
    assert cart.sales_tax() == Decimal("0.10")
    assert cart.total_price() == Decimal("1.10")


def test_impossible_to_remove_more_items_than_exist_in_cart():
    cart = ShoppingCart()
    one_dollar_item = Product("One further Great Test Product", Decimal("1.00"))
    cart.add_item(one_dollar_item)
    nonexistent_item = Product("Does not exist in the cart", Decimal("5.00"))
    assert cart[nonexistent_item] == 0
    with pytest.raises(AssertionError):
        cart.remove_multiple_items(nonexistent_item, 2)
    with pytest.raises(AssertionError):
        cart.remove_multiple_items(one_dollar_item, 10)


def test_cart_has_correct_number_of_items_after_add_and_remove():
    cart = ShoppingCart()
    dove = Product("Dove Soap", "39.99")
    axe = Product("Axe Deo", "99.99")
    cart.add_multiple_items(dove, 2)
    assert len(cart) == 1
    cart.add_multiple_items(axe, 2)
    assert len(cart) == 2
    cart.remove_multiple_items(axe, 1)
    assert len(cart) == 2
    cart.remove_all(dove)
    assert len(cart) == 1
    cart.remove_multiple_items(axe, 1)
    assert len(cart) == 0
    cart.add_multiple_items(axe, 0)
    assert len(cart) == 0


def test_sales_tax_getter_and_setter():
    cart = ShoppingCart()
    sales_tax_rate = Decimal("0.1")
    cart.set_sales_tax_rate(sales_tax_rate)
    assert cart.get_sales_tax_rate() == sales_tax_rate


def test_printing():
    cart = ShoppingCart()
    dove = Product("Dove Soap", "39.99")
    cart.add_item(dove)
    assert dove.name in str(cart)
    assert str(dove.unit_price) in str(cart)
