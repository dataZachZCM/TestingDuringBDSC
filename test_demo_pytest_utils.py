import pytest

# from demo_pytest_utils.utils import (
#     clean_product_name,
#     calculate_total_price,
#     is_high_value_order,
# )


def test_clean_product_name_removes_spaces_and_title_cases():
    result = clean_product_name("  wireless mouse  ")

    assert result == "Wireless Mouse"


def test_clean_product_name_handles_none():
    result = clean_product_name(None)

    assert result == ""


def test_calculate_total_price():
    result = calculate_total_price(10.00, 3)

    assert result == 30.00


def test_calculate_total_price_rejects_negative_price():
    with pytest.raises(ValueError):
        calculate_total_price(-5.00, 2)


def test_calculate_total_price_rejects_negative_quantity():
    with pytest.raises(ValueError):
        calculate_total_price(5.00, -2)


@pytest.fixture
def sample_order():
    return {
        "price": 25.00,
        "quantity": 4,
        "threshold": 100.00,
    }


def test_is_high_value_order_with_fixture(sample_order):
    total_price = calculate_total_price(
        sample_order["price"],
        sample_order["quantity"]
    )

    result = is_high_value_order(
        total_price,
        threshold=sample_order["threshold"]
    )

    assert result is True


def test_is_high_value_order_below_threshold():
    result = is_high_value_order(75.00, threshold=100.00)

    assert result is False