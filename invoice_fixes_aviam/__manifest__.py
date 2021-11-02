# -*- coding: utf-8 -*-
{
    'name': "Invoice Fixes Aviam",

    'summary': """
        Implement Fixes at Invoices for Aviam Requirements""",

    'description': """
        1-Fix to Account date
        2-Fix to Account Move Reversal and Debit Note
        3-Add funcionality to create email template by client
    """,

    'author': "Aviam LTD",
    'website': "http://aviamltd.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale_management','purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_reversal_fix.xml',
        'views/account_move_debit_note.xml',
        'views/partner.xml',
        'views/res_partner_mail_template.xml'
    ],

    # is an application
    'application' : True,
}
