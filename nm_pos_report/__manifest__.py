# -*- coding: utf-8 -*-
{
    'name': "NM - Custom PoS Report",
    'summary': "Add Arabic to the PoS reprot",
    'description': """ """,
    'author': "Smart Way Business Solutions",
    'website': "https://www.smartway.co",
    'category': 'Point of Sale',
    'version': '1.1',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [
    ],
    'assets': {
        'point_of_sale.assets': [
            'nm_pos_report/static/src/js/models.js',
            'nm_pos_report/static/src/xml/OrderReceipt.xml'],
        }
}
