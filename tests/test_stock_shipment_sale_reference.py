#!/usr/bin/env python
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class StockSaleReferencesTestCase(ModuleTestCase):
    'Test stock_shipment_sale_reference module'
    module = 'stock_shipment_sale_reference'

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            StockSaleReferencesTestCase))
    return suite
