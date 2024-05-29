# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'shop_product_discount',
    'version': '1.0',
    'summary': "shop discount module",
    'sequence': 10,
    'author': "anand",
    'description': """
Shop discount  for specific product
""",
    'category': 'Custom/Website_sale',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['mail', 'sale', 'base', 'product', 'website', 'website_sale'],
    'data': [
        'views/views.xml',
        'report/totals.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
