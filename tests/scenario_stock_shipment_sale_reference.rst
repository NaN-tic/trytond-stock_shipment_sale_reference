=============================
Stock Shipment Sale Reference
=============================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from operator import attrgetter
    >>> from proteus import config, Model, Wizard
    >>> today = datetime.date.today()
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax


Create config::
    >>> config = activate_modules('teb')


Create company::

  >>> _ = create_company()
  >>> company = get_company()

Create fiscal year::

  >>> fiscalyear = set_fiscalyear_invoice_sequences(
  ...     create_fiscalyear(company))
  >>> fiscalyear.click('create_period')
  >>> period = fiscalyear.periods[0]

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> receivable = accounts['receivable']
    >>> payable = accounts['payable']
    >>> cash = accounts['cash']

Create payment type::

    >>> PaymentType = Model.get('account.payment.type')
    >>> preceivable = PaymentType(name='Receivable', kind='receivable')
    >>> preceivable.save()
    >>> ppayable = PaymentType(name='Payable', kind='payable')
    >>> ppayable.save()

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.account_payable = payable
    >>> customer.account_receivable = receivable
    >>> customer.customer_payment_type = preceivable
    >>> customer.supplier_payment_type = ppayable
    >>> customer.customer = True
    >>> customer.save()
    >>> supplier = Party(name='Supplier')
    >>> supplier.account_payable = payable
    >>> supplier.account_receivable = receivable
    >>> supplier.save()

Create category::

    >>> ProductCategory = Model.get('product.category')
    >>> category = ProductCategory(name='Category')
    >>> category.accounting = True
    >>> category.account_expense = expense
    >>> category.account_revenue = revenue
    >>> category.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')
    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.list_price = Decimal(30)
    >>> template.accounts_category = True
    >>> template.account_category = category
    >>> template.producible = True
    >>> template.salable = True
    >>> template.save()
    >>> product, = template.products
    >>> product.cost_price = Decimal(20)


    >>> template = ProductTemplate()
    >>> template.name = 'product 2'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.list_price = Decimal(30)
    >>> template.account_category = category
    >>> template.producible = True
    >>> template.save()
    >>> product2, = template.products
    >>> product2.cost_price = Decimal(0)

    >>> template = ProductTemplate()
    >>> template.name = 'product 3'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.producible = True
    >>> template.list_price = Decimal(15)
    >>> template.account_category = category
    >>> template.save()
    >>> product3, = template.products
    >>> product.cost_price = Decimal(0)

Create Components::

    >>> meter, = ProductUom.find([('name', '=', 'Meter')])
    >>> centimeter, = ProductUom.find([('name', '=', 'centimeter')])
    >>> templateA = ProductTemplate()
    >>> templateA.name = 'component A'
    >>> templateA.default_uom = meter
    >>> templateA.type = 'goods'
    >>> templateA.list_price = Decimal(2)
    >>> templateA.account_category = category
    >>> templateA.save()
    >>> componentA, = templateA.products
    >>> componentA.cost_price = Decimal(1)

    >>> templateB = ProductTemplate()
    >>> templateB.name = 'component B'
    >>> templateB.default_uom = meter
    >>> templateB.type = 'goods'
    >>> templateB.list_price = Decimal(2)
    >>> templateB.account_category = category
    >>> templateB.save()
    >>> componentB, = templateB.products
    >>> componentB.cost_price = Decimal(1)

    >>> template1 = ProductTemplate()
    >>> template1.name = 'component 1'
    >>> template1.default_uom = unit
    >>> template1.type = 'goods'
    >>> template1.list_price = Decimal(5)
    >>> template1.account_category = category
    >>> template1.producible = True
    >>> template1.save()
    >>> component1, = template1.products
    >>> component1.cost_price = Decimal(2)

    >>> template2 = ProductTemplate()
    >>> template2.name = 'component 2'
    >>> template2.default_uom = meter
    >>> template2.type = 'goods'
    >>> template2.list_price = Decimal(7)
    >>> template2.account_category = category
    >>> template2.save()
    >>> component2, = template2.products
    >>> component2.cost_price = Decimal(5)

Create Bill of Material::

    >>> BOM = Model.get('production.bom')
    >>> component_bom = BOM(name='component1')
    >>> input1 = component_bom.inputs.new()
    >>> input1.product = componentA
    >>> input1.quantity = 1
    >>> input2 = component_bom.inputs.new()
    >>> input2.product = componentB
    >>> input2.quantity = 1
    >>> output = component_bom.outputs.new()
    >>> output.product = component1
    >>> output.quantity = 1
    >>> component_bom.save()

    >>> ProductBom = Model.get('product.product-production.bom')
    >>> component1.boms.append(ProductBom(bom=component_bom))
    >>> component1.save()

    >>> bom = BOM(name='product')
    >>> input1 =  bom.inputs.new()
    >>> input1.product = component1
    >>> input1.quantity = 5
    >>> input2 =  bom.inputs.new()
    >>> input2.product = component2
    >>> input2.quantity = 150
    >>> input2.uom = centimeter
    >>> output = bom.outputs.new()
    >>> output.product = product
    >>> output.quantity = 1
    >>> bom.save()

    >>> ProductBom = Model.get('product.product-production.bom')
    >>> product.boms.append(ProductBom(bom=bom))
    >>> product.save()

Create a cost plan from BoM::

  >>> CostPlan = Model.get('product.cost.plan')
  >>> plan = CostPlan()
  >>> plan.product = product
  >>> plan.quantity = 1
  >>> plan.save()

Create payment term::

  >>> payment_term = create_payment_term()
  >>> payment_term.save()

Create an Inventory::

    >>> Inventory = Model.get('stock.inventory')
    >>> InventoryLine = Model.get('stock.inventory.line')
    >>> Location = Model.get('stock.location')
    >>> storage, = Location.find([
    ...         ('code', '=', 'STO'),
    ...         ])
    >>> inventory = Inventory()
    >>> inventory.location = storage
    >>> inventory.save()
    >>> inventory_line = InventoryLine(product=product, inventory=inventory)
    >>> inventory_line.quantity = 100.0
    >>> inventory_line.expected_quantity = 0.0
    >>> inventory.save()
    >>> inventory_line.save()
    >>> Inventory.confirm([inventory.id], config.context)
    >>> inventory.state
    u'done'

Sale 5 products::

    >>> Sale = Model.get('sale.sale')
    >>> SaleLine = Model.get('sale.line')
    >>> sale = Sale()
    >>> sale.invoice_method = 'manual'
    >>> sale.party = customer
    >>> sale.reference = 'TestReference1'
    >>> line = sale.lines.new()
    >>> line.product = product
    >>> line.quantity = 2.0
    >>> line = sale.lines.new()
    >>> line.product = product
    >>> line.quantity = 3.0
    >>> sale.payment_term = payment_term
    >>> sale.save()
    >>> Sale.quote([sale.id], config.context)
    >>> Sale.confirm([sale.id], config.context)
    >>> Sale.process([sale.id], config.context)
    >>> sale.state
    u'processing'
    >>> sale.reload()
    >>> len(sale.shipments), len(sale.shipment_returns)
    (1, 0)
    >>> shipment, = sale.shipments
    >>> sale.reference in shipment.sale_references
    True
    >>> sale1_reference = sale.reference

Sale 5 products again::

    >>> Sale = Model.get('sale.sale')
    >>> SaleLine = Model.get('sale.line')
    >>> sale = Sale()
    >>> sale.shipment_method = 'manual'
    >>> sale.invoice_method = 'manual'
    >>> sale.party = customer
    >>> sale.reference = 'TestReference2'
    >>> line = sale.lines.new()
    >>> line.product = product
    >>> line.quantity = 2.0
    >>> line = sale.lines.new()
    >>> line.product = product
    >>> line.quantity = 3.0
    >>> sale.payment_term = payment_term
    >>> sale.save()
    >>> Sale.quote([sale.id], config.context)
    >>> Sale.confirm([sale.id], config.context)
    >>> Sale.process([sale.id], config.context)
    >>> sale.state
    u'done'
    >>> sale.reload()
    >>> len(sale.shipments), len(sale.shipment_returns)
    (0, 0)
    >>> line = sale.lines[0]
    >>> move = shipment.inventory_moves.new()
    >>> move.product = line.product
    >>> move.origin = line
    >>> move.quantity = line.quantity
    >>> move.to_location = shipment.moves[0].to_location
    >>> move.from_location = shipment.moves[0].from_location
    >>> shipment.save()
    >>> shipment.reload()
    >>> sale.reference in shipment.sale_references
    True
    >>> sale2_reference = sale.reference
    >>> sale1_reference in shipment.sale_references and sale2_reference in shipment.sale_references
    True
