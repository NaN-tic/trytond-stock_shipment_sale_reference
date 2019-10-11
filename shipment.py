# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from itertools import chain

__all__ = ['ShipmentOut', 'ShipmentOutReturn']


class ShipmentOutMixin(object):

    sale_references = fields.Function(fields.Char('Sale References'),
        'get_sale_references', searcher='search_sale_references')

    def get_sale_references(self, name):
        references = list(set([m.sale.reference if m.sale.reference else
                    '' for m in self.moves if m.sale]))
        references.sort()
        return ', '.join(references)

    @classmethod
    def __sale_references_field_factory(cls):
        if cls.__name__ == 'stock.shipment.out':
            return 'shipments'
        elif cls.__name__ == 'stock.shipment.out.return':
            return 'shipment_returns'

        return None

    @classmethod
    def search_sale_references(cls, name, clause):
        pool = Pool()
        Sale = pool.get('sale.sale')
        sales = Sale.search([('reference', clause[1], clause[2])])
        field = cls.__sale_references_field_factory()
        if not hasattr(Sale, field):
            return []
        shipments = [eval('s.%s' % field) for s in sales]
        return [('id', 'in', [s.id for s in chain(*shipments) if s.__name__ ==
                    cls.__name__])]


class ShipmentOut(ShipmentOutMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'


class ShipmentOutReturn(ShipmentOutMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.return'
