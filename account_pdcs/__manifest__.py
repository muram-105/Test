# -*- coding: utf-8 -*-
{
    'name': 'SW - Post Dated Cheques Management',
    'version': '2.0',
    'category': 'Accounting',
    'description': """PDc's Management
    - Cheque paper settings: 
        - Height: 165mm
        - Width: 82mm
        - Orientation: Portrait
        - Print from system dialog: Ctrl+Shift+P
""",
    'author' : 'Smart Way Business Solutions',
    'website' : 'https://www.smartway.co',
    'depends': ['base','account','account_reports', 'account_accountant_check_printing', 'contacts'],
    'init_xml': [],
    'data': [
        'data/account_check_printing_data.xml',
        'wizard/refuse_cheque.xml',
        'wizard/reroute_cheque.xml',
        'view/receipt_report.xml',
        'view/extra_reports.xml',
        'view/cheques_report.xml',
        'view/payment_view.xml',
        'view/account_report.xml',
        'security/ir.model.access.csv',
        'view/partner.xml',

             ],
    'images':  ["static/description/image.png"],
    'installable': True,
    'license': "Other proprietary",

}
