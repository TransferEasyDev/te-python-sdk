#! /usr/bin/env python
# -*- coding:utf-8 -*-

from decimal import Decimal, ROUND_DOWN

from hp_money import Money as HPMoney
from hp_money.amount import Amount as HPAmount
from hp_money.currency import Currency

from domain.preload_objects.currencies import take_currency_by


class Money(HPMoney):

    def __init__(self, *, currency, amount, origin=False):
        if not isinstance(currency, Currency):
            currency = take_currency_by(iso_code=currency)

        super(Money, self).__init__(currency=currency, amount=amount, origin=origin)

        self._accuracy = currency.accuracy

        self._amount = Amount(
            amount,
            self._accuracy if not origin else 1,
            self._accuracy,
        )


class Amount(HPAmount):

    def __init__(self, value, accuracy=100, real_accuracy=100):
        super(Amount, self).__init__(value, accuracy)
        self.real_accuracy = Decimal(real_accuracy)

    @property
    def standard_value(self):
        return (self._value / self.real_accuracy).quantize(
            Decimal(1) / self.real_accuracy,
            ROUND_DOWN
        )


