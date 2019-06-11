# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import shipment


def register():
    Pool.register(
        shipment.ShipmentOut,
        shipment.ShipmentOutReturn,
        module='stock_shipment_sale_reference', type_='model')
