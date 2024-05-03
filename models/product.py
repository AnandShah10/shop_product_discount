from odoo import models, fields, api, _
from odoo.tools.misc import clean_context, formatLang


class Product(models.Model):
    _inherit = 'product.product'

    discount = fields.Boolean(default=False, string='Discount')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends_context('lang')
    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed', 'currency_id',
                 'order_line.active_discount')
    def _compute_tax_totals(self):
        super(SaleOrder, self)._compute_tax_totals()
        discount = 0.0
        for i in self:
            for j in i.order_line:
                # print('hellllllllllll')
                if j.product_id.discount:
                    # print('hhhhhh')
                    # discount += j.product_uom_qty * 10
                    discount += j.active_discount
            # print(i.tax_totals, 'Totals,,,,,,,,,,,,,')
            i.tax_totals['discount'] = discount
            i.tax_totals['formatted_discount'] = formatLang(i.env, discount, digits=0,
                                                                currency_obj=i.currency_id)
            # print(i.tax_totals['formatted_amount_total'], 'formatted before..........')
            # print(discount, 'Discount...............')
            # i.tax_totals['amount_total'] = i.tax_totals['amount_total'] - discount
            i.tax_totals['amount_untaxed'] = i.tax_totals['amount_untaxed'] - discount
            # tax_group_base_amount = i.tax_totals['groups_by_subtotal']['Untaxed Amount'][0]['tax_group_base_amount']
            # i.tax_totals['groups_by_subtotal']['Untaxed Amount'][0][
            #     'tax_group_base_amount'] = tax_group_base_amount - discount
            # tax_amount = sum(((line.price_subtotal-line.active_discount) * float(line.tax_id.amount)) / 100 for line in i.order_line)
            # i.tax_totals['groups_by_subtotal']['Untaxed Amount'][0]['tax_group_amount'] = tax_amount
            # new_amount = i.tax_totals['amount_total']
            new = i.tax_totals['amount_total'] - discount
            # i.tax_totals['formatted_amount_total'] = formatLang(i.env, new_amount, digits=0,
            #                                                     currency_obj=i.currency_id)
            #
            i.tax_totals['formatted_amount_total'] = formatLang(i.env, new, digits=0,
                                                        currency_obj=i.currency_id)
            # print("new formatted!!!!!!!!!", i.tax_totals['formatted_amount_total'])

            # print(i.tax_totals, ';;;;;;;;;;')

    @api.depends('order_line.price_subtotal', 'order_line.price_tax', 'order_line.price_total',
                 'order_line.active_discount')
    def _compute_amounts(self):
        print('HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
        super(SaleOrder, self)._compute_amounts()
        print('Byyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
        discount = 0.00
        for i in self:
            print(i.amount_untaxed, i.amount_tax, i.amount_total)
            for j in i.order_line:
                print('hellllllllllll')
                if j.product_id.discount:
                    print('hhhhhh', j.product_id.name)
                    discount += j.product_uom_qty * 10.00
                    j.price_total = j.price_subtotal + j.price_tax - (j.product_uom_qty * 10.00)
            i.amount_total = i.amount_total - discount
            print(i.amount_total, 'cccccccccccccccccc')

    # def _get_name_tax_totals_view(self):
    #     res = super(SaleOrder, self)._get_name_tax_totals_view()
    #     print(res,'......................')
    #     return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    active_discount = fields.Float(string='Discount', compute='_compute_active_discount')

    @api.depends('product_uom_qty', 'product_id.discount')
    def _compute_active_discount(self):
        for i in self:
            if i.product_id.discount:
                i.active_discount = i.product_uom_qty * 10.00
            else:
                i.active_discount = 0.00

    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'active_discount')
    # def _compute_amount(self):
    #     super(SaleOrderLine, self)._compute_amount()
    #     for line in self:
    #         line.price_total -= line.active_discount
