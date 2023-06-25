# -*- coding: utf-8 -*-
{
    'name': "POS Analytic Account",
    'summary': """
        This odoo addons provide analytic account for account entry in POS""",

    'description': """
        This odoo addons provide analytic account for account entry in POS
    """,

    'author': "Seventy Eight Systems",
    'website': "https://www.78systems.com",
    'category': 'POS',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale','account'],

    # always loaded
    'data': [
        'views/pos_config_views.xml',
        'views/pos_session_views.xml',
    ],
    
}
