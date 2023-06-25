# -*- coding: utf-8 -*-
{
    'name': 'Middle East - Accounting Assets',
    'version': '1.0',
    'category': 'Localization',
    'description': """
    """,
    'website': 'https://www.smartway.co',
    'author': 'Smart Way Business Solutions',
    'depends': ['l10n_me','account_asset',],
    'data': [
       
    ],
        'auto_install': True,
        'installable': True,
        
    'post_init_hook': '_auto_install_deffered_expense',
    'license':  "Other proprietary",

}
