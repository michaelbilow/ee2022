from decimal import Decimal
import decimal
from typing import Union, Optional

from pyparsing import line

ctx = decimal.getcontext()
ctx.rounding = decimal.ROUND_HALF_UP


class Product:
    def __init__(self, name: str, unit_price: Union[str, int, float, Decimal]) -> None:
        self.name = name
        self.unit_price = round(Decimal(unit_price), 2)

    def __repr__(self) -> str:
        return f"{self.name} {self.unit_price}"

    def __eq__(self, other: "Product") -> bool:
        return self.name == other.name and self.unit_price == other.unit_price

    def __hash__(self) -> int:
        return hash((self.name, self.unit_price))


class ShoppingCart:
    """
    Class representing a shopping cart with a certain sales tax rate.
    Sales tax is applied to the cart itself which is perhaps a bit diffi
    """

    # Python naming convention for private class members, though nothing
    # is truly private. We could also use dunders to get fuzzed names
    # but again, this isn't truly Java/Scala private.

    def __init__(
        self,
        line_items: Optional[dict[Product, int]] = None,
        sales_tax_rate: Union[str, int, float, Decimal] = Decimal(0),
    ):
        self._line_items: dict[Product, int] = {} if not line_items else line_items
        self._sales_tax_rate: Decimal = Decimal(sales_tax_rate)

    def set_sales_tax_rate(self, rate: Union[str, Decimal]) -> None:
        self._sales_tax_rate = Decimal(rate)

    def get_sales_tax_rate(self) -> Decimal:
        return self._sales_tax_rate

    def gross_price(self) -> Decimal:
        return sum(
            count * product.unit_price for product, count in self._line_items.items()
        )

    def sales_tax(self) -> Decimal:
        return round(self.gross_price() * self._sales_tax_rate, 2)

    def total_price(self) -> Decimal:
        gross_price = self.gross_price()
        sales_tax = self.sales_tax()
        return round(gross_price + sales_tax, 2)

    def add_multiple_items(self, product: Product, count: int) -> None:
        """
        Allows removing items from the cart when `count` < 0
        Note, this is the **only** function that should be used to manipulate
        objects in the cart; every other function that manipulates the line items
        in the cart should call this function--otherwise, it can be tricky
        to make sure that the cart only has line items that are strictly positive.
        """
        if count < 0:
            assert product in self, f"Product {product} not in the cart!"
            current_count = self[product]
            assert (
                count + current_count >= 0
            ), f"Only {current_count} of {product} in the cart; the requested amount ({count}) cannot be removed."
        self._line_items[product] = self[product] + count
        self._cleanup_product(product)
        return

    def add_item(self, product: Product) -> None:
        self.add_multiple_items(product, 1)

    def remove_multiple_items(self, product: Product, count: int) -> None:
        assert (
            count > 0
        ), "You cannot remove a negative number of items; use `add_multiple_items` instead."
        self.add_multiple_items(product, -count)

    def remove_all(self, product: Product) -> None:
        self.add_multiple_items(product, -self[product])

    def _cleanup_product(self, product: Product) -> None:
        """
        Remove zero-count products from the cart
        """
        if not self._line_items[product]:
            del self._line_items[product]

    @staticmethod
    def receipt_format(count, name, price) -> str:
        return f"{count:<10}{name:<40}{price:<10}"

    def __repr__(self) -> str:
        header = f"{'='*60}\n{self.receipt_format('Count', 'Name', 'Price')}"
        items_str = "\n".join(
            self.receipt_format(count, product.name, product.unit_price)
            for product, count in self._line_items.items()
        )
        footer = (
            f"{'='*60}\nSubtotal:\t{self.gross_price()}\n"
            + f"Sales Tax:\t{self.sales_tax()}\nTotal:\t\t{self.total_price()}"
        )
        return f"\n{header}\n{items_str}\n{footer}\n"

    def __contains__(self, product: Product) -> bool:
        return product in self._line_items and self._line_items[product] > 0

    def __getitem__(self, product: Product) -> int:
        return 0 or (product in self and self._line_items[product])

    def __len__(self) -> int:
        return len(self._line_items)
