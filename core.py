#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author:
    Graham Steeds

Context:
    This module provides  the Fund object class for financeapp.py. The Fund object
    class represents a financial instrument such as a mutual fund or stock, that is
    traded in a financial market.

Attributes:
    CORE_LOG_LEVEL: Default log level when this module is called directly.
    DATE_FORMAT: Format for working with dates. (yyyy-mm-dd).
    DEFAULT_CORE_LOG_FILENAME: Default filename for logging when module called directly.
    RUNTIME_ID: Generate a unique uuid object. Used in logging.

Composition Attributes:
    Line length = 88 characters.
"""


import logging
import uuid
from datetime import datetime
from logging import handlers


CORE_LOG_LEVEL = logging.WARNING
DATE_FORMAT = '%Y-%m-%d'
DEFAULT_CORE_LOG_FILENAME = 'core.log'  # Used when __name__ == '__main__'
RUNTIME_ID = uuid.uuid4()

# Configure logging.
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class CoreError(RuntimeError):
    """Base class for exceptions arising from this module."""


class Fund:
    """Represents a financial instrument such as a mutual fund or stock.

    Args:
        symbol (str): First parameter. Symbol representing a financial
            instrument, such as 'F'.
        currency (str): Second parameter. Symbol of trading currency such as 'USD'.
        instrument_type (str): Third parameter. Type of fund. Example: 'MUTUALFUND' or
            'STOCK'.
        dates_prices (list[['yyyy-mm-dd', 'float']]): Fourth parameter. List of lists
            containing date and price data.
        name (str): OPTIONAL. An optional given name or nickname for fund by user.
    """

    def __init__(self, symbol, currency, instrument_type, dates_prices, name=None):
        self.symbol = symbol.upper()  # Fund symbol. Ex. 'FXAIX'.
        self.currency = currency.upper()  # Currency of fund. Ex. 'USD'.
        self.instrument_type = instrument_type.upper()  # Ex. 'STOCK'.
        # Turn date string into datetime object in yyyy-mm-dd format.
        self.dates_prices = [[datetime.strptime(dp[0], DATE_FORMAT).date(), dp[1]]
                             for dp in dates_prices]
        self.name = name  # Optional name for fund given by user.

    def __str__(self):
        """String representation of Fund.

        Args:
            None

        Returns:
            formatted_str (str): String representing Fund.
                Example:
                    'FSMAX -\nUSD - MUTUALFUND\nLatest price: 2022-04-05 - $78.42'
        """

        log.debug(f'__str__ ({self.__repr__()})...')

        # Get the latest price and round it to 2 decimal places.
        if self.dates_prices[-1][1]:
            formatted_price = '{:.2f}'.format(self.dates_prices[-1][1])
        else:  # Use previous days data when latest data is not available.
            formatted_price = '{:.2f}'.format(self.dates_prices[-2][1])

        formatted_str = '{} - {}\n{} - {}\nLatest price: {} - ${}'.\
            format(
                self.symbol,
                self.name or '',
                self.currency,
                self.instrument_type,
                self.dates_prices[-1][0],
                formatted_price
            )

        log.debug(f'__str__ ({self.__repr__()}) complete...')

        return formatted_str

    def __repr__(self):
        """String of funds unique identifying trait: self.symbol.

        Args:
            None

        Returns:
            self.symbol (str): The symbol for the Fund.
        """

        log.debug(f'__repr__ ({self.symbol}) complete.')

        return self.symbol

    def __eq__(self, other):
        """Determine the equality of self and other.

        Other can be a Fund object or a string representing a fund symbol.

        Args:
            other (Fund obj, OR str): Determine the equality of self and other based on
            if Fund.symbol == other.symbol, or if Fund.symbol == other.

        Returns:
            True if found to be the same, False otherwise.
        """

        log.debug(f'__eq__ (self: {self.__repr__()}, other: {other})...')

        if isinstance(other, Fund):  # Compare if type(other) is Fund.
            log.debug(f'__eq__ (other type = {type(other)}, '
                      f'self is other = '
                      f'{True if self.symbol == other.symbol else False}')
            return True if self.symbol == other.symbol else False

        elif isinstance(other, str):  # Compare if type(other) is str.
            log.debug(f'__eq__ (other type = {type(other)}, '
                      f'self is other = '
                      f'{True if self.symbol == other else False}')
            return True if self.symbol == other else False

        else:  # When type other is not a legal type. i.e. a Fund or str.
            msg = f'Type {type(other)} is not a legally comparable type.'
            log.warning(msg)
            raise CoreError(msg)


def core_self_test():
    """Run Unittests on module.

    Args:
        None

    Returns:
        None
    """

    import unittest

    import test_core

    # Conduct unittest.
    suite = unittest.TestLoader().loadTestsFromModule(test_core)
    unittest.TextTestRunner(verbosity=2).run(suite)


def test():
    """For development level module testing."""

    pass


if __name__ == '__main__':

    # Configure Rotating Log. Only runs when module is called directly.
    handler = handlers.RotatingFileHandler(
        filename=DEFAULT_CORE_LOG_FILENAME,
        maxBytes=100**3,  # 0.953674 Megabytes.
        backupCount=1
    )
    formatter = logging.Formatter(
        f'[%(asctime)s] - {RUNTIME_ID} - %(levelname)s - [%(name)s:%(lineno)s] - '
        f'%(message)s'
    )
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(CORE_LOG_LEVEL)

    self_test()
