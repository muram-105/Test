# -*- coding: utf-8 -*-
from . import models
from odoo import api, SUPERUSER_ID,_
 
def _auto_install_deffered_expense(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    companys = env.user.company_ids
    for company in companys:
        if env["account.account"].search([('company_id','=',company.id)]):
            env["account.chart.template"].load_account_assets(company)