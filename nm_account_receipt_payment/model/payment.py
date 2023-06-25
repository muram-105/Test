# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class AccountPayment(models.Model):
    _inherit = "account.payment"
    
    
    not_contact = fields.Boolean('Not a Contact', readonly=True, states={'draft':[('readonly',False)]}, default=False, copy=True)
    available_account_ids = fields.Many2many('account.account',compute="_compute_available_account_ids")
    #Overwrite destination_account_id
    destination_account_id = fields.Many2one(domain="[('id','in',available_account_ids)]")
    
    _sql_constraints = [('not_contact_internal', 'CHECK(not(is_internal_transfer and not_contact))', 'The payment should be Not a Contact or Is Internal Transfer' )]
    
    @api.onchange('is_internal_transfer')
    def _onchange_not_contact_is_internal_transfer(self):
        self.not_contact = False
    
    @api.depends('not_contact','company_id','journal_id','outstanding_account_id')
    def _compute_available_account_ids(self):
        account_obj = self.env['account.account']
        for pay in self:
            if pay.not_contact:
                domain = [('account_type', 'not in', ('asset_receivable', 'liability_payable')), ('company_id', '=', pay.company_id.id),
                          ('id','not in',(pay.journal_id.default_account_id | pay.outstanding_account_id).ids)]
            else:
                domain = [('account_type', 'in', ('asset_receivable', 'liability_payable')), ('company_id', '=', pay.company_id.id)]
            available_account_ids = account_obj.search(domain)
            pay.available_account_ids = available_account_ids
    
        
    @api.onchange("not_contact","payment_type")
    def _onchange_not_contact(self):
        if not self.env.context.get('skip_iit'):
            self.destination_account_id = False
            self.is_internal_transfer = False
        if self.not_contact:
            if self.payment_type =='inbound':
                self.partner_type = 'customer'
            else:
                self.partner_type = 'supplier'

    def _compute_destination_account_id(self):
        pay_ids = self.filtered(lambda x: x.destination_account_id and x.destination_account_id not in x.available_account_ids)
        pay_ids.destination_account_id = False
        self = self.filtered(lambda x: not x.not_contact)
        self and super(AccountPayment, self)._compute_destination_account_id()
        
    def _seek_for_lines(self):
        res = super(AccountPayment, self)._seek_for_lines()
        if self.not_contact:
            line_id = self.line_ids.filtered(lambda x: x.account_id == self.destination_account_id)
            if len(line_id) == 1 and not res[1] and line_id & res[2]:
                res = list(res)
                res[1] = line_id
                res[2] = res[2] - line_id
                res = tuple(res)
        return res