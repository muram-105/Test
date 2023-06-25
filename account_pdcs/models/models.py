# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import expression

class BankBranch(models.Model):
    _name = 'res.bank.branch'
    _description = 'Bank Branch'
    
    name = fields.Char('Name', required=True)

class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(AccountPaymentMethod, self.with_context(from_create=1)).create(vals_list)
        return res

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['sw_inbound_check'] = {'mode': 'multi', 'domain': [('type', '=', 'bank')]}
        if self.env.context.get('from_create'):
            res['sw_inbound_check']['mode'] = 'unique'
        return res

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    cheque_count = fields.Integer("Number of Cheques",compute='_compute_cheque_count')
    
    def _compute_cheque_count(self):
        results = {i['partner_id'][0]: i['partner_id_count']
                    for i in self.env['account.payment'].sudo().read_group([
                    ('partner_id', 'in', self.ids),
                    ('company_id', '=', self.env.company.id),
                    ('is_cheque', '=', True)],
                    [],['partner_id'])}
        for partner_id in self:
            partner_id.cheque_count = results.get(partner_id.id,0)
        
    def open_cheque_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cheques'),
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'domain': [('partner_id', 'in', self.ids),('company_id', '=', self.env.company.id), ('is_cheque', '=', True)],
            'context':dict(search_default_in_cheque_box=1,
                           search_default_under_collection=1,
                           create=0
                           )
            }
    
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    def write(self,vals):
        if any(f in {'name','date_maturity','amount_currency',
                     'currency_id','debit' ,'credit',
                     'partner_id','account_id'}
                      for f in vals.keys()):
            self.mapped('move_id')._check_payment_moves()
        return super(AccountMoveLine, self).write(vals)
    
    
class AccountMove(models.Model):
    _inherit = "account.move"
    
    def _check_payment_moves(self):
        if self.env.context.get('skip_check_payment_moves'):
            return
        move_fields = ['route_move_ids', 'inverse_move_id']
        move_domain = [['&', ('move_id', 'in', self.ids), ('is_cheque', '=', True)]]
        domain = expression.OR(move_domain + [[(i, 'in', self.ids)] for i in move_fields])
        pay = self.env['account.payment'].sudo().search(domain, limit=1)
        if pay and not self._context.get('move_transaction', False):
            raise UserError("Cannot manipulate moves that related to Cheque")
    
    def write(self,vals):
        if any(f in {'name','partner_id','journal_id','date','ref', 'state'}
                     for f in vals.keys()):
            self._check_payment_moves()
        return super(AccountMove, self).write(vals)
    
    
class AccountPayment(models.Model):
    _inherit = "account.payment"

    res_journal_bank_id = fields.Many2one('res.bank', 'Drawee Bank', tracking=True, copy=True)
    journal_bank_id = fields.Many2one('account.journal', 'Cheque Route', related="route_move_id.journal_id", store=True)
    last_payment_method_line_id = fields.Many2one('account.payment.method.line', string='Payment Method', copy=False)
    is_cheque = fields.Boolean('Bank Cheque', compute="_compute_is_cheque", store=True)
    due_date = fields.Date('Cheque Due Date', copy=True)
    collect_date = fields.Date('Collection Date', compute="_compute_collect_date", store=True)
    send_to_bank_date = fields.Date('Send to Bank Date', compute="_compute_send_to_bank_date", store=True)
    inverse_move_id = fields.Many2one('account.move', 'Refused Account Move', readonly=True, tracking=True, copy=False,
                                      ondelete='restrict')
    cheque_state = fields.Selection([('in_cheque_box', 'In Cheques Box'),
                                     ('issued', 'Issued'),
                                     ('under_collection', 'Under Collection'),
                                     ('refused', 'Refused'),
                                     ('collected', 'Collected')], string='Cheque Status',
                                    compute="_compute_cheque_state", tracking=True, store=1)
    cheque_note = fields.Char('Cheque Note', copy=True)
    cheque_language_id = fields.Many2one('res.lang', 'Cheque Language',
                                         domain=[('code', 'in', ['en_US', 'ar_001']), ('active', 'in', [True, False])])
    check_amount_in_words = fields.Char(readonly=False)
    route_move_ids = fields.Many2many('account.move', 'acc_pay_route_move_rel',
                                      'payment_id', 'move_id', string='Routes', copy=False, readonly=True)
    route_move_id = fields.Many2one('account.move', 'Last Route', compute="_compute_route_move_id", store=True)
    handed_to_from_partner = fields.Boolean('Handed To/From Partner', copy=False)
    bank_branch_id = fields.Many2one('res.bank.branch', 'Bank Branch')
    drawee_name = fields.Char('Drawee Name')
    

    _sql_constraints = [('is_cheque_internal', 'CHECK(not(is_internal_transfer and is_cheque))',
                         'The payment should be Cheque or Is Internal Transfer')]
    
    

    @api.depends('payment_method_line_id')
    def _compute_is_cheque(self):
        for pay in self:
            pay.is_cheque = pay.payment_method_line_id.code in ['check_printing', 'sw_inbound_check']
    @api.depends('cheque_state')
    def _compute_collect_date(self):
        for pay in self:
            if pay.inverse_move_id or not pay.is_cheque:
                collect_date = False
            else:
                statement_line_id = pay.get_pdc_statement_line_id()
                collect_date = statement_line_id and statement_line_id.date or False
            pay.collect_date = collect_date

    @api.depends('route_move_ids.state')
    def _compute_route_move_id(self):
        am_obj = self.env['account.move']
        for payment_id in self:
            if payment_id.route_move_ids:
                payment_id.route_move_id = am_obj.search([('id', 'in', payment_id.route_move_ids.ids),
                                                          ('state', '=', 'posted')],
                                                         order="date desc,id desc",
                                                         limit=1)
            else:
                payment_id.route_move_id = False

    @api.depends('cheque_state')
    def _compute_send_to_bank_date(self):
        for pay in self:
            if pay.cheque_state in ['under_collection', 'refused', 'collected']:
                pay.send_to_bank_date = pay.route_move_id.date
            else:
                pay.send_to_bank_date = False

    @api.depends('is_cheque',
                 'state',
                 'inverse_move_id',
                 'payment_type',
                 'move_id.reversal_move_id.state',
                 'route_move_ids',
                 'route_move_ids.line_ids.reconciled',
                 'move_id.line_ids.reconciled',
                 'last_payment_method_line_id',
                 )
    def _compute_cheque_state(self):
        for pay in self:
            if not pay.is_cheque or pay.state != 'posted':
                pay.cheque_state = False
            elif not pay.inverse_move_id and pay.payment_type == 'outbound' and pay.move_id.reversal_move_id.filtered(
                    lambda x: x.state == 'posted'):
                pay.cheque_state = False
            elif pay.inverse_move_id:
                pay.cheque_state = 'refused'
            elif pay.get_pdc_statement_line_id():
                pay.cheque_state = 'collected'
            elif pay.last_payment_method_line_id and pay.last_payment_method_line_id.payment_method_id.code not in ['check_printing', 'sw_inbound_check']:
                pay.cheque_state = 'under_collection'
            elif pay.payment_type == 'outbound':
                pay.cheque_state = 'issued'
            else:
                pay.cheque_state = 'in_cheque_box'


    @api.depends('cheque_state', 'is_cheque')
    def _compute_reconciliation_status(self):
        res = super(AccountPayment, self)._compute_reconciliation_status()
        pay_ids = self.filtered(lambda x: x.is_cheque
                                          and x.cheque_state in
                                          ['in_cheque_box', 'under_collection', 'issued'])
        if pay_ids:
            pay_ids.is_matched = False
        return res


    @api.depends('payment_method_line_id', 'currency_id', 'amount','is_cheque','cheque_language_id')
    def _compute_check_amount_in_words(self):
        for rec in self:
            if rec.is_cheque and rec.cheque_language_id and rec.currency_id:
                
                amount_in_word = rec.currency_id.with_context(lang=rec.cheque_language_id.code).amount_to_text(rec.amount)
                if rec.cheque_language_id.code == 'ar_001':
                    if "Dinar" in amount_in_word:
                        amount_in_word = amount_in_word.replace("Dinar",'دينار')
                    if 'Fils' in amount_in_word:
                        amount_in_word = amount_in_word.replace("Fils",'فلس')
                    amount_in_word = "فقط %s"%(amount_in_word)
                else:
                    amount_in_word = "Only %s"%(amount_in_word)
                rec.check_amount_in_words = amount_in_word
            else:
                rec.check_amount_in_words = False

    @api.onchange('is_cheque')
    def change_is_cheque(self):
        if self.is_cheque:
            # self.is_internal_transfer = False
            self.cheque_language_id = self.env.ref('base.lang_ar')
        else:
            self.cheque_language_id = False
            self.due_date = False
            self.cheque_note = False

    def action_post(self):
        self = self.with_context(skip_check_payment_moves=True)
        for rec in self.filtered('is_cheque'):
            rec.move_id.line_ids.date_maturity = rec.due_date
        return super(AccountPayment, self).action_post()
    
                
    def action_draft(self):
        self = self.with_context(skip_check_payment_moves=True)
        res = super(AccountPayment, self).action_draft()
        self.cancel_cheque()
        return res
    
    
    def action_cancel(self):
        self = self.with_context(skip_check_payment_moves=True)
        result = super(AccountPayment, self).action_cancel()
        self.cancel_cheque()
        return result
    
    def copy(self, default=None):
        self = self.with_context(skip_check_payment_moves=True)
        return super(AccountPayment, self).copy(default)
    
    def _synchronize_from_moves(self, changed_fields):
        self = self.with_context(skip_check_payment_moves=True)
        return super(AccountPayment, self)._synchronize_from_moves(changed_fields)
    
    @api.model_create_multi
    def create(self, vals_list):
        self = self.with_context(skip_check_payment_moves=True)
        return super(AccountPayment, self).create(vals_list)
    
    def write(self, vals):
        self = self.with_context(skip_check_payment_moves=True)
        return super(AccountPayment, self).write(vals)
    
    def cancel_cheque(self):
        self = self.with_context(skip_check_payment_moves=True)
        for payment in self.filtered('is_cheque'):
            payment.last_payment_method_line_id = False
            for move in ['route_move_ids', 'inverse_move_id']:
                if payment[move]:
                    payment[move].button_draft()
                    payment[move].button_cancel()
                    payment[move].line_ids.unlink()
                    

    def get_move_lines_dr_cr(self):
        vals = self._prepare_move_line_default_vals()
        return vals[0]['debit'] > 0  and (vals[0],vals[1]) or (vals[1],vals[0])

    def button_open_journal_entry(self):
        if not self.is_cheque:
            return super(AccountPayment,self).button_open_journal_entry()
        move_ids = self.move_id | self.inverse_move_id | self.route_move_ids
        
        action = {
            'name': _("Journal Entry"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'context': {'create': False},
             'views':[(self.env.ref('account.view_move_tree').id,'tree'),
                      (self.env.ref('account.view_move_form').id,'form')]
        }
        if len(move_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': move_ids.id,
            })
            action['views'].pop(0)
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', move_ids.ids)],
               
            })
        return action
    
    
    
    def get_amount(self, amount):
        amount_list = str(amount).split('.')
        if len(amount_list) > 1:
            l2 = amount_list[1]
            if len(l2) == 1:
                amount_list[1] = l2+'00'
            elif len(l2) == 2:
                amount_list[1] = l2+'0'
        return amount_list

    def get_pdc_statement_line_id(self):
        self.ensure_one()
        reconciled_lines = (self.move_id.line_ids | self.route_move_id.line_ids).filtered(
            lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
        reconciled_amls = reconciled_lines.mapped('matched_debit_ids.debit_move_id') | \
                          reconciled_lines.mapped('matched_credit_ids.credit_move_id')
        statement_line_ids = reconciled_amls.mapped('move_id.statement_line_id')
        return statement_line_ids and statement_line_ids[0]
