# -*- coding:utf-8 -*-
from odoo import _, api, fields, models, tools

class PosSession(models.Model):
    _inherit = 'pos.session'
    
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',related='config_id.account_analytic_id')

    
    
    def _credit_amounts(
        self,
        partial_move_line_vals,
        amount,
        amount_converted,
        force_company_currency=False,
    ):
        """We only want the analyitic account set in the sales items from the account
        move. This is called from `_get_sale_vals` but from other credit methods
        as well. To ensure that only sales items get the analytic account we flag
        the context from the former method with the proper analytic account id.
        """
        account_analytic_id = self.analytic_account_id.id
       
        if account_analytic_id:
            partial_move_line_vals['analytic_distribution'] =  {}
            partial_move_line_vals['analytic_distribution'][account_analytic_id] = account_analytic_id
           
        return super()._credit_amounts(
            partial_move_line_vals, amount, amount_converted, force_company_currency
        )

   


class PosOrder(models.Model):
    _inherit = 'pos.order'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    
    
    @api.model
    def _order_fields(self, ui_order):  
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['analytic_account_id'] = self.env['pos.session'].browse(order_fields.get('session_id')).analytic_account_id.id
        return order_fields
    
